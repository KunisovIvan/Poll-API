from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from .serializers import *
from datetime import datetime


# Вывести список всех опросов
class PollsListView(generics.ListAPIView):
    queryset = Polls.objects.all()
    serializer_class = PollsListSerializer
    permission_classes = (permissions.IsAdminUser, )

# Добавить опрос
class PollCreateView(generics.CreateAPIView):
    serializer_class = PollsListSerializer
    permission_classes = (permissions.IsAdminUser, )

# Изменение/удаление опроса
class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Polls.objects.all()
    serializer_class = PollsListSerializer
    permission_classes = (permissions.IsAdminUser, )

# Добавить вопрос к опросу
class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionCreateSerializer
    permission_classes = (permissions.IsAdminUser, )

    def perform_create(self, serializer):
        poll = get_object_or_404(Polls, pk=self.kwargs['poll_pk'])
        serializer.save(poll=poll)


# Изменение/удаление вопросa
class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionListSerializer
    permission_classes = (permissions.IsAdminUser, )

# Вывести список вопросов, которые относятся к определенному опросу
class QuestionsListView(generics.ListAPIView):
    serializer_class = QuestionListSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
         poll = get_object_or_404(Polls, id=self.kwargs['poll_pk'])
         return poll.questions.all()

# Вывести список активных опросов
class ActivePollsListView(generics.ListAPIView):
    queryset = Polls.objects.filter(finished_at__gte=datetime.today())
    serializer_class = PollsListSerializer
    permission_classes = (permissions.AllowAny,)

#Ответить на вопрос
class AnswersCreateView(generics.CreateAPIView):
    queryset = Answers.objects.all()
    serializer_class = AnswersListSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        question = get_object_or_404(Questions, pk=self.kwargs['question_pk'], poll__id=self.kwargs['poll_pk'], )
        if question.answer_type == 'text_answer':
            return AnswersTextSerializer
        elif question.answer_type == 'radio':
            return AnswerOneChoiceSerializer
        else:
            return AnswerMultipleChoiceSerializer

    def perform_create(self, serializer):
        question = get_object_or_404(Questions, pk=self.kwargs['question_pk'], poll__id=self.kwargs['poll_pk'], )
        try:
            serializer.save(user=self.request.user, question=question)
        except:
            serializer.save(question=question)


# Добавить вариант ответа к определенному вопросу
class AnswerOptionsCreateView(generics.CreateAPIView):
    serializer_class = AnswerOptionsListSerializer
    permission_classes = (permissions.IsAdminUser, )

    def perform_create(self, serializer):
        question = get_object_or_404(Questions, pk=self.kwargs['question_pk'], poll__id=self.kwargs['poll_pk'], )
        serializer.save(question=question)

#Вывести варианты ответа, которые относятся к определенному вопросу
class AnswerOptionsListView(generics.ListAPIView):
    serializer_class = AnswerOptionsListSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
         question = get_object_or_404(Questions, id=self.kwargs['question_pk'])
         return question.answer_options.all()

#Вывести все опросы, пройденные пользователем
class UserIdPollListView(generics.ListAPIView):
    serializer_class = UserIdPollListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Polls.objects.exclude(~Q(questions__answers__user__id=user_id))
        return queryset


