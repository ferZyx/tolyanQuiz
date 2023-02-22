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
    path('mytests/', login_required(mytests_view), name='mytests'),
    path('upload_docx/', login_required(upload_docx), name='upload_docx'),
    path('test-config/<file_pk>', login_required(test_config), name='test-config'),
    path('test-view/<test_id>', login_required(testing_page), name='test-view'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
