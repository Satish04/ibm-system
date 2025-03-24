from rest_framework import serializers
from django.contrib.auth.models import User
from books.models import Book, Review
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    
    class Meta:
        model = Review
        fields = ('id', 'rating', 'comment', 'user', 'book', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'rating', 'average_rating', 'review_count', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class BookSummarySerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()
    review_count = serializers.IntegerField()
    latest_reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'summary', 'average_rating', 'review_count', 'latest_reviews')

class BookRecommendationSerializer(serializers.ModelSerializer):
    similarity_score = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'rating', 'similarity_score')