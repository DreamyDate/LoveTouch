from ckeditor.fields import RichTextField  # Предполагается, что вы используете CKEditor
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.utils import timezone
from datetime import timedelta
from albums.models import Photo
from django.core.validators import MinValueValidator
from cities_light.models import Country, City
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    nickname = models.CharField(
        max_length=255, unique=True, blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/', blank=True, null=True)

    photo_cover = models.ImageField(
        upload_to='users_cover/%Y/%m/%d/', blank=True, null=True)

    age = models.PositiveIntegerField(blank=True, null=True)

    height = models.FloatField(
        validators=[MinValueValidator(0.0)], null=True, blank=True)
    weight = models.FloatField(
        validators=[MinValueValidator(0.0)], null=True, blank=True)

    # Gender and Orientation fields
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    # Relationship and Dating fields
    RELATIONSHIP_GOALS_CHOICES = [
        ('F', 'Friendship'),
        ('D', 'Dating'),
        ('R', 'Relationship'),
        ('N', 'Networking'),
    ]
    relationship_goals = models.CharField(
        max_length=1, choices=RELATIONSHIP_GOALS_CHOICES, blank=True)

    # Habits fields
    SMOKING_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
        ('O', 'Occasionally'),
    ]
    smoking = models.CharField(
        max_length=1, choices=SMOKING_CHOICES, blank=True)
    ALCOHOL_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No, I do not drink'),
        ('O', 'Occasionally'),
        ('Of', 'Often'),
        ('N', 'Never'),
        ('In', 'In the company'),

    ]
    alcohol = models.CharField(
        max_length=2, choices=ALCOHOL_CHOICES, blank=True)

    # Appearance fields
    PHYSIQUE_CHOICES = [
        ('Ec', 'Ectomorph'),
        ('M', 'Mesomorph'),
        ('En', 'Endomorph'),
    ]
    physique = models.CharField(
        max_length=2, choices=PHYSIQUE_CHOICES, blank=True)

    tatu_choices = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    tatu = models.CharField(
        max_length=1, choices=tatu_choices, blank=True, null=True)
    piercing_choices = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    piercing = models.CharField(
        max_length=1, choices=piercing_choices, blank=True, null=True)
    scars_choices = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    scars = models.CharField(
        max_length=1, choices=scars_choices, blank=True, null=True)

    # Category 5: Interests
    interests = models.TextField(blank=True)

    languages = models.ManyToManyField(
        'LanguageModel',  blank=True)

    # Знак зодіаку
    ZODIAC_SIGN_CHOICES = [

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
    zodiac_sign = models.CharField(
        max_length=3, choices=ZODIAC_SIGN_CHOICES, blank=True, null=True)

    SEXUAL_ORIENTATION_CHOICES = [
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
    sexual_orientation = models.CharField(
        max_length=1, choices=SEXUAL_ORIENTATION_CHOICES, blank=True, null=True)

    RELATIONSHIP_STATUS_CHOICES = [
        ('F', 'Free'),
        ('A', 'Attitudes'),
        ('E', 'Everything is difficult'),
        ('F', 'Free relationship')
    ]

    relationship_status = models.CharField(
        max_length=1, choices=RELATIONSHIP_STATUS_CHOICES, blank=True, null=True)

    school = models.CharField(max_length=255, blank=True, null=True)

    organization = models.CharField(max_length=255, blank=True, null=True)
    position = models.ForeignKey('Position', on_delete=models.CASCADE, null=True, blank=True)

    # Діти
    CHILDREN_CHOICES = [
        ('S', 'Sometime in the future'),
        ('Iw', 'I want soon'),
        ('D', 'Do not want'),
        ('Ia', 'I already have children')
        # Добавьте другие варианты по мере необходимости
    ]

    children = models.CharField(
        max_length=2, choices=CHILDREN_CHOICES, blank=True, null=True)
    
    # Рівень освіти
    EDUCATION_LEVEL_CHOICES = [
        ('A', 'Average'),
        ('H', 'Higher'),
        ('Ia', "I am studying for a master's degree"),
        ('Is', 'I study in college'),
        ('B', 'Bachelor'),
        # Добавьте другие варіанти по мере необхідності
    ]

    education_level = models.CharField(
        max_length=2, choices=EDUCATION_LEVEL_CHOICES, blank=True, null=True)
    
    # Тип особистості
    PERSONALITY_TYPE_CHOICES = [
        ('I', 'Introvert'),
        ('E', 'Extrovert'),
        # Добавьте другие варианты по мере необходимости
    ]
    personality_type = models.CharField(
        max_length=1, choices=PERSONALITY_TYPE_CHOICES, blank=True, null=True)

    hair_color = models.CharField(max_length=255, blank=True, null=True)
    eye_color = models.CharField(max_length=255, blank=True, null=True)
    

    # Работа и образование
    WORK_EDUCATION_CHOICES = [
        ('S', 'Student'),
        ('E', 'Employee'),
        ('U', 'Unemployed'),
        # Добавьте другие варианты по мере необходимости
    ]
    work_and_education = models.CharField(
        max_length=255, choices=WORK_EDUCATION_CHOICES, blank=True, null=True)

    # Тварини
    ANIMALS_CHOICES = [
        ('C', 'Cat/cats'),
        ('D', 'Dog/dogs'),
        ('CD', 'Cats and dogs'),
        ('O', 'Other animals'),
        ('N', 'No animals'),

        # Добавьте другие варианты по мере необходимости
    ]
    animals = models.CharField(
        max_length=2, choices=ANIMALS_CHOICES, blank=True, null=True)

    # Релігія
    RELIGION_CHOICES = [
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
    religion = models.CharField(
        max_length=255, choices=RELIGION_CHOICES, blank=True, null=True)

    # Location fields
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)
    credits = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)

    notifications_enabled = models.BooleanField(default=True)
    language = models.CharField(max_length=2, choices=(
        ('en', 'English'), ('ru', 'Russian')), default='ru', blank=True)
    timezone = models.CharField(max_length=50, default='UTC', blank=True)

    followers = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='following_set')

    friends = models.ManyToManyField('self', blank=True)

    liked_by = models.ManyToManyField(
        User, related_name='liked_profiles', blank=True)

    viewers = models.ManyToManyField(
        User, related_name='viewed_profiles', blank=True)
    blocked_users = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='blocked_by')

    is_blocked = models.BooleanField(default=False)
    reason_for_blocking = models.TextField(blank=True, null=True)
    night_mode = models.BooleanField(default=False)

    photo_verified = models.BooleanField(default=False)
    photo_verification_requested = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def add_to_blacklist(self, user_to_block):
        self.blocked_users.add(user_to_block)

    def remove_from_blacklist(self, user_to_unblock):
        self.blocked_users.remove(user_to_unblock)

    def is_blocked_user(self, user_to_check):
        return self.blocked_users.filter(id=user_to_check.id).exists()

    def get_favorite_photos(self):
        return Photo.objects.filter(favorites__user=self.user)

    def add_viewer(self, user):
        """
        Добавить пользователя в список просмотров профиля.
        """
        self.viewers.add(user)

    def add_friend(self, user):
        """
        Добавить пользователя в список друзей и избранных контактов.
        """
        self.friends.add(user)

    def add_like(self, user):
        """
        Добавить лайк от пользователя к профилю.
        """
        self.liked_by.add(user)

    def remove_like(self, user):
        """
        Убрать лайк от пользователя к профилю.
        """
        self.liked_by.remove(user)

    def has_like_from(self, user):
        """
        Проверить, есть ли лайк от указанного пользователя к профилю.
        """
        return self.liked_by.filter(id=user.id).exists()

    def __str__(self):
        return f'Profile of {self.user.username}'

    def remove_friend(self, profile):
        self.friends.remove(profile)
        profile.friends.remove(self)

    def follow(self, profile):
        self.following_set.add(profile)

    def unfollow(self, profile):
        self.following_set.remove(profile)

    def is_premium_active(self):
        """
        Возвращает True, если премиум-статус активен на текущий момент, иначе - False.
        """
        premium_purchase = PremiumPurchase.objects.filter(
            profile=self).latest('expiry_date')
        if premium_purchase:
            return premium_purchase.expiry_date > timezone.now()
        return False

    def request_photo_verification(self):
        """
        Отправляет запрос на верификацию фото.
        """
        self.photo_verification_requested = True
        self.save()

    def verify_photo(self):
        """
        Верифицирует фото пользователя.
        """
        self.photo_verified = True
        self.photo_verification_requested = False
        self.save()

    def following_count(self):
        return self.following_set.count()

    def friends_online(self):
        now = timezone.now()
        five_minutes_ago = now - timedelta(minutes=5)
        return self.friends.filter(last_activity__gte=five_minutes_ago)

    def is_friend_of(self, other_profile):
        return other_profile in self.friends.all()
    
    def is_following_of(self, other_profile):
        return other_profile in self.followers.all()


