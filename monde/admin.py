from django.contrib import admin
from .models import ClothingItem, User,UserProfile, Sections, UserOwnedItems,CartItems,Review

class UserProfileInline(admin.StackedInline):
    model=UserProfile
    can_delete=False
    
class UserAdmin(admin.ModelAdmin):
    inlines=(UserProfileInline,)

#Order by created_at in descending order    
class ReviewAdmin(admin.ModelAdmin):
    ordering=('-created_at',)
    
# Register your models here.
admin.site.register(ClothingItem)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(UserOwnedItems)
admin.site.register(CartItems)
admin.site.register(Sections)
admin.site.register(Review,ReviewAdmin)

