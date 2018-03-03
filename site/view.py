from core.sql_core import db
from core.view_core import BaseView


class HomeView(BaseView):
    def get(self, request, *args, **kwargs):
        # kwargs = {'home':True}
        kwargs['home'] = True
        return super().get(request, *args, **kwargs)


class CommentView(BaseView):
    def get(self, request, *args, **kwargs):
        kwargs['comment'] = True
        return super().get(request, *args, **kwargs)


class ViewView(BaseView):
    def get(self, request, *args, **kwargs):
        kwargs['view'] = True
        kwargs['comments'] = db.get_data_by_sql('SELECT * FROM comments')
        print(kwargs['comments'])
        return super().get(request, *args, **kwargs)


class StatView(BaseView):
    def get(self, request, *args, **kwargs):
        kwargs['stat'] = True
        return super().get(request, *args, **kwargs)
