from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('login',views.loginuser , name='login'),
    path('signup', views.signup, name='signup'),
    path('logout',views.logoutuser , name='logout'),
   # path('',views.index , name='data'),
    #path("home",views.index , name='data'),
    #path("about",views.about , name='about'),
    path("sos",views.sos , name='sos'),
    path("live",views.live , name='live'),
    path("selfdefence",views.selfdefence , name='selfdefence'),
    path('',views.contact , name='contact'),
    #new
    path("send_location/", views.send_location, name="send_location"),
    path("send_alert/", views.send_alert, name="send_alert"),
    path("edit/<int:pk>/<str:source>/", views.edit_contact, name="edit_contact"),
    path("delete/<int:pk>/<str:source>/", views.delete_contact, name="delete_contact"),

]

