from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_product_related_cache(sender, instance, **kwargs):
    print("Redis: Cleared popular_products cache")
    cache.delete("popular_products")

    # Очистка связанных кэшей поиска
    product_name = instance.name.lower()
    try:
        keys = cache._cache.keys("search:*")  # Работает только с Redis backend
        cleared = 0

        for key in keys:
            key_str = key.decode("utf-8") if isinstance(key, bytes) else key
            query = key_str.split("search:")[1]
            if query in product_name:
                cache.delete(key_str)
                cleared += 1

        if cleared:
            print(f"Redis: Cleared {cleared} search cache entries related to '{product_name}'")
    except Exception as e:
        print(f"⚠️ Redis search cache cleanup failed: {e}")
