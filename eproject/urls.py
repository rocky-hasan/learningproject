from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth import views as auth_view
from core.forms import SignupForm, LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    path('courses/', views.courses, name='courses'),
    path('course/<id>/', views.course, name='course'),

    path('contact/', views.Contact.as_view(), name='contact'),
    path('profile/', views.profile, name='profile'),
    path('profileupdate/<int:id>/', views.profileupdate, name='profileupdate'),
    path('attendance/', views.attendance, name='attendance'),
    path('enroll/', views.enroll, name='enroll'),

   #_________authentication_______

    path('signup/', views.Signup.as_view(), name='signup'),
    path('signin/', auth_view.LoginView.as_view(template_name='signin.html', authentication_form=LoginForm), name='signin'),
    path('logout/', auth_view.LogoutView.as_view(next_page='signin'), name='logout'),
    path('reset_pass/', views.reset_pass, name='reset_pass'),

    path('accounts/', include('allauth.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
