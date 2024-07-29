from django.template.defaulttags import register


# Если честно, я был сильно удивлен, почему такой базовый шаблонный фильтр все еще не был добавлен по умолчанию
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
