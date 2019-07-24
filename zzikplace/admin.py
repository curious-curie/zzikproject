from django.contrib import admin
from .models import Place
from .models import Review

class ReviewInline(admin.TabularInline):
    model = Review
    
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'address']
    inlines = [
        ReviewInline,
    ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'place', 'author','tip']


admin.site.register(Place, PlaceAdmin)
admin.site.register(Review, ReviewAdmin)
# Register your models here.
