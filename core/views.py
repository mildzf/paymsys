from django.contrib.auth.mixins import UserPassesTestMixin 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.conf import settings 

from .mixins import PageLinksMixin


class StaffViewMixin(UserPassesTestMixin, SuccessMessageMixin):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class StaffCreateView(StaffViewMixin, CreateView):
    pass 


class StaffDeleteView(StaffViewMixin, DeleteView):
    pass 


class StaffDetailView(StaffViewMixin, DetailView):
    pass 


class StaffListView(StaffViewMixin, PageLinksMixin, ListView):
    paginate_by = settings.PAGINATE_BY


class StaffUpdateView(StaffViewMixin, UpdateView):
    pass 

class StaffDetailListView(StaffViewMixin, SingleObjectMixin, PageLinksMixin, ListView):
    paginate_by = settings.PAGINATE_BY