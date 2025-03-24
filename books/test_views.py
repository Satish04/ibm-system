from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, Mock
from books.models import Book, Review
from books.api.v1.serializers import BookSerializer, ReviewSerializer

class BookViewSetTest(TestCase):
    """Test cases for the BookViewSet API endpoints."""

    def setUp(self):
        """Set up test client, user, and book instances."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            rating=4.5
        )

    def test_get_book_list(self):
        """Test retrieving a list of books."""
        response = self.client.get('/books/api/v1/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book(self):
        """Test creating a new book."""
        new_book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'description': 'New Description'
        }
        response = self.client.post('/books/api/v1/books/', new_book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_get_book_detail(self):
        """Test retrieving details of a specific book."""
        response = self.client.get(f'/books/api/v1/books/{self.book.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        """Test updating an existing book."""
        updated_data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'description': 'Updated Description'
        }
        response = self.client.put(
            f'/books/api/v1/books/{self.book.pk}/',
            updated_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        """Test deleting a book."""
        response = self.client.delete(f'/books/api/v1/books/{self.book.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    @patch('books.api.v1.utils.requests.get')
    @patch('books.api.v1.utils.requests.post')
    def test_generate_summary(self, mock_post, mock_get):
        """Test generating a summary for a book."""
        # Mock successful health check
        mock_health = Mock()
        mock_health.status_code = 200
        mock_get.return_value = mock_health

        # Mock successful summary generation
        mock_summary = "Test summary"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": mock_summary}
        mock_post.return_value = mock_response
        
        response = self.client.post(f'/books/api/v1/books/{self.book.pk}/generate_summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary'], mock_summary)

    def test_add_review(self):
        """Test adding a review to a book."""
        review_data = {
            'rating': 4,
            'comment': 'Great book!'
        }
        response = self.client.post(
            f'/books/api/v1/books/{self.book.pk}/add_review/',
            review_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().book, self.book)
        self.assertEqual(Review.objects.first().user, self.user)

class ReviewViewSetTest(TestCase):
    """Test cases for the ReviewViewSet API endpoints."""

    def setUp(self):
        """Set up test client, user, book, and review instances."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description'
        )
        
        self.review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=4,
            comment='Test Review'
        )

    def test_get_review_list(self):
        """Test retrieving a list of reviews."""
        response = self.client.get('/books/api/v1/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_review(self):
        """Test creating a new review."""
        new_review_data = {
            'book': self.book.id,
            'rating': 5,
            'comment': 'New Review'
        }
        response = self.client.post('/books/api/v1/reviews/', new_review_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(Review.objects.last().book_id, self.book.id)

    def test_get_review_detail(self):
        """Test retrieving details of a specific review."""
        response = self.client.get(f'/books/api/v1/reviews/{self.review.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], self.review.comment)

    def test_update_review(self):
        """Test updating an existing review."""
        updated_data = {
            'book': self.book.id,
            'rating': 3,
            'comment': 'Updated Review'
        }
        response = self.client.put(
            f'/books/api/v1/reviews/{self.review.pk}/',
            updated_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, 'Updated Review')

    def test_delete_review(self):
        """Test deleting a review."""
        response = self.client.delete(f'/books/api/v1/reviews/{self.review.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
