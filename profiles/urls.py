from django.urls import path
from .views import ProfileEditView, ProfileView

urlpatterns = [
    path('profile/<username>/', ProfileView.as_view(), name='profile'),
    path('edit-profile/<username>/',
         ProfileEditView.as_view(), name='edit-profile'),
]
