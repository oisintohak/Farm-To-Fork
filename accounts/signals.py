from django.contrib.auth.models import Group


def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name=instance.user_type)
        instance.groups.add(group)
