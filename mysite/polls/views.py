from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Choice, Response
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User



# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})
@login_required
def index(request):
    answered = Question.objects.filter(choice__response__user = request.user)
    # while answered is not None:
    #     for answer in answered:  
    #         b = answer.save()
    #         answered.exclude(b)
    #         for answer in answered:
    #             if answer.id == b.id:
    #                 answer.remove()
    #             answered.add(b)
    #         index = answered.iterator().next()
    #         if answer.id == index.id:
    #             answer.remove()
    # figure out how to delete from a queery sets bc theyre not like lists

    notAnswered = Question.objects.exclude(choice__response__user = request.user)
    context = {
        "answered" : answered,
        "notAnswered" : notAnswered 
    }
    return render(request, "polls/index.html", context) #error on this line. can't pass in a query set? "supposed to be a dictionary rather than a queery set"

    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    # template_name = "polls/index.html"
    # context_object_name = "latest_question_list"
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by("-pub_date")[:5]
    # def get_queryset(self):
        # """
        # Return the last five published questions (not including those set to be
        # published in the future).
        # """
        # return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(LoginRequiredMixin,generic.DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
# @login_required
# def pollsA(request,pk):
#         question = get_object_or_404(Question)
#         r = Response.objects.filter(user = request.user, choice__question = question)
#         q = Question.objects.get(pk=question)
#         choice = Choice.objects.get(id=r)
#         choice.votes += 1
#         choice.save()
#         if vote.objects.filter(question=1, user = request.user).count() == 1:
#             return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
@login_required
def detail(request, question_id):
    
    question = Question.objects.get(pk=question_id)
    usersvoted = User.objects.filter(response__choice__question = question_id)

    if request.user in usersvoted:
        my_response = Choice.objects.filter(question = question_id, response__user = request.user).annotate(num_votes=Count("response")).first()
        choices = Choice.objects.filter(question_id = question_id).annotate(num_votes=Count("response")).exclude(response__user = request.user)

        return render(request, 'polls/results.html', {'question': question, "my_response": my_response, "choices": choices})    
    #question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

@login_required
def results(request,pk):
    # if not r.exists():
    choices = Choice.objects.filter(question_id = pk).annotate(num_votes=Count("response")).exclude(response__user = request.user)
    my_response = Choice.objects.filter(question = pk, response__user = request.user).annotate(num_votes=Count("response")).first()
    #model = Question
    #template_name = "polls/results.html"
    #return render(request,"polls/results.html",context)
    #make context
    context = {
        "my_response": my_response,
        "question": Question.objects.get(id = pk),
        "choices": choices,
    }
    return render(request, "polls/results.html", context)

@login_required     
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    r = Response.objects.filter(user = request.user, choice__question = question)
    if r is not None:
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
            Question.objects.filter(choice = selected_choice) # THIS IS when u wanna know the exact chocie someone made if they already voted highlighted part of the assigment *
            
        except (KeyError, Choice.DoesNotExist):
            return render(
                request,
                "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
            ) 
        else: 
            r = Response(choice = selected_choice , time = datetime.now() , user = request.user) 
            r.save()
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

# Leave the rest of the views (detail, results, vote) unchanged
