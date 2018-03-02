class BaseView(object):
    context = {}

    def get(self, request, *args, **kwargs):
        self.context = kwargs

    def post(self, request, *args, **kwargs):
        pass

    def view(self, request, *args, **kwargs):
        if request['REQUEST_METHOD'] == 'GET':
            return self.get(request, *args, **kwargs)
        else:
            return self.post(request, *args, **kwargs)
