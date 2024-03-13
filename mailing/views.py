from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from blog.models import Post
from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Mailing, Client, Message, Log


class HomePageView(TemplateView):
    template_name = 'mailing/main_page.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_count'] = Mailing.objects.all().count()
        context_data['active_mailing_count'] = Mailing.objects.filter(is_active=True, ).count()
        context_data['clients_count'] = Client.objects.all().distinct().count()
        context_data['posts'] = Post.objects.all()[:3]

        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    """Просмотр списка рассылок"""
    model = Mailing


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Просмотр рассылки"""
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создание"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        if form.is_valid():
            new_mailing = form.save(commit=False)
            new_mailing.owner = self.request.user
            new_mailing.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:mailing_list')



class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser or self.object.owner != self.request.user:
            raise Http404
        return self.object


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление"""
    model = Mailing
    success_url = reverse_lazy('mailing:home')


class ClientListView(ListView):
    """Просмотр списка клиентов"""
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создание клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MessageListView(LoginRequiredMixin, ListView):
    """Просмотр сообщений"""
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание клиента"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class LogListView(ListView):
    """Просмотр логов"""
    model = Log

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all'] = context_data['object_list'].count()
        context_data['success'] = context_data['object_list'].filter(attempt_status=True).count()
        context_data['error'] = context_data['object_list'].filter(attempt_status=False).count()
        return context_data


@login_required
@permission_required('mailing.set_is_active')
def active_toggle(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.is_active:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True
    mailing_item.save()
    return redirect(reverse('mailing:mailing_list'))