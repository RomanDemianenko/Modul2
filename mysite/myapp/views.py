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

from myapp.forms import RegistrationForm, ProductForm, OrderForm, LoginForm
from myapp.models import Product, MyUser, Order, Cancel


# class CartMixin():
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             customer = Customer.objects.filter(user=request.user).first()
#             if not customer:
#                 customer = Customer.objects.create(
#                     user=request.user
#                 )
#             cart = Cart.objects.filter(owner=customer, in_order=False).first()
#             if not cart:
#                 cart = Cart.objects.create(owner=customer)
#         else:
#             cart = Cart.objects.filter(for_anonymous_user=True).first()
#             if not cart:
#                 cart = Cart.objects.create(for_anonymous_user=True)
#         self.cart = cart
#         return super().dispatch(request, *args, **kwargs)
#
#


# class AddToCartView(CartMixin):
#
#     def get(self, request, *args, **kwargs):
#         product_slug = kwargs.get('slug')
#         product = Product.objects.get(slug=product_slug)
#         car


class BaseView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.order_by('-id')
        context = {
            'products': products
        }
        return render(request, 'base.html', context)


class UserLoginView(LoginView):
    # form_class = AuthenticationForm
    # success_url = '/'
    # template_name = 'login.html'

    # http_method_names = ['get', 'post']

    # def get_success_url(self):
    #     return self.success_url

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)
        # product = Product.objects.all()
        context = {'form': form}
        # return self.render_to_response(self.get_context_data())
        # return super().get(request=self.request)
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        # form = self.get_form(AuthenticationForm)
        form = LoginForm(request.POST)
        print('hello1')
        if form.is_valid():
            print('hello2')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print('hello22')
            if user:
                print('hello3')
                if user.is_active:
                    login(request, user)
                    print('hello4')
                    messages.success(request, 'You are login')
                    return HttpResponseRedirect('/')
                # return self.form_valid(form)
            else:
                messages.warning(request, 'You have login already')
        else:
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            # user = authenticate(username=username, password=password)
            # login(request, user)
            print('hello45')
            return HttpResponseRedirect('/')
            # return self.form_invalid(form)

        context = {'form': form}
        return render(request, 'login.html', context)


class RegistrationView(CreateView):
    model = MyUser
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = '/'

    def get_success_url(self):
        return self.success_url

    http_method_names = ['get', 'post']

    # def get(self, request, *args, **kwargs):
    #     form = RegistrationForm(request.POST)
    #     product = Product.objects.all()
    #     context = {'form': form, 'product': product}
    #     return render(request, 'registration.html', context)
    #
    # def post(self, request, *args, **kwargs):
    #     form = RegistrationForm(request.POST)
    #     if form.is_valid():
    #         new_user = form.save(commit=False)
    #         new_user.username = form.cleaned_data['username']
    #         new_user.email = form.cleaned_data['email']
    #         new_user.name = form.cleaned_data['name']
    #         new_user.save()
    #         new_user.set_password(form.cleaned_data['password'])
    #         new_user.save()
    #         MyUser.objects.create(user=new_user)
    #         MyUser.objects.upgrade(cash='10000')
    #         user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    #         login(request, user)
    #         messages.success(request, 'Welcomm in our club')
    #         return HttpResponseRedirect('/')
    #     context = {'form': form}
    #     return render(request, 'registration.html', context)


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


class BuyingRedirectView(RedirectView):
    model = Order
    form_class = OrderForm

    def get(self, request, *args, **kwargs):
        product_id = request.POST['id']
        product = Product.objects.get(id=product_id)
        user_quantity = request.POST['quantity']
        user_quantity = int(user_quantity)
        if product.quantity >= user_quantity:
            customer_id = request.customer.id
            user = MyUser.objects.get(id=customer_id)
            if user.cash < (product.price * user_quantity):
                product.quantity -= user_quantity
                user.cash -= product.price * user_quantity
                order = Order.objects.create(customer=user, product=product,
                                             total_price=product.price * user_quantity)
                user.save()
                product.save()
                order.save()
                messages.success(request, 'Thx for using our servers')
            else:
                messages.warning(request, 'You need to fill up a wallet')
        else:
            messages.warning(request, 'We don`t have enough staff')
        return HttpResponseRedirect('/')


class OrderViewList(ListView, LoginRequiredMixin):
    model = Order
    # form = OrderForm
    template_name = 'order.html'
    paginate_by = 5
    ordering = ['order_time']
    login_url = '/login'


class CancelListView(PermissionRequiredMixin, ListView):
    permission_required = 'request.user.is_superuser'
    model = Cancel
    fields = '__all__'
    template_name = 'cancel.html'
    paginate_by = 5


class ReturnOfGoodRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        order_id = request.POST.get('id')
        if order_id is None:
            messages.info(request, 'There is nothing to talk about')
            return HttpResponseRedirect('/')
        order = Order.objects.get(id=order_id)
        if datetime.now(timezone.utc) - order.order_time < timedelta(seconds=180):
            cancel = Cancel.objects.create(come_back=order)
            cancel.save()
            messages.info(request, 'YOU cancelled the order(((((')
        else:
            messages.warning(request, 'You`are late')
        return HttpResponseRedirect('/order/')


class ReturnPositionRedirectsView(RedirectView):
    def get(self, request, *args, **kwargs):
        post_id = request.POST.get('id')
        if post_id is None:
            HttpResponseRedirect('/')
        cancel_id = Cancel.objects.get(id=post_id).come_back.customer.id
        user = MyUser.objects.get(id=cancel_id)
        user.cash = Cancel.objects.get(id=cancel_id).come_back.total_price
        user.save()
        product = Cancel.objects.get(id=cancel_id).come_back.product
        quantity = Cancel.objects.get(id=cancel_id).come_back.quantity
        product.quantity += quantity
        product.save()
        Cancel.objects.get(id=cancel_id).delete()
        messages.info(request, 'Order Cancelled')
        return HttpResponseRedirect('/cancel')
