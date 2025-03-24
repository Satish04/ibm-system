# Intelligent Book Management System

A Django-based REST API service for managing books and reviews, featuring AI-powered book summary generation using Ollama.

## Features

- RESTful API with Django REST Framework
- JWT Authentication
- PostgreSQL Database
- Docker Containerization
- Ollama Integration for AI-powered Book Summaries
- Book and Review Management
- Rating System
- Robust Error Handling and Logging

## Tech Stack

- Django 5.1.6
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- Ollama (Mistral Model)
- JWT Authentication

## Prerequisites

- Docker
- Docker Compose

## Project Structure

```
book_management/
├── books/                    # Main Django app
│   ├── api/                 # API endpoints
│   │   └── v1/             # API version 1
│   ├── models.py           # Database models
│   └── tests/              # Unit tests
│       ├── test_models.py  # Model tests
│       ├── test_utils.py   # Utility tests
│       └── test_views.py   # View tests
├── book_management/         # Django project settings
├── docker/                  # Docker configuration files
├── requirements.txt         # Python dependencies
└── docker-compose.yml       # Docker services configuration
```

## Database Schema

### Book Model
- `title`: CharField
- `author`: CharField
- `description`: TextField
- `summary`: TextField (AI-generated)
- `rating`: FloatField
- `review_count`: IntegerField
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

### Review Model
- `book`: ForeignKey(Book)
- `user`: ForeignKey(User)
- `rating`: IntegerField
- `comment`: TextField
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

## API Endpoints

### Authentication
- `POST /api/v1/token/`: Get JWT token
- `POST /api/v1/token/refresh/`: Refresh JWT token

### Books
- `GET /api/v1/books/`: List all books
- `POST /api/v1/books/`: Create a new book
- `GET /api/v1/books/{id}/`: Get book details
- `PUT /api/v1/books/{id}/`: Update book
- `DELETE /api/v1/books/{id}/`: Delete book
- `POST /api/v1/books/{id}/generate_summary/`: Generate AI summary
- `POST /api/v1/books/{id}/add_review/`: Add a review to a book
- `GET /api/v1/books/{id}/reviews/`: Get all reviews for a book

### Reviews
- `GET /api/v1/reviews/`: List all reviews
- `POST /api/v1/reviews/`: Create a new review
- `GET /api/v1/reviews/{id}/`: Get review details
- `PUT /api/v1/reviews/{id}/`: Update review
- `DELETE /api/v1/reviews/{id}/`: Delete review

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd book_management
```

2. Create a `.env` file in the project root:
```env
POSTGRES_DB=<book_management>
POSTGRES_USER=<postgres>
POSTGRES_PASSWORD=<postgres>
POSTGRES_HOST=<db>
POSTGRES_PORT=<5432>
```

3. Build and start the containers:
```bash
docker-compose up -d
```

4. Create a superuser:
```bash
docker exec -it book_management_app python manage.py createsuperuser
```

5. Access the API at `http://localhost:8000/books/api/v1/`

## AI Summary Generation

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

## Development

To run tests:
```bash
docker exec -it book_management_app python manage.py test
```

To make migrations:
```bash
docker exec -it book_management_app python manage.py makemigrations
docker exec -it book_management_app python manage.py migrate
```

### Testing
The project includes comprehensive test coverage:
- Model tests: Test database models and their relationships
- View tests: Test API endpoints and their responses
- Utility tests: Test helper functions and external service integrations
- Mock tests: Test external service interactions without actual API calls

## Security

- JWT authentication for API endpoints
- PostgreSQL password protection
- CSRF protection
- Environment variables for sensitive data
- Input validation and sanitization
- Error logging for security monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
