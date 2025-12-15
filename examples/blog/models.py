"""Example Django models for testing the scanner."""

from django.db import models
from django.contrib.auth.models import User


class TimestampedModel(models.Model):
    """Abstract base model with timestamp fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    """Blog category model."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "blog_categories"
        verbose_name_plural = "categories"


class Post(TimestampedModel):
    """Blog post model with abstract inheritance."""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField("Tag", related_name="posts", blank=True)
    published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]


class Comment(TimestampedModel):
    """Comment model with self-referential relationship."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    content = models.TextField()
    approved = models.BooleanField(default=False)


class Tag(models.Model):
    """Tag model for post categorization."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)


class Profile(models.Model):
    """User profile with one-to-one relationship."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True)
    website = models.URLField(blank=True)
