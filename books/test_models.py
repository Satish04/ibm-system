from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Book, Review
from django.core.exceptions import ValidationError

class BookModelTest(TestCase):
    """Test cases for the Book model."""

    def setUp(self):
        """Create a test book instance."""
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            rating=4.5
        )

    def test_book_creation(self):
        """Test that a book can be created with correct attributes."""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.description, "Test Description")
        self.assertEqual(self.book.rating, 4.5)

    def test_book_str_representation(self):
        """Test the string representation of a book."""
        self.assertEqual(str(self.book), "Test Book by Test Author")

    def test_invalid_rating(self):
        """Test that a book cannot be created with an invalid rating."""
        with self.assertRaises(ValidationError):
            book = Book(
                title="Invalid Book",
                author="Test Author",
                description="Test Description",
                rating=6.0  # Rating should be between 0 and 5
            )
            book.full_clean()

class ReviewModelTest(TestCase):
    """Test cases for the Review model."""

    def setUp(self):
        """Create test user, book, and review instances."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description"
        )
        self.review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=4,
            comment="Great book!"
        )

    def test_review_creation(self):
        """Test that a review can be created with correct attributes."""
        self.assertEqual(self.review.book, self.book)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, "Great book!")

    def test_review_str_representation(self):
        """Test the string representation of a review."""
        expected = f"Review by {self.user.username} for {self.book.title}"
        self.assertEqual(str(self.review), expected)

    def test_invalid_rating(self):
        """Test that a review cannot be created with an invalid rating."""
        with self.assertRaises(ValidationError):
            review = Review(
                book=self.book,
                user=self.user,
                rating=6,  # Rating should be between 1 and 5
                comment="Test comment"
            )
            review.full_clean()

    def test_book_average_rating(self):
        """Test that a book's rating is updated correctly when reviews are added."""
        # Create another review
        Review.objects.create(
            book=self.book,
            user=User.objects.create_user(username='testuser2', password='testpass123'),
            rating=5,
            comment="Excellent!"
        )
        # Refresh book from database
        self.book.refresh_from_db()
        # Average should be (4 + 5) / 2 = 4.5
        self.assertEqual(self.book.rating, 4.5)
