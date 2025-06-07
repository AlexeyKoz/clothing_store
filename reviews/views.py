from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
from .models import Review


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Импортируем форму здесь, чтобы избежать циклических импортов
    from .forms import ReviewForm

    # Проверяем, не оставлял ли пользователь уже отзыв на этот товар
    existing_review = Review.objects.filter(user=request.user, product=product).first()
    if existing_review:
        messages.warning(request, "You have already reviewed this product. You can edit your existing review.")
        return redirect('reviews:edit_review', review_id=existing_review.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Your review has been added successfully!")
            return redirect('catalog:product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {
        'form': form,
        'product': product
    })


@login_required
def edit_review(request, review_id):
    from .forms import ReviewForm

    review = get_object_or_404(Review.objects.select_related('product'), id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated successfully!")
            return redirect('catalog:product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/edit_review.html', {
        'form': form,
        'review': review,
        'product': review.product
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review.objects.select_related('product'), id=review_id, user=request.user)
    product_id = review.product.id

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect('catalog:product_detail', product_id=product_id)

    return render(request, 'reviews/delete_review.html', {
        'review': review
    })