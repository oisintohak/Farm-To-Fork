from django.db import models
from django.contrib.gis.geos import Point
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import Group
from django.urls import reverse

from checkout.models import Address


class UserProfile(models.Model):
    """
    A user profile model to store user information
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=40,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=40,
        null=True,
    )
    phone_number = models.CharField(
        max_length=20, null=True, blank=False, default=None)
    address = models.OneToOneField(
        'checkout.Address',
        on_delete=models.SET_NULL,
        related_name='profile',
        blank=True,
        null=True,
    )
    bio = models.TextField(max_length=3000, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'id': self.request.user.id})

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.user:
            self.user.delete()


@receiver(post_save, sender=auth.get_user_model())
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
        instance.profile.save()
    if created:
        Address.objects.create(profile=instance.profile)
        instance.profile.address.save()


@receiver(post_save, sender=auth.get_user_model())
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if not instance.user_type:
            instance.user_type = 'Farmer'
        group = Group.objects.get(name=instance.user_type)
        instance.groups.add(group)


@receiver(pre_save, sender=Address)
def generate_location(sender, instance, **kwargs):
    if instance.latitude and instance.longitude:
        location = Point(
            float(instance.longitude),
            float(instance.latitude)
        )
        instance.location = location
