from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice, Thing



def index(request):
    if request.method == 'POST':
        print('post request')
    else:
        latest_questions = Question.objects.filter(published_at__lte=timezone.now()) \
                                            .order_by('-published_at')
        return render(request, 'polls/index.html', {'latest_questions': latest_questions})
    

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay question voting form
        error_message = "You didn't select a choice."
        context = {
            'question': question,
            'error_message': error_message
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def new_question(request):
    question_text = request.POST['question_text']
    if not question_text:
        return redirect(reverse('polls:index'))

    question = Question(question_text=request.POST['question_text'])
    question.save()
    thing = Thing(content=question.question_text)
    thing.save()
    return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
