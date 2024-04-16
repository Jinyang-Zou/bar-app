"""
URL configuration for bar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("bar_app.urls.auth")),
    path("api/references/", include("bar_app.urls.references")),
    path("api/bars/", include("bar_app.urls.bars")),
    path("api/stocks/", include("bar_app.urls.stocks")),
    path("api/stat/", include("bar_app.urls.statistiques")),
    path("api/orders/", include("bar_app.urls.orders")),
]
