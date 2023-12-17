from django import forms

class CustomDecimalField(forms.DecimalField):
    def to_python(self, value):
        # Заменить запятую на точку перед валидацией
        if isinstance(value, str):
            value = value.replace(',', '.')
        return super().to_python(value)
