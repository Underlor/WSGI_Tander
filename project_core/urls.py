from site.view import HomeView, StatView, ViewView, CommentView, GetRegion, StatCityView

urlpatterns = [
    [r'^/comment/$', CommentView(template_name='main.html')],
    [r'^/view/$', ViewView(template_name='main.html')],
    [r'^/stat/(?P<region_id>[0-9]+)/$', StatCityView(template_name='main.html')],
    [r'^/stat/$', StatView(template_name='main.html')],
    [r'^/getcities/$', GetRegion()],
    [r'^/$', HomeView(template_name='main.html')],
]
