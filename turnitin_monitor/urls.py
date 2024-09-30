from django.contrib import admin
from django.urls import path
from slots import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.slot_list, name='slot_list'),
    path('inactive-slots/', views.inactive_slots, name='inactive_slots'),
]
