"""
Django app configuration for the Book Management System.

This module contains the configuration for the books app, which handles
book and review management functionality.
"""

from django.apps import AppConfig


class BooksConfig(AppConfig):
    """
    Configuration class for the books application.

    This class defines the application settings including the default
    auto field type and application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'
