from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class AuthenticationMiddleware:
    """
    Custom middleware to handle authentication state and redirects.
    Ensures proper routing based on authentication status.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Public URLs that don't require authentication
        self.public_urls = [
            reverse('login'),
            reverse('signup'),
        ]
    
    def __call__(self, request):
        # Check if the current path is a public URL
        is_public_url = request.path in self.public_urls
        
        # Handle authenticated users trying to access login/signup
        if request.user.is_authenticated and is_public_url:
            if request.path == reverse('login') or request.path == reverse('signup'):
                messages.info(request, 'You are already logged in.')
                return redirect('home')
        
        response = self.get_response(request)
        return response


class LoginRequiredMiddleware:
    """
    Middleware to require authentication for all views except public ones.
    Provides a centralized way to protect routes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that are accessible without authentication
        self.exempt_urls = [
            reverse('login'),
            reverse('signup'),
        ]
    
    def __call__(self, request):
        # Check if URL is exempt or if user is authenticated
        path = request.path
        
        # Allow access to static and media files
        if path.startswith('/static/') or path.startswith('/media/'):
            return self.get_response(request)
        
        # Check if current path is exempt
        is_exempt = any(path == exempt_url for exempt_url in self.exempt_urls)
        
        # Redirect unauthenticated users to login (except for exempt URLs)
        if not is_exempt and not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this page.')
            return redirect(f"{reverse('login')}?next={path}")
        
        response = self.get_response(request)
        return response