from modeltranslation.translator import TranslationOptions, translator
from .models import MenuItem


class MenuItemTranslationOptions(TranslationOptions):
    fields = ('title',)  # Add other fields as needed


translator.register(MenuItem, MenuItemTranslationOptions)


