from django.contrib import admin
from django.urls import include, path, re_path

from myapp.views import UserLoginView, UserLogout, RegistrationView, ProductListView, ProductUpdateView, OrderViewList, \
    ReturnOfGoodRedirectView, CancelListView, ReturnPositionRedirectsView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogout.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('update/', ProductUpdateView.as_view(), name='change_products_list'),
    path('order/', OrderViewList.as_view()),
    path('order/return', ReturnOfGoodRedirectView.as_view()),
    path('cancel', CancelListView.as_view()),
    path('cancel/list', ReturnPositionRedirectsView.as_view())
    # path('products/', ProductListView.as_view(), name='products'),
]
