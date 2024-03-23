from django.contrib import admin

admin.site.index_title = "Administration"
# admin.site.index_template = "index.html"

from .models import Booking, Menu, Category, Feedback, FeedImage, MenuImage

admin.site.register(Menu)
admin.site.register(Booking)
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(FeedImage)
admin.site.register(MenuImage)
