import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now() 


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text

class Response(models.Model): 
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    time = models.DateTimeField("Time")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # @property
    # def getText(self):
    #     return self.choice.choice_text
    def __str__(self):
        return self.choice.choice_text
    # @classmethod
    # def create(choice time):
    #     choice = choice
    #     time = time
    #     # do something with the book
    #     return book
#class ResponseManager(models.Manager) :
#      def create_response(self, choice):
#           response = self.create(choice = choice)
#           return response;
#https://docs.djangoproject.com/en/4.2/ref/models/instances/#:~:text=To%20create%20a%20new%20instance,you%20need%20to%20save()%20.
#how to make an object of a model in jango. where do u go from here 
    
# def was_published_recently(self):
#     now = timezone.now()
#     return now - datetime.timedelta(days=1) <= self.pub_date <= now