from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Override username to add validators
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[MinLengthValidator(3)],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    
    def __str__(self):
        return self.username
    
    @property
    def questions_asked(self):
        return self.questions.count()
    
    @property
    def questions_answered(self):
        return self.answers.count()
    
    @property
    def total_score(self):
        return self.questions_asked + self.questions_answered
    
    class Meta:
        ordering = ['-date_joined']


class Question(models.Model):
    """Question model for Would You Rather questions"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    option_one_text = models.CharField(max_length=255)
    option_two_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Would you rather {self.option_one_text} or {self.option_two_text}?"
    
    @property
    def option_one_votes(self):
        return self.answers.filter(option_selected='optionOne').count()
    
    @property
    def option_two_votes(self):
        return self.answers.filter(option_selected='optionTwo').count()
    
    @property
    def total_votes(self):
        return self.answers.count()
    
    def has_user_answered(self, user):
        if not user.is_authenticated:
            return False
        return self.answers.filter(user=user).exists()
    
    def get_user_answer(self, user):
        try:
            return self.answers.get(user=user)
        except Answer.DoesNotExist:
            return None


class Answer(models.Model):
    """Answer model for user responses to questions"""
    OPTION_CHOICES = [
        ('optionOne', 'Option One'),
        ('optionTwo', 'Option Two'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    option_selected = models.CharField(max_length=10, choices=OPTION_CHOICES)
    answered_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'question')
        ordering = ['-answered_at']
    
    def __str__(self):
        return f"{self.user.username} answered {self.question.id}"