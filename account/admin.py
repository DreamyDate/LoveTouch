from modeltranslation.admin import TranslationAdmin
from .models import StatusFavorite
from django.contrib import admin
from .models import (Profile, SocialLink, Status, StatusComment, StatusLike, 
                     MenuItem, BlockedIP, CreditTransaction, PremiumPackage, 
                     PremiumPurchase, StatusFavorite, LanguageModel, Position)


from django.contrib.admin.widgets import FilteredSelectMultiple


class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('friends', 'liked_by', 'viewers','followers', 'blocked_users')
    list_display = ['user', 'age', 'gender',
                    'relationship_goals', 'weight', 'credits']
    actions = ['make_premium', 'verify_photos']


    def make_premium(self, request, queryset):
        for profile in queryset:
            profile.make_premium()
    make_premium.short_description = "Сделать выбранные профили премиум"

    def verify_photos(self, request, queryset):
        for profile in queryset:
            profile.verify_photo()
    verify_photos.short_description = "Верифицировать фото выбранных профилей"

admin.site.register(Profile, ProfileAdmin)
# SocialLink
@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'facebook', 'twitter', 'instagram')

# Status
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'creation_date')
    list_filter = ('type',)

# StatusComment
@admin.register(StatusComment)
class StatusCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_date')

# StatusLike
@admin.register(StatusLike)
class StatusLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_date')

# MenuItem
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'enabled')
    list_display_links = ('url',)

# BlockedIP
@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'date_blocked')

# CreditTransaction
@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'date')
    list_filter = ('transaction_type',)

# PremiumPackage
@admin.register(PremiumPackage)
class PremiumPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration')

# PremiumPurchase
@admin.register(PremiumPurchase)
class PremiumPurchaseAdmin(admin.ModelAdmin):
    list_display = ('profile', 'package', 'purchase_date', 'expiry_date')


@admin.register(StatusFavorite)
class StatusFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at')
    search_fields = ('user__username', 'status__type', 'status__id')


@admin.register(LanguageModel)
class LanguageModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


class MenuItemAdmin(TranslationAdmin):
    pass




