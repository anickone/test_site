from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from products import views


urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('products/',
         views.ProductList.as_view(),
         name='product-list'),
    re_path('products/(?P<pk>[0-9a-z-]+)/',
            views.ProductDetail.as_view(),
            name='product-detail'),
    path('products-users/',
         views.UserList.as_view(),
         name='user-list'),
    path('products-users/<int:pk>/',
         views.UserDetail.as_view(),
         name='user-detail')
])
