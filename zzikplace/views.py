from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from .models import Place, Review, Like, Save
from django.contrib.auth.models import User

def index(request):
    return render(request, 'zzikplace/index.html')

def around(request):
    return render(request, 'zzikplace/index.html')

def my(request):
    places = Place.objects.filter(saved_users = request.user)
    print(places)
    return render(request, 'zzikplace/my.html', {'places' : places})

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
        #arounds  = place.get_around()
        #first_around = arounds[1]
        #second_around = arounds[2]
        # d = dict(arounds)
        # sorted_places = list(d.keys())
        # first_around = sorted_places[1]
        # second_around = sorted_places[2]
        return render(request, 'zzikplace/detail.html', {'place':place, 'timelist': timelist})


def add(request, id=None):
    if id:
        place = Place.objects.get(id=id)
        return render(request, 'zzikplace/add.html', {'place' : place})
    else:
        return render(request, 'zzikplace/new.html')




def places(request):
    places = Place.objects.all()
    return render(request, 'zzikplace/places.html', { 'places': places })

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