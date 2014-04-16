from django.http import HttpResponse, HttpResponseRedirect
#from django.template import RequestContext, loader
from pollsapp.models import Poll, Choice
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

'''
def index(request):
    #return HttpResponse("Hello world.  You're at the poll index.")
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #output = ','.join([p.question for p in latest_poll_list])
    #return HttpResponse(output)
    #template = loader.get_template('pollsapp/index.html')
'''
'''
    context = RequestContext(
        request,
        {'latest_poll_list': latest_poll_list},
    )
    return HttpResponse(template.render(context))
'''
'''
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'pollsapp/index.html', context)

'''
class IndexView(generic.ListView):
    template_name = 'pollsapp/index.html'
    context_object_name = 'latest_poll_list'
    
    def get_queryset(self):
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
'''
def detail(request, poll_id):
    #return HttpResponse("You're looking at poll %s." % poll_id)
'''
'''
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
'''
'''
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'pollsapp/detail.html', {'poll': poll})
'''

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'pollsapp/detail.html'

    def get_queryset(self):
        """
        Prevents seeing polls that are not ready for publication.
        """
        return Poll.objects.filter(
            pub_date__lte = timezone.now()
        )

'''
def results(request, poll_id):
    #return HttpResponse("Your looking at the results of poll %s." % poll_id)
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_list = poll.choice_set.all()
    return render(request, 'pollsapp/results.html', {'poll': poll})
'''

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'pollsapp/results.html'


def vote(request, poll_id):
    #return HttpResponse("You're voting on poll %s." % poll_id)
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,
            'pollsapp/detal.html',
            {'poll': p, 
             'error_message': "You didn't select a choice"},
        )

    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

            
