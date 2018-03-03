from site.view import HomeView, StatView, ViewView, CommentView

urlpatterns = [
    [r'^/comment/$', CommentView, 'main.html'],
    [r'^/view/$', ViewView, 'main.html'],
    [r'^/stat/$', StatView, 'main.html'],
    [r'^/$', HomeView, 'main.html'],
]
