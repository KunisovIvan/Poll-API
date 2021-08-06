from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'poll_app'
urlpatterns = [
    path('active_polls/', ActivePollsListView.as_view()),
    path('user_polls/', UserIdPollListView.as_view()),

    path('polls/', PollsListView.as_view()),
    path('polls/<int:pk>/', PollDetailView.as_view()),
    path('polls/<int:poll_pk>/questions/', QuestionsListView.as_view()),
    path('polls/<int:poll_pk>/questions/<int:pk>/', QuestionDetailView.as_view()),
    path('polls/<int:poll_pk>/questions/<int:question_pk>/answers_options', AnswerOptionsListView.as_view()),
    path('polls/<int:poll_pk>/questions/<int:question_pk>/answers/', AnswersCreateView.as_view()),


    path('polls/create/', PollCreateView.as_view()),
    path('polls/<int:poll_pk>/questions/create/', QuestionCreateView.as_view()),
    path('polls/<int:poll_pk>/questions/<int:question_pk>/answers_options/create', AnswerOptionsCreateView.as_view()),
]