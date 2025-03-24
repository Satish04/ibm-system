"""
Core models for the Book Management System.

This module defines the database models for managing books and their reviews,
including the Book and Review models with their respective fields and relationships.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.utils import timezone

class TimeStampedModel(models.Model):
    """
    An abstract base model that provides self-managed created_at and updated_at fields.
    """
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Book(TimeStampedModel):
    """
    Model representing a book in the system.

    Attributes:
        title (str): The title of the book
        author (str): The author of the book
        genre (str): The genre of the book
        year_published (int): The year the book was published
        description (str): A detailed description of the book
        summary (str): AI-generated summary of the book (optional)
        rating (float): Average rating of the book (0.0 to 5.0)
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, null=True, blank=True)
    year_published = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
        null=True,
        blank=True
    )
    description = models.TextField()
    summary = models.TextField(blank=True, null=True)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

    def update_rating(self):
        """
        Update the book's average rating based on all its reviews.
        
        Calculates the average rating from all reviews and updates the book's rating field.
        If there are no reviews, the rating is set to 0.0.
        """
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.rating = avg_rating if avg_rating is not None else 0.0
        self.save()

class Review(TimeStampedModel):
    """
    Model representing a user review for a book.

    Attributes:
        book (Book): The book being reviewed
        user (User): The user who wrote the review
        rating (int): Rating given by the user (1 to 5)
        comment (str): Detailed review comment
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_rating()
