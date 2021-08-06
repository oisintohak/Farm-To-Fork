from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import Group
from django.urls import reverse


from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model to store address information
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
    phone_number = models.CharField(max_length=20,
                                    null=True, blank=True)
    street_address1 = models.CharField(max_length=80,
                                       null=True, blank=False)
    street_address2 = models.CharField(max_length=80,
                                       null=True, blank=False)
    town_or_city = models.CharField(max_length=40,
                                    null=True, blank=False)
    county = models.CharField(max_length=80,
                              null=True, blank=False)
    postcode = models.CharField(max_length=20,
                                null=True, blank=False)
    country = CountryField(blank_label='Country',
                           null=True, blank=False)
    latitude = models.DecimalField(
        max_digits=30, decimal_places=20, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=30, decimal_places=20, blank=True, null=True
    )
    location = PointField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'id': self.user.id})

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=auth.get_user_model())
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=auth.get_user_model())
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name=instance.user_type)
        instance.groups.add(group)


@receiver(pre_save, sender=UserProfile)
def generate_location(sender, instance, **kwargs):
    if instance.latitude and instance.longitude:
        location = Point(
            float(instance.longitude),
            float(instance.latitude)
        )
        instance.location = location
