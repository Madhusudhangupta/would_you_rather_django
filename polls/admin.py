from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Question, Answer


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin with enhanced display and functionality"""
    list_display = [
        'username', 
        'email', 
        'full_name',
        'avatar_preview',
        'questions_asked', 
        'questions_answered',
        'total_score',
        'is_staff',
        'date_joined'
    ]
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('avatar', 'bio')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    def full_name(self, obj):
        """Display user's full name"""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.username
    full_name.short_description = 'Full Name'
    
    def avatar_preview(self, obj):
        """Display avatar thumbnail in admin"""
        if obj.avatar:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%;" />',
                obj.avatar.url
            )
        return '-'
    avatar_preview.short_description = 'Avatar'
    
    def questions_asked(self, obj):
        """Display count of questions asked"""
        count = obj.questions.count()
        return format_html('<strong>{}</strong>', count)
    questions_asked.short_description = 'Questions Asked'
    
    def questions_answered(self, obj):
        """Display count of questions answered"""
        count = obj.answers.count()
        return format_html('<strong>{}</strong>', count)
    questions_answered.short_description = 'Questions Answered'
    
    def total_score(self, obj):
        """Display total user score"""
        score = obj.total_score
        return format_html('<strong style="color: #667eea;">{}</strong>', score)
    total_score.short_description = 'Total Score'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Question Admin with enhanced features"""
    list_display = [
        'id',
        'question_preview',
        'author',
        'created_at',
        'total_votes',
        'option_one_percentage',
        'option_two_percentage'
    ]
    list_filter = ['created_at', 'author']
    search_fields = ['option_one_text', 'option_two_text', 'author__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'vote_statistics']
    
    fieldsets = (
        ('Question Details', {
            'fields': ('author', 'option_one_text', 'option_two_text')
        }),
        ('Metadata', {
            'fields': ('created_at', 'vote_statistics')
        }),
    )
    
    def question_preview(self, obj):
        """Display question preview"""
        return f"{obj.option_one_text[:30]}... or {obj.option_two_text[:30]}..."
    question_preview.short_description = 'Question'
    
    def total_votes(self, obj):
        """Display total votes"""
        return format_html('<strong>{}</strong>', obj.total_votes)
    total_votes.short_description = 'Total Votes'
    
    def option_one_percentage(self, obj):
        """Display option one percentage"""
        total = obj.total_votes
        if total == 0:
            return '0%'
        percentage = (obj.option_one_votes / total) * 100
        return format_html('<span style="color: #3298dc;">{:.1f}%</span>', percentage)
    option_one_percentage.short_description = 'Option 1 %'
    
    def option_two_percentage(self, obj):
        """Display option two percentage"""
        total = obj.total_votes
        if total == 0:
            return '0%'
        percentage = (obj.option_two_votes / total) * 100
        return format_html('<span style="color: #48c774;">{:.1f}%</span>', percentage)
    option_two_percentage.short_description = 'Option 2 %'
    
    def vote_statistics(self, obj):
        """Display detailed vote statistics"""
        if obj.total_votes == 0:
            return 'No votes yet'
        
        option_one_pct = (obj.option_one_votes / obj.total_votes) * 100
        option_two_pct = (obj.option_two_votes / obj.total_votes) * 100
        
        return format_html(
            '<div style="margin: 10px 0;">'
            '<p><strong>Option 1:</strong> {} votes ({:.1f}%)</p>'
            '<p><strong>Option 2:</strong> {} votes ({:.1f}%)</p>'
            '<p><strong>Total:</strong> {} votes</p>'
            '</div>',
            obj.option_one_votes, option_one_pct,
            obj.option_two_votes, option_two_pct,
            obj.total_votes
        )
    vote_statistics.short_description = 'Vote Statistics'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Answer Admin with filtering and search"""
    list_display = [
        'id',
        'user',
        'question_preview',
        'option_selected',
        'answered_at'
    ]
    list_filter = ['option_selected', 'answered_at', 'user']
    search_fields = [
        'user__username',
        'question__option_one_text',
        'question__option_two_text'
    ]
    date_hierarchy = 'answered_at'
    readonly_fields = ['answered_at']
    
    fieldsets = (
        ('Answer Details', {
            'fields': ('user', 'question', 'option_selected')
        }),
        ('Metadata', {
            'fields': ('answered_at',)
        }),
    )
    
    def question_preview(self, obj):
        """Display question preview"""
        return f"Q{obj.question.id}: {obj.question.option_one_text[:25]}..."
    question_preview.short_description = 'Question'