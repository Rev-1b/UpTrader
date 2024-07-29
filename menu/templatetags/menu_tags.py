from collections import defaultdict

from django import template
from django.db.models import QuerySet
from django.http import Http404

from menu.models import MenuItemModel

register = template.Library()


@register.inclusion_tag('draw_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    item_slug = context.get('item_slug', None)
    menu_slug = context.get('menu_slug', None)

    # Получаем все разделы меню, принадлежащие выбранному меню. Если выбранный пункт не является верхним,
    # все вышестоящие пункты будут включены в запрос
    menu_queryset = MenuItemModel.objects.filter(
        head_menu__name=menu_name).select_related('parent')

    parent_to_item_dict = defaultdict(list)
    item_to_parent_dict = {}

    for item in menu_queryset:
        # Словарь, который содержит все дочерние элементы на 1 уровень ниже для каждого пункта меню
        parent_to_item_dict[str(item.parent)].append(item)

        # Словарь, который содержит пару 'пункт меню': 'его родительский элемент'. Нужен для оптимизации
        item_to_parent_dict[str(item)] = item.parent

    if item_slug:  # Если был выбран любой пункт меню, кроме корневых
        item = _find_item(menu_queryset, item_slug)
        resulted_menu = _create_menu_dict(parent_to_item_dict, item_to_parent_dict, item)
    else:  # Если выбран корневой пункт меню (объект HeadMenuModel)
        resulted_menu = {}

    # None будет иметь только самый высокоуровневый элемент, с которого и начнется отрисовка меню
    resulted_menu['main'] = parent_to_item_dict['None']

    return {'menu': resulted_menu, 'curr': 'main', 'menu_slug': menu_slug}


def _create_menu_dict(parent_to_item: dict[str, list[MenuItemModel]],
                      item_to_parent: dict[str, MenuItemModel],
                      item: MenuItemModel) -> dict[MenuItemModel, list[MenuItemModel]]:
    menu = {}
    while item:
        # Для отображаемого первого уровня вложенности для текущего элемента меню
        item_children = parent_to_item[str(item)]
        menu[item] = item_children

        # Приходится прибегать к такому костылю, так как item = item.parent вызовет n+1 для каждого уровня вложенности
        item = item_to_parent[str(item)]

    return menu


def _find_item(queryset: QuerySet[MenuItemModel], item_slug: str) -> MenuItemModel:
    # итерируемся по menu_queryset как по обычному списку, чтобы не создавать дополнительный запрос
    for item in queryset:
        if item.slug == item_slug:
            return item
    raise Http404(f'"{item_slug}" is not a valid menu item')
