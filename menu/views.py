from django.views.generic import TemplateView
from menu.models import HeadMenuModel


class MainPageView(TemplateView):
    template_name = 'draw_menu/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_menu'] = HeadMenuModel.objects.all()
        context['params'] = self.kwargs
        return context


