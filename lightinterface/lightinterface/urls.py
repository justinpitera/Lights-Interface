from django.contrib import admin
from django.urls import path
from lightinterface import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('turn-on-light/', views.turn_on_lights, name='turn_on_lights'),
    path('turn-off-light/', views.turn_off_lights, name='turn_off_lights'),
    path('set_color/', views.set_color, name='set_color'),
]
