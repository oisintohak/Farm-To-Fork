from django.urls import path
from .views import ProfileEditView, ProfileView, FarmerMapView

urlpatterns = [
    path('farmer-map', FarmerMapView.as_view(), name='farmer-map'),
    path('detail/<id>', ProfileView.as_view(), name='profile'),
    path('edit', ProfileEditView.as_view(), name='profile-edit'),
]
