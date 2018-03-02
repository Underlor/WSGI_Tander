class BaseView(object):

    def get(self, request, *args, **kwargs):
        return kwargs

    def post(self, request, *args, **kwargs):
        return kwargs

    def view(self, request, *args, **kwargs):
        if request['REQUEST_METHOD'] == 'GET':
            return self.get(request, *args, **kwargs)
        else:
            return self.post(request, *args, **kwargs)
