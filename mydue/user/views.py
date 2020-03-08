from django.shortcuts import render
from .forms import UserForm, UserLoginForm
from django.views.generic import FormView, CreateView, RedirectView, TemplateView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.models import User
from datetime import datetime
from services.models import Services
from .quickstart import parse


class Home(TemplateView):
    template_name = 'home.html'

# @login_required
def dashView(request):
    today = datetime.now()
    hour, minute = today.hour, today.minute
    print(hour)
    print(minute)
    if hour == 0 and minute < 59:
        parse_data = parse()
        print(parse_data)
        for data in parse_data:
            due = Services.objects.create(user = request.user)
            due.provider = data['vendor']
            due.message_id = data['id']
            due.bill_id = data['invoiceid']
            due.due_date = data['date']
            due.amount = data['amt']
            due.save()
    else:
        pass
    return render(request,'dash.html')

    # {'from': 'odraamkv@gmail.com', 'id': '170b68278bcde106', 'amt': '1500',
    # 'date': '22/03/2020', 'vendor': 'Netflix', 'invoiceid': '121231231'}


# class DashView(TemplateView):
#     template_name="dash.html"

class RegView(FormView):
    template_name = "register.html"
    form_class = UserForm
    success_url = "../login"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginView(FormView):
    success_url = '../dash'
    form_class = UserLoginForm
    template_name = 'login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.authenticate_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    url = '../'
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)
