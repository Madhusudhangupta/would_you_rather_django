# Would You Rather Django App

## Core Application Files

#### **Models & Database**
-  `polls/models.py` - User, Question, Answer models with validation
-  Migrations folder with `__init__.py`

#### **Views & Controllers**
-  `polls/views.py` - All views with authentication logic
-  `polls/urls.py` - Application URL routing
-  `would_you_rather/urls.py` - Project URL configuration

#### **Forms**
-  `polls/forms.py` - UserSignupForm, UserLoginForm, QuestionForm, AnswerForm

#### **Templates**
-  `polls/templates/polls/base.html` - Base template with navbar
-  `polls/templates/polls/login.html` - Login page (modern design)
-  `polls/templates/polls/signup.html` - Signup page (NEW)
-  `polls/templates/polls/home.html` - Home with stats and tabs (UPDATED)
-  `polls/templates/polls/new_question.html` - Create question (UPDATED)
-  `polls/templates/polls/question_detail.html` - Answer/results page (UPDATED)
-  `polls/templates/polls/leaderboard.html` - Leaderboard with rankings (UPDATED)
-  `polls/templates/polls/404.html` - Error page (UPDATED)

#### **Static Files**
-  `polls/static/polls/css/style.css` - Complete styling
-  `polls/static/polls/images/default-avatar.png` - Default avatar image

#### **Admin**
-  `polls/admin.py` - Enhanced admin interface

#### **Middleware**
-  `polls/middleware.py` - Authentication middleware (NEW)

#### **Management Commands**
-  `polls/management/__init__.py`
-  `polls/management/commands/__init__.py`
-  `polls/management/commands/create_initial_users.py`
-  `polls/management/commands/seed_questions.py` (NEW)

#### **Configuration**
-  `polls/apps.py` - App configuration
-  `would_you_rather/settings.py` - Project settings with security
-  `would_you_rather/wsgi.py` - WSGI configuration
-  `would_you_rather/asgi.py` - ASGI configuration

---

## Setup Commands in Order

```bash
# 1. Create project directory
mkdir would_you_rather_project
cd would_you_rather_project

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install Django==4.2.7 Pillow==10.1.0

# 4. Create Django project
django-admin startproject would_you_rather .

# 5. Create app
python manage.py startapp polls

# 6. Create directory structure
mkdir -p polls/templates/polls
mkdir -p polls/static/polls/css
mkdir -p polls/static/polls/images
mkdir -p polls/management/commands
mkdir -p media/avatars

# 7. Create __init__.py files
touch polls/management/__init__.py
touch polls/management/commands/__init__.py

# 8. Copy all code files to their locations

# 9. Add default avatar image to:
# polls/static/polls/images/default-avatar.png

# 10. Run migrations
python manage.py makemigrations polls
python manage.py migrate

# 11. Create test users
python manage.py create_initial_users

# 12. Seed sample questions
python manage.py seed_questions

# 13. Create superuser
python manage.py createsuperuser

# 14. Collect static files
python manage.py collectstatic --noinput

# 15. Run server
python manage.py runserver
```

---

## Testing Checklist

### Authentication Testing

####  Signup Flow
- [ ] Navigate to `/signup/`
- [ ] Try username < 3 chars (should fail)
- [ ] Try duplicate username (should fail)
- [ ] Try duplicate email (should fail)
- [ ] Try password < 8 chars (should fail)
- [ ] Try password mismatch (should fail)
- [ ] Create valid account
- [ ] Verify auto-login after signup
- [ ] Verify redirect to home page
- [ ] Verify success message appears

####  Login Flow
- [ ] Navigate to `/`
- [ ] Try wrong username (should fail)
- [ ] Try wrong password (should fail)
- [ ] Login with correct credentials
- [ ] Verify redirect to home
- [ ] Verify welcome message
- [ ] Verify navbar appears

####  Logout Flow
- [ ] Click avatar dropdown
- [ ] Click "Logout"
- [ ] Verify session cleared
- [ ] Verify redirect to login
- [ ] Verify goodbye message

####  Protected Routes
- [ ] Logout completely
- [ ] Try to access `/home/` (should redirect to login)
- [ ] Try to access `/add/` (should redirect to login)
- [ ] Try to access `/leaderboard/` (should redirect to login)
- [ ] Login and verify access to all routes

### Application Testing

####  Home Page
- [ ] View stats boxes (unanswered, answered, score)
- [ ] Switch between tabs
- [ ] Verify unanswered questions display
- [ ] Verify answered questions display
- [ ] Click "Answer" button
- [ ] Click "View Results" button

####  Create Question
- [ ] Navigate to New Question
- [ ] Try option < 3 chars (should fail)
- [ ] Create valid question
- [ ] Verify success message
- [ ] Verify question in unanswered tab
- [ ] Cancel and return to home

