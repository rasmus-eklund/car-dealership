from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:car_id>', views.car_detail, name='car'),
    path('form/<str:form_type>/', views.admin_forms, name='admin_forms'),
    path('edit/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('car/delete_image/<int:image_id>/',
         views.delete_car_image, name='delete_car_image'),
    path('add_car/', views.add_car, name='add_car'),
    path('reserve/<int:car_id>/', views.reserve_car, name='reserve_car'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]
