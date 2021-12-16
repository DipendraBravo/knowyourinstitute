"""newsportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from home import views as home_views
from users import views as user_views

urlpatterns = [
    path('personal/', home_views.personal, name='personal'),
    path('admin/', admin.site.urls),
    path('', home_views.index, name ='home'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('edit/',home_views.edit, name='edit'),
    path('submitSource/', home_views.submit_source, name='submitSource'),
    path('submitCategory/', home_views.submit_category, name='submitCategory'),
    path('searchQuery/', home_views.search, name='search'),
    path('pricing/', home_views.pricing, name='pricing'),
    path('source/',home_views.source_selected, name='source_selected'),
    path('categorySelected', home_views.category_selected, name='category_selected'),
    path('languageSelected/',home_views.language_selected, name='languageSelected'),
    path('unauthpricing/',home_views.unauth_pricing, name='unauth_pricing'),
]
