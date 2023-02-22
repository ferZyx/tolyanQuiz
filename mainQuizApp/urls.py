from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls,),
    path('', main_page, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('tests/', login_required(files_view), name='tests'),
    path('test_config/', login_required(test_view), name='test'),
    path('testing/<test_id>', login_required(testing_page), name='testing_page'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
