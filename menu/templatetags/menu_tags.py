from django import template
from collections import defaultdict

from menu.models import MenuItemModel

register = template.Library()


@register.inclusion_tag('draw_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    '''
    Неоптимальное решение! Для избегания проблемы n+1 при построении маршрута до верхнего элемента меню было принято
    решение переводить QuerySet в список, что избавляет от проблемы с множественными запросами, но создает новую -
    хранение в памяти лишних данных. Я уверен, что есть способ избежать этих двух проблем, но я за ограниченное время
    его найти не смог.
    '''
    item_slug = context.get('params', {}).get('item_slug', None)
    menu_slug = context.get('params', {}).get('menu_slug', None)

    menu_items = list(MenuItemModel.objects.filter(
        head_menu__name=menu_name).select_related('parent'))

    parent_item_dict = defaultdict(list)
    item_parent_dict = {}

    for item in menu_items:
        parent_item_dict[str(item.parent)].append(item)
        item_parent_dict[str(item)] = item.parent

    if item_slug:
        item = _find_item(menu_items, item_slug)
        menu_temp = _create_menu_dict(parent_item_dict, item_parent_dict, item)
    else:
        menu_temp = {}
    menu_temp['main'] = parent_item_dict['None']

    return {'menu': menu_temp, 'curr': 'main', 'menu_slug': menu_slug}


def _create_menu_dict(parent_item: dict[str, list[MenuItemModel]],
                      item_parent: dict[str, MenuItemModel],
                      item: MenuItemModel) -> dict[MenuItemModel, list[MenuItemModel]]:
    menu = {}
    while item:
        item_children = parent_item[str(item)]
        menu[item] = item_children

        item = item_parent[str(item)]

    return menu


def _find_item(lst: list[MenuItemModel], item_slug: str) -> MenuItemModel:
    for item in lst:
        if item.slug == item_slug:
            return item
