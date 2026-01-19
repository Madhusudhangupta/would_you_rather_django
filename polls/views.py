from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, F, Window
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from .models import User, Question, Answer
from .forms import UserLoginForm, UserSignupForm, QuestionForm, AnswerForm
from django.db.models.functions import DenseRank


# ============================================================
# AUTHENTICATION VIEWS
# ============================================================

@never_cache
def login_view(request):
    """
    Handle user login with proper validation and error handling.
    Redirects authenticated users to home page.
    """
    # Redirect if already authenticated
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect to next parameter or home
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            # Form validation failed
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserLoginForm()
    
    return render(request, 'polls/login.html', {
        'form': form,
        'show_signup': True
    })


@never_cache
def signup_view(request):
    """
    Handle user registration with validation.
    Automatically logs in user after successful registration.
    """
    # Redirect if already authenticated
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            # Create new user
            user = form.save()
            
            # Get the password from cleaned data for authentication
            raw_password = form.cleaned_data.get('password1')
            
            # Authenticate and login the user
            authenticated_user = authenticate(
                request,
                username=user.username,
                password=raw_password
            )
            
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(
                    request,
                    f'Account created successfully! Welcome, {user.username}!'
                )
                return redirect('home')
            else:
                messages.error(request, 'Account created but login failed. Please try logging in.')
                return redirect('login')
        else:
            # Form has validation errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserSignupForm()
    
    return render(request, 'polls/signup.html', {
        'form': form,
        'show_login': True
    })


@login_required
@require_http_methods(["GET", "POST"])
def logout_view(request):
    """
    Handle user logout and clear authentication state.
    Redirects to login page with confirmation message.
    """
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye, {username}! You have been logged out.')
    return redirect('login')


# ============================================================
# MAIN APPLICATION VIEWS
# ============================================================

@login_required
def home_view(request):
    """
    Display home page with answered and unanswered questions.
    Requires authentication.
    """
    user = request.user
    
    # Get answered question IDs for current user
    answered_question_ids = Answer.objects.filter(
        user=user
    ).values_list('question_id', flat=True)
    
    # Get unanswered questions
    unanswered_questions = Question.objects.exclude(
        id__in=answered_question_ids
    ).select_related('author').order_by('-created_at')
    
    # Get answered questions
    answered_questions = Question.objects.filter(
        id__in=answered_question_ids
    ).select_related('author').order_by('-created_at')
    
    # Determine active tab
    active_tab = request.GET.get('tab', 'unanswered')
    
    context = {
        'unanswered_questions': unanswered_questions,
        'answered_questions': answered_questions,
        'active_tab': active_tab,
        'unanswered_count': unanswered_questions.count(),
        'answered_count': answered_questions.count(),
    }
    
    return render(request, 'polls/home.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def new_question_view(request):
    """
    Handle creation of new questions.
    Requires authentication.
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            messages.success(request, 'Question created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuestionForm()
    
    return render(request, 'polls/new_question.html', {'form': form})


@login_required
def question_detail_view(request, question_id):
    """
    Display question details and handle answer submission.
    Shows results if user has already answered, otherwise shows answer form.
    Requires authentication.
    """
    question = get_object_or_404(Question.objects.select_related('author'), id=question_id)
    user = request.user
    
    # Check if user has already answered
    user_answer = question.get_user_answer(user)
    
    if user_answer:
        # User has answered - show results
        total_votes = question.total_votes
        option_one_votes = question.option_one_votes
        option_two_votes = question.option_two_votes
        
        # Calculate percentages
        option_one_percentage = (option_one_votes / total_votes * 100) if total_votes > 0 else 0
        option_two_percentage = (option_two_votes / total_votes * 100) if total_votes > 0 else 0
        
        context = {
            'question': question,
            'user_answer': user_answer,
            'total_votes': total_votes,
            'option_one_votes': option_one_votes,
            'option_two_votes': option_two_votes,
            'option_one_percentage': round(option_one_percentage, 1),
            'option_two_percentage': round(option_two_percentage, 1),
            'show_results': True,
        }
    else:
        # User hasn't answered - show answer form
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.user = user
                answer.question = question
                
                try:
                    answer.save()
                    messages.success(request, 'Answer submitted successfully!')
                    return redirect('question_detail', question_id=question.id)
                except Exception as e:
                    messages.error(request, 'An error occurred while saving your answer.')
            else:
                messages.error(request, 'Please select an option.')
        else:
            form = AnswerForm()
        
        context = {
            'question': question,
            'form': form,
            'show_results': False,
        }
    
    return render(request, 'polls/question_detail.html', context)

@login_required
def leaderboard_view(request):
    """
    Display leaderboard without conflicting property names
    """
    users = User.objects.annotate(
        questions_authored_count=Count('questions', distinct=True),
        answers_count=Count('answers', distinct=True)  # or exclude self if needed
    )

    # Sort by total score
    sorted_users = sorted(
        users,
        key=lambda u: (u.questions_authored_count + u.answers_count),
        reverse=True
    )

    leaderboard = []
    for idx, user in enumerate(sorted_users, start=1):
        leaderboard.append({
            'rank': idx,
            'user': user,
            'questions_asked': user.questions_authored_count,
            'questions_answered': user.answers_count,
            'total_score': user.questions_authored_count + user.answers_count
        })

    return render(request, 'polls/leaderboard.html', {'leaderboard': leaderboard})

# @login_required
# def leaderboard_view(request):
    """
    Display leaderboard with sequential ranks in order of total_score.
    """
    users = User.objects.annotate(
        total_questions=Count('questions'),
        total_answers=Count('answers')
    )

    # Sort users by total_score descending, then questions asked, then answers
    users = sorted(
        users,
        key=lambda u: (u.total_questions + u.total_answers, u.total_questions, u.total_answers),
        reverse=True
    )

    leaderboard = []
    for idx, user in enumerate(users, start=1):
        leaderboard.append({
            'rank': idx,
            'user': user,
            'questions_asked': user.total_questions,
            'questions_answered': user.total_answers,
            'total_score': user.total_questions + user.total_answers
        })

    return render(request, 'polls/leaderboard.html', {'leaderboard': leaderboard})


# ============================================================
# ERROR HANDLERS
# ============================================================

def custom_404_view(request, exception=None):
    """Handle 404 errors with custom template"""
    return render(request, 'polls/404.html', status=404)