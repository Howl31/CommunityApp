from django.urls import path
from . import views

urlpatterns = [
    path('', views.navigate, name='navigate'),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('services', views.services, name='services'),
    path('add_service', views.add_service, name='add_service'),
    path('queries', views.queries, name='queries'),
    path('ask_question', views.ask_question, name='ask_question'),
    path('discussion/<int:pk>', views.discussion, name='discussion'),
    path('contact', views.contact, name='contact'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin/admin_panel', views.admin_panel, name='admin_panel'),
    path('admin/users', views.users, name='users'),
    path('admin/user_details/<int:pk>', views.user_details, name='user_details'),
    path('admin/del_service/<int:pk>', views.del_service, name='del_service'),
    path('admin/change_sts/<int:pk>', views.change_sts, name='change_sts'),
    path('admin/admin_queries', views.admin_queries, name='admin_queries'),
]