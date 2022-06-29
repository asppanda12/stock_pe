from django import urls
from django.urls import path
from .import views 
urlpatterns = [
    path('', views.index, name='index'),
    path('take_form', views.take_form, name='take_form'),
      path('buyshare', views.buyshare, name='buyshare'),
        path('sellshare', views.sellshare, name='sellshare'),
          path('register', views.register, name='register'),
           path('buy', views.buy, name='buy'),
            path('login', views.login, name='login'),
             path('sell', views.sell, name='sell'),
               path('logout', views.logout, name='logout'),
                path('register1', views.register1, name='register1'),
                path('home', views.home, name='home'),
                path('login1', views.login1, name='login1'),
                path('router', views.router, name='router'),

]