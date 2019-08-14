from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save  # 추가
from django.dispatch import receiver  
from django.utils import timezone
import re, cmath, math

# class Profile(models.Model):   # 추가
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.CharField(max_length=30, blank=True)

#     def __str__(self):   # 추가
#         return 'id=%d, user id=%d, email=%s' % (self.id, self.user.id, self.email)

class Place(models.Model):
    title = models.CharField(max_length=256)
    address = models.TextField()
    x = models.FloatField(default = None)
    y = models.FloatField(default = None)
    saved_users = models.ManyToManyField(User, blank=True, related_name='places_saved', through='Save')
    tag_content = models.TextField()
    tag_set = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    place_hit = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.tag_content)

        if not tags:
            return
        
        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(name=t)
            self.tag_set.add(tag)
    
    def get_tags(self):
        return ",".join([str(p) for p in self.tag_set.all()])

    def haversine_distance(self, obj):
        radius = 6371 # FAA approved globe radius in km
    
        dlat = math.radians(self.x-obj.x)
        dlon = math.radians(self.y-obj.y)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(obj.x)) \
            * math.cos(math.radians(self.x)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
    
        # Return distance in km
        return int(math.floor(d))
    
    def get_around(self):
        dist_list = {}
        places = Place.objects.all()
        for place in places:
            dist = self.haversine_distance(place)
            dist_list[place] = dist
        arounds = sorted(dist_list.items(), key=lambda kv: kv[1])
        d = dict(arounds)
        sorted_places = list(d.keys())
        # return sorted_places
        return arounds
        # 거리순으로 나열된 장소명 리스트 


    @property
    def update_counter(self):
        self.place_hit = self.place_hit + 1
        self.save()

class Tag(models.Model):
    name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name

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
    tag_content = models.TextField(blank=True)
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


class SearchWord(models.Model):
    searchword = models.CharField(max_length=30, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):  
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):  
#     instance.profile.save()
