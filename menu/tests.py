from django.test import TestCase, Client
from django.urls import reverse

from .models import HeadMenuModel, MenuItemModel


class MenuTests(TestCase):
    def setUp(self):
        self.client = Client()
        menu = HeadMenuModel.objects.create(name='Bio', slug='bio')
        item1_1 = MenuItemModel.objects.create(name='Царство животных', slug='tcarstvo-zyvotnyh', head_menu=menu)
        item1_2 = MenuItemModel.objects.create(name='Царство растений', slug='tcarstvo-rasteniy', head_menu=menu)
        item2_1 = MenuItemModel.objects.create(name='Многоклеточные', slug='mnogokletochnye', head_menu=menu, parent=item1_1)
        item3_1 = MenuItemModel.objects.create(name='Тип хордовые', slug='tip-hordovye', head_menu=menu, parent=item2_1)
        item4_1 = MenuItemModel.objects.create(name='Человек', slug='chelovek', head_menu=menu, parent=item3_1)

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'draw_menu/main_page.html')
        self.assertIn('head_menu', response.context)
        self.assertEqual(len(response.context['head_menu']), 1)
        self.assertEqual(response.context['head_menu'][0].name, 'Bio')

    def test_menu(self):
        response = self.client.get(reverse('menu', kwargs={'menu_slug': 'bio'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'draw_menu/main_page.html')
        self.assertIn('menu', response.context)
        self.assertEqual(len(response.context['menu']), 1)
        self.assertEqual(len(response.context['menu']['main']), 2)

    def test_menu_item(self):
        response = self.client.get(reverse('menu_item', kwargs={'menu_slug': 'bio', 'item_slug': 'chelovek'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'draw_menu/main_page.html')
        self.assertIn('menu', response.context)
        self.assertEqual(len(response.context['menu']), 5)

