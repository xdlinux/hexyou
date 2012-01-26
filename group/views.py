from django.shortcuts import render_to_response,redirect,get_object_or_404
from NearsideBindings.group.forms import GroupForm
from NearsideBindings.group.models import Group
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


def frontpage(request):
    """docstring for group"""
    return render_to_response('groups/frontpage.html')

def single(request,group_slug):
    group = get_object_or_404(Group,slug=group_slug)
    return render_to_response('groups/single.html',locals())

@login_required(login_url='/login/')
def new(request):
    if request.POST:
        form = GroupForm(request.POST)
        success,group,membership=form.create_group(request.user)
        if success:
            return redirect('/groups/%s' % group.slug)
    else:
        form=GroupForm()
    return render_to_response('groups/new.html', {
        'form':form
        }, context_instance=RequestContext(request)
    )
    
