from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    """index"""
    return render_to_response("index.html",locals(),context_instance=RequestContext(request))

def home(request):
    """timeline"""
    return render_to_response("home.html")

def signup(request):
    """page for signup"""
    return render_to_response("accounts/signup.html")

def signin(request):
    """page for signup"""
    return render_to_response("accounts/signin.html")