class LanguageModel(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'SocialLink of {self.user.username}'


class Status(models.Model):
    """Represents a status created by a user, which can be of type text, photo, or video."""

    STATUS_TYPES = (
        ('text', 'Text'),
        ('photo', 'Photo'),
        ('video', 'Video'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='statuses')
    content = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(
        max_length=5, choices=STATUS_TYPES, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    photo = models.ImageField(
        upload_to='status_photos/users/%Y/%m/%d/', blank=True, null=True)
    video = models.FileField(
        upload_to='status_videos/users/%Y/%m/%d/', blank=True, null=True)
    comments_count = models.PositiveIntegerField(default=0, editable=False)
    likes_count = models.PositiveIntegerField(default=0, editable=False)
    comments_enabled = models.BooleanField(default=True)
    favorites = models.ManyToManyField(
        User, through='StatusFavorite', related_name='favorite_statuses')

    def __str__(self):
        return f'{self.user.username} - {self.type}'

    def save(self, *args, **kwargs):
        if self.type == "text" and not self.content:
            raise ValidationError(
                "Text content is required for the text status type.")
        if self.type == "photo" and not self.photo:
            raise ValidationError(
                "A photograph is required for the photographic type of status.")
        if self.type == "video" and not self.video:
            raise ValidationError("Video is required for status video type.")
        super(Status, self).save(*args, **kwargs)

    def update_comment_count(self):
        self.comments_count = self.comments.count()
        self.save()

    def like(self, user):
        like, created = StatusLike.objects.get_or_create(
            user=user, status=self)
        if created:
            self.update_likes_count()

    def unlike(self, user):
        deleted_count = StatusLike.objects.filter(
            user=user, status=self).delete()
        if deleted_count[0] > 0:
            self.update_likes_count()

    def update_likes_count(self):
        self.likes_count = self.likes.count()
        self.save()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def delete_status(self):
        self.delete()

    def add_to_favorites(self, user):
        favorite, created = StatusFavorite.objects.get_or_create(
            user=user, status=self)
        if created:
            # Вы можете выполнить дополнительные действия при добавлении статуса в избранное
            pass

    def remove_from_favorites(self, user):
        deleted_count = StatusFavorite.objects.filter(
            user=user, status=self).delete()
        if deleted_count[0] > 0:
            # Вы можете выполнить дополнительные действия при удалении статуса из избранного
            pass


class StatusComment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name='comments')
    text = RichTextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(
        default=0)  # новое поле для количества лайков

    def __str__(self):
        return f'Comment by {self.user.username} on {self.status}'

    def save(self, *args, **kwargs):
        super(StatusComment, self).save(*args, **kwargs)
        self.status.update_comment_count()

    def like(self):
        """Увеличить количество лайков на 1."""
        self.likes_count += 1
        self.save()

    def add_reply(self, user, text):
        """Добавить реплай к этому комментарию."""
        reply = StatusComment(user=user, status=self.status, text=text)
        reply.save()


class StatusLike(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='status_likes')
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'status')
        indexes = [
            models.Index(fields=['user', '-created_date']),
        ]


@receiver(post_save, sender=StatusLike)
def update_likes_count_on_add(sender, instance, **kwargs):
    instance.status.update_likes_count()


@receiver(post_delete, sender=StatusLike)
def update_likes_count_on_delete(sender, instance, **kwargs):
    instance.status.update_likes_count()


class StatusFavorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='status_favorites')
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.status.type} - {self.status.id}'


