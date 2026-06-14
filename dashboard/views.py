from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .models import Asset, Task


class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset_count'] = Asset.objects.count()
        context['task_open_count'] = Task.objects.filter(status='open').count()
        context['task_in_progress_count'] = Task.objects.filter(status='in_progress').count()
        context['task_done_count'] = Task.objects.filter(status='done').count()
        return context


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='admin').exists() or self.request.user.is_superuser

    def handle_no_permission(self):
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(self.request.get_full_path())


class IsAdminContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_admin'] = user.is_authenticated and (
            user.is_superuser or user.groups.filter(name='admin').exists()
        )
        return context


class AssetListView(IsAdminContextMixin, ListView):
    model = Asset
    template_name = 'dashboard/asset_list.html'
    context_object_name = 'assets'


class AssetDetailView(DetailView):
    model = Asset
    template_name = 'dashboard/asset_detail.html'
    context_object_name = 'asset'


class AssetCreateView(AdminRequiredMixin, CreateView):
    model = Asset
    template_name = 'dashboard/asset_form.html'
    fields = ['name', 'status', 'location', 'notes']
    success_url = reverse_lazy('asset_list')


class TaskListView(IsAdminContextMixin, ListView):
    model = Task
    template_name = 'dashboard/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'dashboard/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(AdminRequiredMixin, CreateView):
    model = Task
    template_name = 'dashboard/task_form.html'
    fields = ['title', 'description', 'status']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
