# All of extra functions required in views.py will be written here.
# 'util' stands for utility.

from .models import *

def add_category(request, listing):
    if len(request.POST["category"]) > 0:
        temp_category = str(request.POST["category"])
        try:
            listing.category.add(Category.objects.get(category_name=temp_category))
            # Does Not Exist Error may occur
        except:
            new_category = Category(category_name=temp_category)
            new_category.save()
            listing.category.add(new_category)


