from django.contrib import admin
from .models import Place
from .models import Review, Tag

class ReviewInline(admin.TabularInline):
    model = Review



class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'address']
    inlines = [
        ReviewInline,
    ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_place_id', 'get_place_name', 'tip', 'author']

    def get_place_name(self, obj):
        return obj.place.title
    get_place_name.short_description = 'place_name'

    def get_place_id(self, obj):
        return obj.place.id
    get_place_id.short_description = 'place_id'


admin.site.register(Place, PlaceAdmin)
admin.site.register(Review, ReviewAdmin)
# Register your models here.
