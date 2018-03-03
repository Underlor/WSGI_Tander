class BaseView:
    def get(self, request, *args, **kwargs):
        return kwargs

    def post(self, request, *args, **kwargs):
        return kwargs

    def view(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
        # if request['REQUEST_METHOD'] == 'GET':
        #     return self.get(request, *args, **kwargs)
        # elif request['REQUEST_METHOD'] == 'POST':
        #     return self.post(request, *args, **kwargs)
