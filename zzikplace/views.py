from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from .models import Place, Review, Like, Save, SearchWord
from django.contrib.auth.models import User
from django.db.models import Count
import math
from math import radians, cos, sin, asin, sqrt

def index(request):
    return render(request, 'zzikplace/index.html')

def around(request):
    all = Place.objects.all()
    user_place = Place.objects.last()

    places = get_near_me(user_place.x, user_place.y)
    print(places)

    return render(request, 'zzikplace/around.html', { 'places' : places })

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
        place = Place.objects.get(id=id)

        queryset = Review.objects.all().filter(place_id=id)
        
        a_number = queryset.filter(time="A").count()
        b_number = queryset.filter(time="B").count()
        c_number = queryset.filter(time="C").count()
        d_number = queryset.filter(time="D").count()
        e_number = queryset.filter(time="E").count()
        timelist = [a_number, b_number, c_number, d_number, e_number]
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
        return render(request, 'zzikplace/detail.html', {'place':place, 'timelist': timelist, 'first_around': first_around, 'first_dist': first_dist, 'second_around': second_around, 'second_dist' : second_dist})

def add(request, id=None):
    if id:
        place = Place.objects.get(id=id)
        return render(request, 'zzikplace/add.html', {'place' : place})
    else:
        return render(request, 'zzikplace/new.html')



def places(request):
    places = Place.objects.all()
    # featured = []
    # for place in places:
    #     # if place.saved_users.count() > 0:
    #         featured.append(place)
    
    sort = request.GET.get('sort', '')
    if sort == 'saves':
        # saves = {}
        # saved_list = []
        # for place in places:
        #     saves.update({ place : place.saved_users.count()})
        # saves_dict =  (sorted(saves.items(), key=lambda kv: kv[1], reverse=True))
        # for item in saves_dict:
        #     saved_list.append(item[0])
        saved_list = Place.objects.annotate(saved_count = Count('saved_users')).order_by('-saved_count')
        return render(request, 'zzikplace/places.html', { 'places': saved_list })
    elif sort == 'views':
        places = Place.objects.order_by('-place_hit', '-created_at')

        return render(request, 'zzikplace/places.html', {'places': places })
    else: 
        return render(request, 'zzikplace/places.html', { 'places': places })

def my(request):
    places = Place.objects.filter(saved_users = request.user)
    return render(request, 'zzikplace/my.html', {'places' : places})

def myposts(request):
    reviews = Review.objects.filter(author = request.user)
    return render(request, 'zzikplace/myposts.html', {'reviews' : reviews})

def myposts_delete(request, id):
    review = Review.objects.get(id=id)
    place = review.place
    review.delete()
    if place.review_set.count == 0:
        place.delete()
    return redirect('/reviews/myposts')
    
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

def place_unsave(request, pk):
    place = Place.objects.get(id = pk)
    place.delete()
    return redirect('/reviews/my') 

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
        dist = haversine(x,y, place.x, place.y)
        if dist <= 10:
            dist_list[place] = round(dist,2)
    arounds = sorted(dist_list.items(), key=lambda kv: kv[1])
    return arounds
    # 10km 이하, 거리순 


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def findplace(request):
    if request.method == 'POST':
        searchword = request.POST['search-word']
  
        places = Place.objects.all()
        tag_places = []
        for place in places:
            if place.tag_set.filter(name__contains = searchword):
                tag_places.append(place)
            elif searchword in place.address:
                tag_places.append(place)
        return render(request, 'zzikplace/findplace.html', {'searchword' : searchword, 'places' : tag_places})