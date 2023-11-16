from django.urls import path

from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('login/', views.login, name="login"),
	path('cart/', views.cart, name='cart'),
	path('checkout/', views.checkout, name="checkout"),
	path('index/', views.index, name="index"),
	path('update_item/', views.updateItem, name="update_item")

]