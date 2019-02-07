from datetime import date

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    bio = models.TextField(
        max_length=400,
        help_text="You bio here!"
    )
    phone_number = PhoneNumberField()
    website = models.URLField(max_length=250)
    photo = models.ImageField(
        upload_to='upload/profile/',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["date_joined"]

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('polls:profile', kwargs={'username': self.username})

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Connection(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='follower',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["date_created"]

    def __str__(self):
        return f"{self.follower} : {self.following}"


class UserPost(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        blank=True
    )
    date_posted = models.DateField(default=date.today)
    date_updated = models.DateField(default=date.today)
    likes = models.IntegerField(default=0)
    PUBLIC = 1
    PRIVATE = 2
    PRIVACY_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    )
    privacy = models.PositiveSmallIntegerField(
        default=PUBLIC,
        choices=PRIVACY_CHOICES
    )
    text = models.TextField(
        max_length=1000,
        help_text="Your post here!"
    )

    class Meta:
        ordering = ["date_updated"]

    def get_number_of_likes(self):
        return self.like_set.count()


class Comment(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    commenter = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        blank=True
    )
    text = models.CharField(max_length=100)
    date_posted = models.DateField(default=date.today)

    def __str__(self):
        return f"Posted on {self.date_posted}. Comment: {self.text}"


class Like(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user_post", "user_profile")
