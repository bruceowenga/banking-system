
from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, ListView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Meeting

from .forms import UserRegistrationForm, UserAddressForm, UpdateProfileForm, UpdateAccountForm, UpdateAddressForm


User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:deposit_money')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    redirect_authenticated_user = False


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


def editProfile(request):
    if request.method == 'GET':
        profile_form = UpdateProfileForm(instance=request.user)
        account_form = UpdateAccountForm(instance=request.user)
        address_form = UpdateAddressForm(instance=request.user.address)
        context = {'profile_form': profile_form, 'account_form': account_form, 'address_form': address_form}
        return render(request, 'accounts/edit_profile.html', context)
    else:
        profile_form = UpdateProfileForm(request.POST, instance=request.user)
        account_form = UpdateAccountForm(request.POST, instance=request.user)
        address_form = UpdateAddressForm(request.POST, instance=request.user.address)

        if profile_form.is_valid() and account_form.is_valid() and address_form.is_valid():
            profile_form.save()
            account_form.save()
            address_form.save()
            messages.success(
                request,
                'Your Profile Has Been Updated.'
            )
            return HttpResponseRedirect(
                reverse_lazy('accounts:edit_profile')
            )
        else:
            context = {'profile_form': profile_form, 'account_form': account_form, 'address_form': address_form}
            return render(request, 'accounts/edit_profile.html', context)


def attendance(request):
    # attendance_list = request.meeting.attendance_set.all(user=request.user)
    # context = {'attendance_list': attendance_list}
    return render(request, 'accounts/attendance.html', context)

class AttendanceView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'accounts/attendance.html'
    context_object_name = 'attendance_list'

    def get_queryset(self):
        return self.model.attendance_set.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meeting_list'] = Meeting.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        meeting_id = request.POST.get('meeting_id')
        meeting = Meeting.objects.get(id=meeting_id)
        # attendance = Attendance.objects.create(user=request.user, meeting=meeting)
        # messages.success(
        #     request,
        #     'You Have Been Marked As Present For The Meeting.'
        # )
        return HttpResponseRedirect(
            reverse_lazy('accounts:attendance')
        )