####  Answer Question
- [ ] Click "Answer" on question
- [ ] View question details
- [ ] Try submitting without selection (should fail)
- [ ] Select option and submit
- [ ] Verify results display
- [ ] Verify percentages calculated
- [ ] Verify your choice marked
- [ ] Question moves to answered tab

####  Leaderboard
- [ ] View all users ranked
- [ ] Verify top 3 have special styling
- [ ] Verify scores calculated correctly
- [ ] Verify "You" tag on current user
- [ ] Verify medals/badges display
- [ ] Check responsive design

####  404 Page
- [ ] Navigate to `/invalid-url/`
- [ ] Verify custom 404 page
- [ ] Verify "Invalid URL" message
- [ ] Click "Go to Home" (or Login if not authenticated)

### UI/UX Testing

####  Navbar (Authenticated)
- [ ] All links present (Home, New Question, Leadboard)
- [ ] Active link highlighted
- [ ] Username displayed
- [ ] Avatar displayed
- [ ] Dropdown works
- [ ] Logout button works
- [ ] Mobile responsive (burger menu)

####  Messages
- [ ] Success messages display
- [ ] Error messages display
- [ ] Messages auto-hide after 5 seconds
- [ ] Messages dismissible with X button

####  Forms
- [ ] All inputs have icons
- [ ] Validation errors display
- [ ] Help text displays
- [ ] Focus states work
- [ ] Submit buttons work
- [ ] Cancel/back buttons work

####  Responsive Design
- [ ] Test on mobile (< 768px)
- [ ] Test on tablet (768px - 1024px)
- [ ] Test on desktop (> 1024px)
- [ ] All elements stack properly
- [ ] Touch targets large enough
- [ ] Text readable on all sizes

### Admin Panel Testing

####  Admin Features
- [ ] Login to `/admin/`
- [ ] View users list with stats
- [ ] View questions with vote stats
- [ ] View answers
- [ ] Create new question via admin
- [ ] Edit existing question
- [ ] Delete question
- [ ] Verify avatar previews display

---

### Visual Features
-  Gradient backgrounds
-  Smooth animations
-  Hover effects
-  Loading states
-  Font Awesome icons
-  Color-coded elements
-  Progress bars
-  Medals/badges
-  Responsive cards
-  Modern forms

---

## Security Features Implemented

-  Password hashing (Django default)
-  CSRF protection on all forms
-  Session-based authentication
-  Login required decorators
-  Password validation (min 8 chars)
-  Username validation (min 3 chars)
-  Email validation
-  SQL injection protection (Django ORM)
-  XSS protection (Django templates)
-  Protected routes
-  Secure logout

---

## Database Schema

### User Model
- id (PK)
- username (unique, min 3 chars)
- email (unique)
- password (hashed)
- first_name
- last_name
- avatar (image)
- date_joined
- Computed: questions_asked, questions_answered, total_score

### Question Model
- id (PK)
- author (FK to User)
- option_one_text
- option_two_text
- created_at
- Computed: option_one_votes, option_two_votes, total_votes

### Answer Model
- id (PK)
- user (FK to User)
- question (FK to Question)
- option_selected (optionOne/optionTwo)
- answered_at
- Unique: (user, question)

---

## Quick Reference

### URLs
- `/` - Login
- `/signup/` - Sign up
- `/home/` - Home page
- `/add/` - New question
- `/question/<id>/` - Question detail
- `/leaderboard/` - Leaderboard
- `/logout/` - Logout
- `/admin/` - Admin panel

### Test Users (if created)
- Username: `Alex One`, Password: `password123`
- Username: `Bob Two`, Password: `password123`
- Username: `Charles Three`, Password: `password123`

### Management Commands
```bash
python manage.py create_initial_users
python manage.py seed_questions
python manage.py createsuperuser
python manage.py runserver
```

---

## Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --clear
```

### Database Errors
```bash
rm db.sqlite3
rm -rf polls/migrations/
python manage.py makemigrations polls
python manage.py migrate
```

### Import Errors
Check all `__init__.py` files exist

### Avatar Not Displaying
Check MEDIA_URL and MEDIA_ROOT in settings

### Session Issues
```bash
python manage.py clearsessions
```

---

## Features Summary

### Authentication
-  User registration with validation
-  Login with username/password
-  Auto-login after signup
-  Secure logout
-  Protected routes
-  Session management

### Questions
-  Create questions
-  Answer questions
-  View results with percentages
-  Track answered/unanswered
-  Progress bars

### Leaderboard
-  User rankings
-  Score calculation
-  Top 3 highlighting
-  Medals/badges
-  Statistics display

### UI/UX
-  Modern, responsive design
-  Font Awesome icons
-  Smooth animations
-  Success/error messages
-  Loading states
-  Mobile-friendly

### Admin
-  User management
-  Question management
-  Answer tracking
-  Statistics display
-  Avatar previews

---