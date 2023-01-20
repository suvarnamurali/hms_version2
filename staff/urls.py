from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('home', views.staff_home, name='staff_home'),
    path('register',views.registration,name = 'register'),
    path('appointment/', views.appointments, name='appointment'),
    path('patient_search/', views.patient_search, name='patient-search'), 
    path('staff/', views.staff_list, name = 'staff-list'),
    path('profile/', views.profile, name="staff-prof"),
    path('logout/',views.log_out,name = 'logout')
]
