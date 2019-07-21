from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save  # 추가
from django.dispatch import receiver  
from django.utils import timezone

# class Profile(models.Model):   # 추가
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.CharField(max_length=30, blank=True)

#     def __str__(self):   # 추가
#         return 'id=%d, user id=%d, email=%s' % (self.id, self.user.id, self.email)

class Place(models.Model):
    title = models.CharField(max_length=256)
    address = models.TextField()
    saved_users = models.ManyToManyField(User, blank=True, related_name='places_saved', through='Save')
    
class Review(models.Model):
    TIME_CHOICES = (
        ('A', '해 뜰 무렵'),
        ('B', '한낮'),
        ('C', '해 질 무렵'),
        ('D', '밤'),
        ('E', '시간이 상관 없어요'),
    )
    
    place = models.ForeignKey(Place, on_delete = models.CASCADE)
    tip = models.TextField()
    author = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    liked_users = models.ManyToManyField(User, blank=True, related_name='reviews_liked', through='Like')
    photo = models.ImageField(upload_to='review_photos')
    time = models.CharField(max_length=1, choices=TIME_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):  
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):  
#     instance.profile.save()
