# All of extra functions required in views will be written here.
# 'util' stands for utility.

from .models import *

def add_category(request, listing):
    if len(request.POST["category"]) > 0:
        my_temp_object = Category.objects.create(category_name=str(request.POST["category"]))
    if my_temp_object in Category.objects.all():
        my_temp_object.delete()
        listing.category.add(Category.objects.get(category_name=str(request.POST["category"])))
    else:
        listing.category.add(my_temp_object)