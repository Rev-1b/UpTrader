from django.urls import path
from menu.views import MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('<slug:menu_slug>/', MainPageView.as_view(), name='menu'),
    path('<slug:menu_slug>/<slug:item_slug>', MainPageView.as_view(), name='menu_item'),
]