
from django.contrib import admin
from django.urls import path
from shorty import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Serve index.html at the root URL
    path('shorten', views.ShortenAPIView.as_view(), name='shorten_url'),
    path('lengthen', views.LengthenAPIView.as_view(), name='lengthen_url'),
]
