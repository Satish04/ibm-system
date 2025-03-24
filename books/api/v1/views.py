"""
API views for the Book Management System.

This module provides ViewSets for managing books and reviews through the REST API,
including features like book summaries, recommendations, and review management.
"""

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Avg, Count

from books.models import Book, Review
from books.api.v1.serializers import (
    BookSerializer,
    ReviewSerializer,
    BookSummarySerializer,
    BookRecommendationSerializer,
    CustomTokenObtainPairSerializer
)
from books.api.v1.utils import generate_summary

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view for JWT authentication.
    
    Extends the default JWT token view to use custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer

class BaseBookViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """Base ViewSet with common functionality."""
    permission_classes = [IsAuthenticated]

class BookViewSet(BaseBookViewSet):
    """
    ViewSet for managing books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        """Add aggregated fields to queryset."""
        return Book.objects.annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )

    @action(detail=True, methods=['post'])
    def generate_summary(self, request, **_):
        """Generate a summary for the book using AI."""
        book = self.get_object()
        summary = generate_summary(book.description)
        book.summary = summary
        book.save()
        return Response({"summary": summary})

    @action(detail=True, methods=['get'])
    def reviews(self, request, **_):
        """Get all reviews for a specific book."""
        book = self.get_object()
        reviews = book.reviews.select_related('user').all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_review(self, request, **_):
        """Add a new review to the book."""
        book = self.get_object()
        review_data = request.data.copy()
        review_data['book_id'] = book.id
        serializer = ReviewSerializer(data=review_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            book.refresh_from_db()
            book_serializer = BookSerializer(book)
            return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def summary(self, request, **_):
        """Get book summary and aggregated rating."""
        book = self.get_object()
        book_with_stats = Book.objects.filter(id=book.id).annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).first()
        latest_reviews = book.reviews.select_related('user').order_by('-created_at')[:5]
        book_with_stats.latest_reviews = latest_reviews
        serializer = BookSummarySerializer(book_with_stats)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """Get personalized book recommendations."""
        user_reviews = Review.objects.filter(user=request.user)
        if not user_reviews.exists():
            recommended_books = Book.objects.annotate(
                average_rating=Avg('reviews__rating'),
                similarity_score=Avg('rating')
            ).order_by('-average_rating')[:5]
        else:
            highly_rated = user_reviews.filter(rating__gte=4).values_list('book', flat=True)
            recommended_books = Book.objects.exclude(
                id__in=highly_rated
            ).annotate(
                average_rating=Avg('reviews__rating'),
                similarity_score=Avg('rating')
            ).filter(
                average_rating__gte=4
            ).order_by('-average_rating')[:5]

        serializer = BookRecommendationSerializer(recommended_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def generate_content_summary(self, request):
        """Generate a summary for given book content."""
        content = request.data.get('content')
        if not content:
            return Response(
                {"error": "Content is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        summary = generate_summary(content)
        return Response({"summary": summary})

class ReviewViewSet(BaseBookViewSet):
    """
    ViewSet for managing reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)