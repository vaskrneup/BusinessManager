from django import template

register = template.Library()


@register.filter("get_current_price_filter")
def get_current_price_filter(instance, model_cache):
    return instance.get_current_price(model_cache)
