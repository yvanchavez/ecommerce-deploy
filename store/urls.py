from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .views import password_reset, password_reset_confirm, perfil, ProductView, ProductDetailView, ProductUpdateView, \
    ProductCreateView, ProductDeleteView

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('detail/<int:id>', views.detail, name="detail"),
    path('search/', views.search, name="search"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('login/', LoginView.as_view(template_name="store/login.html"), name='login'),
    path('salir/', LogoutView.as_view(), name='logout'),
    path('perfil/', perfil, name='perfil'),
    path('registrate/', views.registrate, name="registrate"),
    path('resetpassword/', password_reset, name='resetpassword'),
    path('confirmar-nueva-contraseña/<key>/', password_reset_confirm, name='password_reset_confirm'),
    path('change_password/', views.change_password, name="change_password"),

    path('products/', ProductView.as_view(), name='products'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='productdetail'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

]
