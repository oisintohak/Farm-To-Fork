from django.urls import path
from .views import ProfileDelete, ProfileEditView, ProfileView, FarmerMapView

urlpatterns = [
    path('farmer-map', FarmerMapView.as_view(), name='farmer-map'),
    path('detail/<id>', ProfileView.as_view(), name='profile'),
    path('edit', ProfileEditView.as_view(), name='profile-edit'),
    path('delete/<pk>/', ProfileDelete.as_view(), name='profile-delete'),

]
