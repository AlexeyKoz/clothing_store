from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(email_confirmed)
def enforce_single_email(request, email_address, **kwargs):
    """
    When a new email address is confirmed, this signal makes it the user's
    exclusive primary email. It forcefully sets all other emails for the
    user to non-primary, promotes the new one, updates the core user model,
    and then deletes all other email address records.
    """
    user = email_address.user

    # Atomically set all of the user's emails to non-primary first.
    EmailAddress.objects.filter(user=user).update(primary=False)

    # Set the newly confirmed email as primary.
    email_address.primary = True
    email_address.save()

    # Directly update the main email field on the user model itself.
    user.email = email_address.email
    user.save(update_fields=['email'])

    # Finally, delete all other email addresses associated with this user.
    EmailAddress.objects.filter(user=user).exclude(
        pk=email_address.pk).delete()
