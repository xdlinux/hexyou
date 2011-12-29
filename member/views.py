# Create your views here.
from django.shortcuts import render_to_response

def frontpage(request):
    """docstring for person"""
    return render_to_response('members/frontpage.html')

def single(request):
	"""docstring for person"""
	return render_to_response('members/single.html')