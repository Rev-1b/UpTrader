from django.contrib import admin
from menu.models import HeadMenuModel, MenuItemModel


class HeadMenuInLine(admin.TabularInline):
    model = MenuItemModel
    prepopulated_fields = {"slug": ("name",)}


class MenuItemInline(admin.TabularInline):
    model = MenuItemModel
    prepopulated_fields = {'slug': ('name',)}


@admin.register(HeadMenuModel)
class HeadMenuModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        HeadMenuInLine,
    ]


@admin.register(MenuItemModel)
class MenuModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        MenuItemInline
    ]
