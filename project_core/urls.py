from site.view import HomeView, StatView, ViewView, CommentView

urlpatterns = [
    [r'^/comment/$', CommentView(template_name='main.html')],
    [r'^/view/$', ViewView(template_name='main.html')],
    [r'^/stat/$', StatView(template_name='main.html')],
    [r'^/$', HomeView(template_name='main.html')],
]
