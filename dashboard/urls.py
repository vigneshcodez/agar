from django.urls import path
from .views import business_list, business_create, business_edit, delete_business,index\

urlpatterns = [
    path('', index, name='dashboard_index'),
    path('business/', business_list, name='business_list'),
    path('business/create/', business_create, name='business_create'),
    path('business/edit/<int:id>/', business_edit, name='business_edit'),
    path('business/delete/<int:id>/', delete_business, name='business_delete'),
]
