from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("cart", views.cart_view, name="cart"),
    path("order", views.order_view, name="order"),
    path("removefromcart/<int:cart_id>/", views.removefromcart_view, name="removefromcart"),
    path("payment", views.payment,name="payment" ),
    path("number", views.number, name="number")
    ]
