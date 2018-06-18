from django.contrib import admin
from django.urls import path, re_path

from mainapp import views

urlpatterns = {
    path('', views.home),
    path('market/<int:categoryid>/<int:childid>/<int:sortid>', views.market),
    path('cart',views.cart),
    re_path('^mine',views.mine),
    path('register',views.register),
    path('upload',views.upload),
    path('login',views.login),
    path('logout',views.logout),
    path('select/<int:cart_id>',views.selectCart),
    path('addCart/<int:cart_id>',views.addCart),
    path('subCart/<int:cart_id>',views.subCart),
    path('order/<int:num>',views.order),
    path('pay/<str:num>/<int:payType>',views.pay)
}
