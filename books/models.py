from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    published_year = models.CharField(max_length=4)  # หรือใช้ DateField ถ้าคุณต้องการเก็บเป็นปี
    num_pages = models.IntegerField(null=True, blank=True)  # ฟิลด์สำหรับจำนวนหน้า
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # ฟิลด์ที่เพิ่มใหม่
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()