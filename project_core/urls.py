from site.view import HomeView, StatView, ViewView, CommentView, DeleteComment

urlpatterns = [
    [r'^/comment/$', CommentView(template_name='main.html')],
    [r'^/view/$', ViewView(template_name='main.html')],
    [r'^/stat/$', StatView(template_name='main.html')],
    [r'^/delete/$', DeleteComment()],
    [r'^/$', HomeView(template_name='main.html')],
]
