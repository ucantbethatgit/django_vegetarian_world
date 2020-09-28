from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vegetables/', views.VegetableListView.as_view(), name='vegetables'),
    path('vegetable/<int:pk>', views.VegetableDetailView.as_view(), name='vegetable-detail'),
    path('farmers/', views.FarmerListView.as_view(), name='farmers'),
    path('farmer/<int:pk>', views.FarmerDetailView.as_view(), name='farmer-detail'),
]

urlpatterns += [   
    path('myvegetables/', views.LoanedVegetablesByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [   
    path('vegetable/<uuid:pk>/renew/', views.renew_vegetable_agrarian, name='renew-vegetable-agrarian'),
]

urlpatterns += [  
    path('farmer/create/', views.FarmerCreate.as_view(), name='farmer_create'),
    path('farmer/<int:pk>/update/', views.FarmerUpdate.as_view(), name='farmer_update'),
    path('farmer/<int:pk>/delete/', views.FarmerDelete.as_view(), name='farmer_delete'),
]