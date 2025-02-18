from django.views import View
from app.views.views_decorator import protected, unauthorized, public


class UnauthorizedView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, 'get'): self.get = unauthorized(self.get)
        if hasattr(self, 'post'): self.post = unauthorized(self.post)

class ProtectedView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, 'get'): self.get = protected(self.get)
        if hasattr(self, 'post'): self.post = protected(self.post)

class PublicView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, 'get'): self.get = public(self.get)
        if hasattr(self, 'post'): self.post = public(self.post)