class MenuItem(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    url = models.CharField(_("URL"), max_length=200)
    order = models.IntegerField(_("Order"), default=0)
    icon_name = models.CharField(
        _("Icon Name"), max_length=200, null=True, blank=True)
    icon_color = models.CharField(
        _("Icon Color"), max_length=7, default='#000000', blank=True)
    enabled = models.BooleanField(_("Enabled"), default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.TextField(blank=True, null=True)
    date_blocked = models.DateTimeField(auto_now_add=True)


class CreditTransaction(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    TRANSACTION_TYPES = [
        ('C', 'Credit'),
        ('D', 'Debit'),
    ]
    transaction_type = models.CharField(
        max_length=1, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True, null=True)


class PremiumPackage(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in days")

    # Булевые переменные для поиска по различным параметрам
    enable_age = models.BooleanField(default=False)
    enable_gender = models.BooleanField(default=False)
    enable_country = models.BooleanField(default=False)
    enable_city = models.BooleanField(default=False)
    enable_personality_type = models.BooleanField(default=False)
    enable_height = models.BooleanField(default=False)
    enable_weight = models.BooleanField(default=False)
    enable_hair_color = models.BooleanField(default=False)
    enable_eye_color = models.BooleanField(default=False)
    enable_relationship_goals = models.BooleanField(default=False)
    enable_relationship_status = models.BooleanField(default=False)
    enable_sexual_orientation = models.BooleanField(default=False)
    enable_children = models.BooleanField(default=False)
    enable_smoking = models.BooleanField(default=False)
    enable_alcohol = models.BooleanField(default=False)
    enable_physique = models.BooleanField(default=False)
    enable_tatu = models.BooleanField(default=False)
    enable_piercing = models.BooleanField(default=False)
    enable_scars = models.BooleanField(default=False)
    enable_zodiac_sign = models.BooleanField(default=False)
    enable_animals = models.BooleanField(default=False)
    enable_religion = models.BooleanField(default=False)
    enable_interests = models.BooleanField(default=False)
    enable_languages = models.BooleanField(default=False)
    enable_school = models.BooleanField(default=False)
    enable_education_level = models.BooleanField(default=False)
    enable_work_and_education = models.BooleanField(default=False)
    enable_organization = models.BooleanField(default=False)
    enable_position = models.BooleanField(default=False)

    def get_filter_settings(self):
        return {
            'enable_age': self.enable_age,
            'enable_gender': self.enable_gender,
            'enable_country': self.enable_country,
            'enable_city': self.enable_city,
            'enable_personality_type': self.enable_personality_type,
            'enable_height': self.enable_height,
            'enable_weight': self.enable_weight,
            'enable_hair_color': self.enable_hair_color,
            'enable_eye_color': self.enable_eye_color,
            'enable_relationship_goals': self.enable_relationship_goals,
            'enable_relationship_status': self.enable_relationship_status,
            'enable_sexual_orientation': self.enable_sexual_orientation,
            'enable_children': self.enable_children,
            'enable_smoking': self.enable_smoking,
            'enable_alcohol': self.enable_alcohol,
            'enable_physique': self.enable_physique,
            'enable_tatu': self.enable_tatu,
            'enable_piercing': self.enable_piercing,
            'enable_scars': self.enable_scars,
            'enable_zodiac_sign': self.enable_zodiac_sign,
            'enable_animals': self.enable_animals,
            'enable_religion': self.enable_religion,
            'enable_interests': self.enable_interests,
            'enable_languages': self.enable_languages,
            'enable_school': self.enable_school,
            'enable_education_level': self.enable_education_level,
            'enable_work_and_education': self.enable_work_and_education,
            'enable_organization': self.enable_organization,
            'enable_position': self.enable_position,
        }
    def __str__(self):
        return self.title



class PremiumPurchase(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    package = models.ForeignKey(PremiumPackage, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return f"{self.profile.user.username} - {self.package.title}"
