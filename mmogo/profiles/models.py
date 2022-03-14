from django.db import models
from django.contrib.auth.models import User
from mmogo.contrib.locations.models import Country


class Profile(models.Model):
    ENGLISH = 0
    MALE = 1
    FEMALE = 2
    GENDER_NOT_SET = 0

    LANGUAGE_CHOICES = ((ENGLISH, 'English'), )
    GENDER_CHOICES = ((GENDER_NOT_SET, 'Not Set'),
                      (MALE, 'Male'), (FEMALE, 'Female'),)

    user = models.OneToOneField(
        User, related_name="user_profile", on_delete=models.CASCADE)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, default=ENGLISH)

    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    cover = models.ImageField(
        upload_to='profiles/covers/', blank=True, null=True)

    mobile = models.CharField(max_length=255, blank=True, null=True)
    accepted_terms = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True, null=True)
    mobile_token = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    invitation_code = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(
        Country, related_name="user_country", on_delete=models.CASCADE)

    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=GENDER_NOT_SET)

    life_time_value = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=11)
    total_savings = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=11)
    abandoned_value = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=11)
    potential_savings = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=11)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_login = models.BooleanField(default=True)
    first_login_at = models.DateTimeField(blank=True, null=True)
    last_login_at = models.DateTimeField(blank=True, null=True)
    is_guest = models.BooleanField(default=False)
    onboarded = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(f"{self.user.first_name} {self.user.last_name}")

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
