from django import forms
from account.models import Profile, LanguageModel


class ProfileFilterForm(forms.Form):
    GENDER_CHOICES = [
        ('', '-----'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    RELATIONSHIP_GOALS_CHOICES = [
        ('', '-----'),
        ('F', 'Friendship'),
        ('D', 'Dating'),
        ('R', 'Relationship'),
        ('N', 'Networking'),
    ]

    RADIUS_CHOICES = [
        (None, '-----'),
        (25, '25 km'),
        (50, '50 km'),
        (100, '100 km'),
        (150, '150 km'),
        (200, '200 km'),
        ('country', 'Country-wide'),
    ]
    SMOKING_CHOICES = [
        (None, '-----'),
        ('Y', 'Yes'),
        ('N', 'No'),
        ('O', 'Occasionally'),
    ]

    PHYSIQUE_CHOICES = [
        (None, '-----'),
        ('Ec', 'Ectomorph'),
        ('M', 'Mesomorph'),
        ('En', 'Endomorph'),
    ]

    tatu_choices = [
        (None, '-----'),
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    piercing_choices = [
        (None, '-----'),
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    scars_choices = [
        (None, '-----'),
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    # Знак зодіаку
    ZODIAC_SIGN_CHOICES = [

        (None, '-----'),
        ('Ca', 'Capricorn'),
        ('Aq', 'Aquarius'),
        ('Pi', 'Pisces'),
        ('Ar', 'Aries'),
        ('Ta', 'Taurus'),
        ('Ge', 'Gemini'),
        ('Can', 'Cancer'),
        ('Le', 'Leo'),
        ('Vi', 'Virgo'),
        ('Li', 'Libra'),
        ('Sc', 'Scorpio'),
        ('Op', 'Ophiuchus'),
        ('Sa', 'Sagittarius')

    ]

    SEXUAL_ORIENTATION_CHOICES = [
        (None, '-----'),
        ('H', 'Hetero'),
        ('G', 'Gay'),
        ('L', 'Lesbian'),
        ('B', 'Bisexual'),
        ('A', 'Asexual'),
        ('D', 'Demisexual'),
        ('P', 'Pansexual'),
        ('Q', 'Queer'),
        ('S', 'Still searching')
    ]

    RELATIONSHIP_STATUS_CHOICES = [
        (None, '-----'),
        ('F', 'Free'),
        ('A', 'Attitudes'),
        ('E', 'Everything is difficult'),
        ('F', 'Free relationship')
    ]

    # Діти
    CHILDREN_CHOICES = [
        (None, '-----'),
        ('S', 'Sometime in the future'),
        ('Iw', 'I want soon'),
        ('D', 'Do not want'),
        ('Ia', 'I already have children')

    ]

    # Рівень освіти
    EDUCATION_LEVEL_CHOICES = [
        (None, '-----'),
        ('A', 'Average'),
        ('H', 'Higher'),
        ('Ia', "I am studying for a master's degree"),
        ('Is', 'I study in college'),
        ('B', 'Bachelor'),
        # Добавьте другие варіанти по мере необхідності
    ]

    # Тип особистості
    PERSONALITY_TYPE_CHOICES = [
        (None, '-----'),
        ('I', 'Introvert'),
        ('E', 'Extrovert'),
        # Добавьте другие варианты по мере необходимости
    ]

    # Работа и образование
    WORK_EDUCATION_CHOICES = [
        (None, '-----'),
        ('S', 'Student'),
        ('E', 'Employee'),
        ('U', 'Unemployed'),
        # Добавьте другие варианты по мере необходимости
    ]

    # Тварини
    ANIMALS_CHOICES = [
        (None, '-----'),
        ('C', 'Cat/cats'),
        ('D', 'Dog/dogs'),
        ('CD', 'Cats and dogs'),
        ('O', 'Other animals'),
        ('N', 'No animals'),

        # Добавьте другие варианты по мере необходимости
    ]

    # Релігія
    RELIGION_CHOICES = [
        (None, '-----'),
        ('Ag', 'Agnosticism'),
        ('At', 'Atheism'),
        ('Bu', 'Buddhism'),
        ('Ca', 'Catholicism'),
        ('Ch', 'Christianity'),
        ('H', 'Hinduism'),
        ('Ja', 'Jainism'),
        ('JU', 'Judaism'),
        ('M', 'Mormonism'),
        ('I', 'Islam'),
        ('Z', 'Zoroastrianism'),
        ('Si', 'Sikhism'),
        ('Sp', 'Spiritualism'),

        # Добавьте другие варианты по мере необходимости
    ]

    ALCOHOL_CHOICES = [
        (None, '-----'),
        ('Y', 'Yes'),
        ('N', 'No, I do not drink'),
        ('O', 'Occasionally'),
        ('Of', 'Often'),
        ('N', 'Never'),
        ('In', 'In the company'),

    ]

    search_gender = forms.MultipleChoiceField(
        choices=GENDER_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Gender"
    )
    search_smoking = forms.MultipleChoiceField(
        choices=SMOKING_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Smoking"
    )
    search_age_from = forms.IntegerField(
        min_value=0, required=False, label="Age from")
    search_age_to = forms.IntegerField(
        min_value=0, required=False, label="Age to")
    search_goals = forms.ChoiceField(
        choices=RELATIONSHIP_GOALS_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.RadioSelect,
        required=False,
        label="Relationship Goals"
    )

    search_city = forms.CharField(max_length=255, required=False, label="City")
    search_country = forms.CharField(
        max_length=255, required=False, label="Country")
    search_radius = forms.ChoiceField(
        choices=RADIUS_CHOICES, required=False, label="Radius")
    current_latitude = forms.FloatField(
        widget=forms.HiddenInput(), required=False)
    current_longitude = forms.FloatField(
        widget=forms.HiddenInput(), required=False)

    language_choices = LanguageModel.objects.values_list('id', 'name')
    LANGUAGES_CHOICES = [(str(id), language_name)
                         for id, language_name in language_choices]

    search_languages = forms.MultipleChoiceField(
        choices=LANGUAGES_CHOICES,  # включаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Languages"
    )

    search_physique = forms.MultipleChoiceField(
        choices=PHYSIQUE_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Physique"
    )

    search_personality_type = forms.MultipleChoiceField(
        choices=PERSONALITY_TYPE_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Personality type"
    )

    search_relationship_status = forms.MultipleChoiceField(
        choices=RELATIONSHIP_STATUS_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Relationship status"
    )

    search_sexual_orientation = forms.MultipleChoiceField(
        choices=SEXUAL_ORIENTATION_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Sexual orientation"
    )

    search_children = forms.MultipleChoiceField(
        choices=CHILDREN_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Children"
    )

    search_alcohol = forms.MultipleChoiceField(
        choices=ALCOHOL_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Alcohol"
    )

    search_tatu = forms.MultipleChoiceField(
        choices=tatu_choices[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tatu"
    )

    search_piercing = forms.MultipleChoiceField(
        choices=piercing_choices[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Piercing"
    )

    search_scars = forms.MultipleChoiceField(
        choices=scars_choices[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Scars"
    )

    search_zodiac_sign = forms.MultipleChoiceField(
        choices=ZODIAC_SIGN_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Zodiac sign"
    )

    search_animals = forms.MultipleChoiceField(
        choices=ANIMALS_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Animals"
    )

    search_religion = forms.MultipleChoiceField(
        choices=RELIGION_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Religion"
    )

    search_education_level = forms.MultipleChoiceField(
        choices=EDUCATION_LEVEL_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Education level"
    )

    search_work_and_education = forms.MultipleChoiceField(
        choices=WORK_EDUCATION_CHOICES[1:],  # исключаем пустой выбор
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Work and education"
    )


