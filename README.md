# Intelligent Book Management System

A sophisticated Django-based REST API service for managing books and reviews, featuring AI-powered book summary generation using Ollama's Mistral model.

## 🚀 Features

- **RESTful API Architecture**
  - Built with Django REST Framework
  - API versioning (v1)
  - Comprehensive API documentation with Swagger UI

- **Authentication & Security**
  - JWT-based authentication
  - Token refresh mechanism
  - Secure password handling
  - CSRF protection

- **Core Functionality**
  - Book management (CRUD operations)
  - Review system with ratings
  - AI-powered book summary generation
  - Book recommendations based on user preferences
  - Rating aggregation and statistics

- **Database**
  - PostgreSQL for robust data storage
  - Efficient data relationships
  - Optimized queries

- **Development & Deployment**
  - Docker containerization
  - Easy setup with Docker Compose
  - Automated testing suite
  - Comprehensive logging

## 📋 Prerequisites

- Docker & Docker Compose
- Git
- Port 8000 available on host machine

## 🛠️ Quick Start

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd book_management
   ```

2. **Environment Setup**
   Create a `.env` file in the project root:
   ```env
   POSTGRES_DB=book_management
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

3. **Build & Start Services**
   ```bash
   docker-compose up -d
   ```

4. **Create Admin User**
   ```bash
   docker exec -it book_management_app python manage.py createsuperuser
   ```

5. **Access the Application**
   - API Documentation: http://localhost:8000/api/docs/
   - Admin Interface: http://localhost:8000/admin/
   - API Base URL: http://localhost:8000/books/api/v1/

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/token/` - Obtain JWT token
- `POST /api/v1/token/refresh/` - Refresh JWT token

### Book Endpoints
- `GET /api/v1/books/` - List all books
- `POST /api/v1/books/` - Create a book
- `GET /api/v1/books/{id}/` - Get book details
- `PUT /api/v1/books/{id}/` - Update book
- `DELETE /api/v1/books/{id}/` - Delete book
- `POST /api/v1/books/{id}/generate_summary/` - Generate AI summary
- `GET /api/v1/books/{id}/reviews/` - Get book reviews
- `POST /api/v1/books/{id}/add_review/` - Add review

### Review Endpoints
- `GET /api/v1/reviews/` - List all reviews
- `POST /api/v1/reviews/` - Create review
- `GET /api/v1/reviews/{id}/` - Get review details
- `PUT /api/v1/reviews/{id}/` - Update review
- `DELETE /api/v1/reviews/{id}/` - Delete review

## 🧪 Testing & Development

### Running Tests
```bash
docker exec -it book_management_app python manage.py test
```

### Test Coverage
- Model validations
- API endpoints
- Authentication
- Summary generation
- Error handling
- Database operations

## 🤖 AI Summary Generation

The system uses Ollama with the Mistral model to generate summaries for books. The summary generation is triggered through the `/api/v1/books/{id}/generate_summary/` endpoint.

### How it works:
1. When a POST request is made to the generate_summary endpoint:
   - The system performs a health check on the Ollama service
   - If the service is healthy, it sends the book's description to Ollama
   - Ollama processes the text using the Mistral model
   - The generated summary is returned in the response

### Error Handling:
- Connection errors: Returns a message if Ollama service is unavailable
- Timeout errors: Returns a message if the request takes too long (timeout: 120s)
- General errors: Returns detailed error messages for debugging

## 📊 Database Schema

### Book Model
```python
class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField(default=0)
    summary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Review Model
```python
class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Key Features
- BigAutoField for all primary keys
- Cascading deletes for reviews when a book is deleted
- One-to-Many relationship between Book and Review models
- Rating system:
  - Book rating: 0-5 float (average of review ratings)
  - Review rating: 1-5 integer
- Automatic timestamps for creation and updates
- Nullable summary field for AI-generated content

## 📚 Sample Data & Fixtures

### Loading Sample Data
The project includes sample data to help you get started quickly:

1. **Load Fixtures**
   ```bash
   # Load sample books
   docker exec -it book_management_app python manage.py loaddata books/fixtures/sample_books.json
   
   # Load sample reviews
   docker exec -it book_management_app python manage.py loaddata books/fixtures/sample_reviews.json
   ```

2. **Sample Admin User**
   ```bash
   docker exec -it book_management_app python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
   ```

### Sample API Requests

1. **Get JWT Token**
   ```bash
   curl -X POST http://localhost:8000/api/v1/token/ \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "admin123"}'
   ```

2. **List Books**
   ```bash
   curl -X GET http://localhost:8000/books/api/v1/books/ \
        -H "Authorization: Bearer <your_token>"
   ```

3. **Add a Book**
   ```bash
   curl -X POST http://localhost:8000/books/api/v1/books/ \
        -H "Authorization: Bearer <your_token>" \
        -H "Content-Type: application/json" \
        -d '{
          "title": "Sample Book",
          "author": "John Doe",
          "description": "A great book about coding"
        }'
   ```

4. **Generate Summary**
   ```bash
   curl -X POST http://localhost:8000/books/api/v1/books/1/generate_summary/ \
        -H "Authorization: Bearer <your_token>"
   ```

5. **Add Review**
   ```bash
   curl -X POST http://localhost:8000/books/api/v1/books/1/add_review/ \
        -H "Authorization: Bearer <your_token>" \
        -H "Content-Type: application/json" \
        -d '{
          "rating": 5,
          "comment": "Excellent book!"
        }'
   ```

## 🔒 Security Features

- JWT authentication for API security
- PostgreSQL password protection
- Environment variables for sensitive data
- Input validation and sanitization
- Error logging for security monitoring
- CSRF protection enabled

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please:
1. Check the API documentation at `/api/docs/`
2. Review existing issues on GitHub
3. Create a new issue if needed

---
Built with ❤️ using Django, DRF, and Ollama
