from django import template

register = template.Library()

BUTTON_CLASSES = {
    "primary": "text-white bg-primary-700 hover:bg-primary-800 focus:ring-blue-300 dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-blue-800",
    "secondary": "text-gray-900 bg-white border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700",
    "dark": "text-white bg-gray-800 hover:bg-gray-900 focus:ring-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700",
    "light": "text-gray-900 bg-white border border-gray-300 hover:bg-gray-100 focus:ring-gray-100 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700",
    "success": "text-white bg-green-700 hover:bg-green-800 focus:ring-green-300 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800",
    "error": "text-white bg-red-700 hover:bg-red-800 focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900",
    "warning": "text-white bg-yellow-400 hover:bg-yellow-500 focus:ring-yellow-300 dark:focus:ring-yellow-900",
    # outline
    "primary-outline": "text-center border text-primary-700 border-primary-700 hover:text-white hover:bg-primary-800 focus:ring-primary-300 dark:border-primary-500 dark:text-primary-500 dark:hover:text-white dark:hover:bg-primary-500 dark:focus:ring-primary-800",
    "success-outline": "text-center border text-green-700 border-green-700 hover:text-white hover:bg-green-800 focus:ring-green-300 dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-900",
    "error-outline": "text-center border text-red-700 border-red-700 hover:text-white hover:bg-red-800 focus:ring-red-300 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900",
    "warning-outline": "text-center border text-yellow-400 border-yellow-400 hover:text-white hover:bg-yellow-500 focus:ring-yellow-300 dark:border-yellow-300 dark:text-yellow-300 dark:hover:text-white dark:hover:bg-yellow-400 dark:focus:ring-yellow-900",
}


@register.filter
def get_button_classes(type):
    if type in BUTTON_CLASSES:
        return BUTTON_CLASSES[type]

    return BUTTON_CLASSES["primary"]
