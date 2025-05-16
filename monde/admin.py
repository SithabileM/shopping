from django.contrib import admin
from .models import ClothingItem, User,UserProfile, Sections, UserOwnedItems,CartItems,Review, ClothingItemAdminForm
from .utils.imagekit import upload_to_imagekit

class UserProfileInline(admin.StackedInline):
    model=UserProfile
    can_delete=False
    
class UserAdmin(admin.ModelAdmin):
    inlines=(UserProfileInline,)

#Order by created_at in descending order    
class ReviewAdmin(admin.ModelAdmin):
    ordering=('-created_at',)
    
class ClothingItemAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        form= ClothingItemAdminForm
        if 'image_file' in request.FILES:
            image= request.FILES['image_file']
            response=upload_to_imagekit(image)
            obj.image_url=response.get('url')
            super().save_model(request, obj, form, change)
    
# Register your models here.
admin.site.register(ClothingItem, ClothingItemAdmin)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(UserOwnedItems)
admin.site.register(CartItems)
admin.site.register(Sections)
admin.site.register(Review,ReviewAdmin)



