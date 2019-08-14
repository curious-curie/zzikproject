from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from .models import Place, Review, Like, Save
from django.contrib.auth.models import User
import math

def index(request):
    return render(request, 'zzikplace/index.html')

def around(request):
    return render(request, 'zzikplace/index.html')



def new(request):
    return render(request, 'zzikplace/new.html')

def detail(request, id=None):
    if request.method == "POST":
        title = request.POST['place_name']
        address = request.POST['place_addr']
        x = request.POST['place_x']
        y = request.POST['place_y']
        tip = request.POST['tip']
        photo = request.FILES.get('photo', False)
        time = request.POST['time']
        tag_content = request.POST['tag_content']
        if Place.objects.filter(address = address):
            place = Place.objects.get(address = address)
            print(place)
            place.tag_content += tag_content
        else:
            place, is_place =  Place.objects.get_or_create(address=address, tag_content = tag_content, title=title, x= x, y= y)
        id = place.id
        place.save()
        place.tag_save()
        review = Review.objects.create(place_id=id, tip=tip, tag_content = tag_content, photo=photo, time=time, author=request.user)
        review.save()
        return redirect('/reviews/detail/' + str(id))

    elif request.method == "GET":
        # place = Place.objects.get(id=id)
        # arounds  = place.get_around()
        # first_around = arounds[1]
        # second_around = arounds[2]
        # return render(request, 'zzikplace/detail.html', {'place':place, 'first_around': first_around, 'second_around':second_around})
        place = Place.objects.get(id=id)
        arounds = place.get_around()
        if len(arounds) < 3:
            first_around = place
            second_around = place
            first_dist = 0
            second_dist = 0
        else:
            first_around = arounds[1][0]
            first_dist = arounds[1][1]
            second_around = arounds[2][0]
            second_dist = arounds[2][1]
        return render(request, 'zzikplace/detail.html', {'place':place, 'first_around': first_around, 'first_dist': first_dist, 'second_around': second_around, 'second_dist' : second_dist})

def add(request, id=None):
    if id:
        place = Place.objects.get(id=id)
        return render(request, 'zzikplace/add.html', {'place' : place})
    else:
        return render(request, 'zzikplace/new.html')



def places(request):
    places = Place.objects.all()
    return render(request, 'zzikplace/places.html', { 'places': places })

def my(request):
    places = Place.objects.filter(saved_users = request.user)
    return render(request, 'zzikplace/my.html', {'places' : places})

def myposts(request):
    reviews = Review.objects.get(author = request.user)
    return render(request, 'zzikplace/myposts.html', {'reviews' : reviews})

def place_save(request, pk):
    place = Place.objects.get(id = pk)
    save_list = place.save_set.filter(user_id = request.user.id)
    if save_list.count() > 0:
        place.save_set.get(user_id = request.user.id).delete()
    else:
        Save.objects.create(user_id = request.user.id, place_id = place.id)
    next = request.META['HTTP_REFERER']
    return redirect (next)

def review_like(request, pk):
    review = Review.objects.get(id = pk)
    like_list = review.like_set.filter(user_id = request.user.id)
    if like_list.count() > 0:
        review.like_set.get(user_id = request.user.id).delete()
    else:
        Like.objects.create(user_id = request.user.id, review_id = review.id)
    next = request.META['HTTP_REFERER']
    return redirect (next)

def tag_list(request, tag):
    places = Place.objects.all()
    tag_places = []
    for place in places:
        if place.tag_set.filter(name__contains = tag):
            tag_places.append(place)
        elif tag in place.address:
            tag_places.append(place)
    return render(request, 'zzikplace/tags.html', {'places' : tag_places})



def get_near_me(x, y):
    dist_list = {}
    places = Place.objects.all()
    for place in places:
        dist = distance(x,y, place)
        if dist <= 10:
            dist_list[place] = dist
    arounds = sorted(dist_list.items(), key=lambda kv: kv[1])
    d = dict(arounds)
    near_me = list(d.keys())
    return near_me
    # 10km 이하, 거리순 

def distance(x,y, obj):
    radius = 6371 # FAA approved globe radius in km

    dlat = math.radians(x-obj.x)
    dlon = math.radians(y-obj.y)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(obj.x)) \
        * math.cos(math.radians(x)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return int(math.floor(d))

