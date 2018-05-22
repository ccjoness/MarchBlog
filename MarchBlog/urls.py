"""MarchBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views as b_views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'blogs', b_views.BlogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', b_views.home, name='home'),
    path('b/<slug:b_slug>/', b_views.single_blog, name='single_blog'),
    # re_path('b/(?P<slug>[-\w]+)/', b_views.single_blog, name='single_blog'),


    path('login/', b_views.login_view, name='login'),
    path('logout/', b_views.logout_view, name='logout'),
    path('register/', b_views.register, name='register'),

    path('api/username-validator/', b_views.username_validator, name='username_validator'),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
