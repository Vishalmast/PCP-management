from django.urls import path, include

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    
    path('addInfo',addInfo,name='addInfo'),
    path('lists',lists,name='lists'),
    path('diss',dissatisfy, name='diss'),
    path('profile', profile, name = 'profile'),
    path('book', book, name= 'book'),
    path('address', address, name='address'),
    path('addview',addview, name='addview'),
    path('ins',ins, name='ins'),
    path('go',go, name='go'),
    path('schedule',schedule, name='schedule'),
    path('satisfaction_check', satisfaction_check, name = "satisfaction_check"),
    path('doctor_change', doctor_change, name="doctor_change"),
]