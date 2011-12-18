from django.shortcuts import render_to_response


def frontpage(requset):
    """docstring for group"""
    return render_to_response('groups/frontpage.html')

def single(request):
    return render_to_response('groups/single.html')