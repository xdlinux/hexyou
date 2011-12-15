from django.shortcuts import render_to_response


def frontpage(requset):
    """docstring for group"""
    return render_to_response('group/base.html')
