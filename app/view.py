from core.view_core import BaseView


class IndexView(BaseView):
    def get(self, request, *args, **kwargs):
        kwargs = {'irem': '123s'}
        return super().get(request, *args, **kwargs)
