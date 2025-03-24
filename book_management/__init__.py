# from django.core.management.base import BaseCommand
# from books.models import Book, Review
# from django.contrib.auth.models import User
# import random
#
# def handle_():
#
#     books_data = [
#         {"title": f"Book {i}", "author": f"Author {i}", "description": f"Description for book {i}"}
#         for i in range(1000)
#     ]
#
#     books = [Book(**book_data) for book_data in books_data]
#     Book.objects.bulk_create(books)
#
#     books = Book.objects.all()
#     user, _ = User.objects.get_or_create(username="satish", defaults={"email": "satishpandey2212@gmail.com"})
#
#     reviews_data = []
#     for book in books:
#         for _ in range(3):  # 3 reviews per book
#             reviews_data.append({
#                 "book": book,
#                 "user": user,
#                 "rating": round(random.uniform(3, 5), 1),
#                 "comment": f"Review for {book.title}"
#             })
#     Review.objects.bulk_create([Review(**review) for review in reviews_data])
