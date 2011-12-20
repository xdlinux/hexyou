from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    """index"""
    return render_to_response("index.html",locals(),context_instance=RequestContext(request))


def signup(request):
    """page for signup"""
    return render_to_response("accounts/signup.html")
