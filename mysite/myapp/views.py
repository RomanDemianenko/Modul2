from datetime import datetime, timezone, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, RedirectView
from django.views.generic.base import View

from myapp.forms import RegistrationForm, ProductForm, OrderForm, LoginForm, CancelForm
from myapp.models import Product, MyUser, Order, Cancel


class BaseView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.order_by('-id')
        context = {
            'products': products
        }
        return render(request, 'base.html', context)


class UserLoginView(LoginView):

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'You are login')
                    return HttpResponseRedirect('/')
            else:
                messages.warning(request, 'You have login already')
        else:
            print('hello45')
            return HttpResponseRedirect('/')

        context = {'form': form}
        return render(request, 'login.html', context)


class RegistrationView(CreateView):
    model = MyUser

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        product = Product.objects.all()
        context = {'form': form, 'product': product}
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.name = form.cleaned_data['name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            messages.success(request, 'Welcomm in our club')
            return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'registration.html', context)


class UserLogout(LogoutView):
    login_url = '/products/'
    template_name = 'log_out.html'
    next_page = '/'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    login_url = '/login'
    permission_required = 'request.user.is_superuser'
    model = Product
    form_class = ProductForm
    success_url = '/'
    template_name = 'create.html'


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'request.user.is_superuser'
    model = Product
    fields = '__all__'
    template_name = 'update.html'
    success_url = '/'


class ProductListView(ListView):
    model = Product
    form_class = ProductForm
    paginate_by = 5
    ordering = ['-id']
    template_name = 'base.html'


class BuyingCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = '/'
    template_name = 'buying.html'

    def post(self, request, *args, **kwargs):
        # form = OrderForm(request.POST)

        user_quantity = request.POST['quantity']
        user_quantity = int(user_quantity)
        product_id = request.POST['product']
        product = Product.objects.get(id=product_id)
        user_id = request.POST['customer']
        user = MyUser.objects.get(id=user_id)
        if product.quantity >= user_quantity:
            if user.cash >= user_quantity * product.price:
                product.quantity -= user_quantity
                user.cash -= user_quantity * product.price
                order = Order.objects.create(customer=user, product=product,
                                             total_price=user_quantity * product.price)
                user.save()
                product.save()
                order.save()
                messages.success(self.request, 'Thx for using our servers')
            else:
                messages.warning(self.request, 'You need to fill up a wallet')
        else:
            messages.warning(self.request, 'We don`t have enough staff')
        return HttpResponseRedirect('/')


class OrderViewList(ListView, LoginRequiredMixin):
    model = Order
    # form = OrderForm
    template_name = 'order.html'
    paginate_by = 5
    ordering = ['-order_time']
    login_url = '/login'


class CancelListView(PermissionRequiredMixin, ListView):
    permission_required = 'request.user.is_superuser'
    model = Cancel
    fields = '__all__'
    template_name = 'cancel.html'
    paginate_by = 5


class ReturnOfGoodRedirectView(RedirectView, LoginRequiredMixin):
    # model = Cancel
    # form_class = CancelForm
    # login_url = '/login/'

    def get(self, request, *args, **kwargs):
        order_id = request.POST.get('cancel')
        # order_id = form.cleaned_data.get('cancel').id
        order = Order.objects.get(id=order_id)
        if order_id is None:
            messages.info(request, 'There is nothing to talk about')
            return HttpResponseRedirect('/')

        if datetime.now(timezone.utc) - order.order_time < timedelta(seconds=180):
            cancel = Cancel.objects.create(come_back=order)
            cancel.save()
            messages.info(request, 'YOU cancelled the order(((((')
        else:
            messages.warning(request, 'You`are late')
        return HttpResponseRedirect('/')


class ReturnPositionRedirectsView(PermissionRequiredMixin, RedirectView):
    permission_required = 'request.user.is_superuser'

    def get(self, request, *args, **kwargs):
        cancel_id = request.POST.get('id')
        if cancel_id is None:
            messages.info(self.request, 'There is nothing to talk about')
            HttpResponseRedirect('/')
        cancel_id = Cancel.objects.get(id=cancel_id).come_back.customer.id
        user = MyUser.objects.get(id=cancel_id)
        user.cash = Cancel.objects.get(id=cancel_id).come_back.total_price
        user.save()
        product = Cancel.objects.get(id=cancel_id).come_back.product
        quantity = Cancel.objects.get(id=cancel_id).come_back.quantity
        product.quantity += quantity
        product.save()
        Cancel.objects.get(id=cancel_id).delete()
        messages.info(request, 'Order Cancelled')
        return HttpResponseRedirect('/cancel/')
