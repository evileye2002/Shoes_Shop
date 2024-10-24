from django import template

register = template.Library()


@register.inclusion_tag("partials/breadcrumbs.html")
def show_breadcrumbs(breadcrumbs, last_crum: str = None):
    return {
        "breadcrumbs": breadcrumbs,
        "last_crum": last_crum,
    }
