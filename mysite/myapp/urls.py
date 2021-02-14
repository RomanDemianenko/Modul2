from django.contrib import admin
from django.urls import include, path, re_path

from myapp.views import UserLoginView, UserLogout, RegistrationView, ProductListView, ProductUpdateView, OrderViewList, \
    ReturnOfGoodCreateView, CancelListView, ReturnPositionRedirectsView, BuyingCreateView, ProductCreateView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('buying/', BuyingCreateView.as_view(), name='buying'),
    path('admin/', admin.site.urls),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('order/', OrderViewList.as_view(), name='order'),
    path('order/return', ReturnOfGoodCreateView.as_view(), name='return'),
    path('cancel/', CancelListView.as_view(), name='cancel'),
    path('cancel/retrun/<int:pk>/', ReturnPositionRedirectsView.as_view(), name='come_back')
]
