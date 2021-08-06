from rest_framework import serializers
from .models import Polls, Questions, Answers, AnswerOptions
from django.db.models import Q

#Вывод опросов
class PollsListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Polls


#Вывод вопросов
class QuestionListSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        fields = '__all__'
        model = Questions

    def get_answers(self, question):
        user_id = self.context.get('request').user.id
        answers = Answers.objects.filter(
            Q(question=question) & Q(user__id=user_id))
        serializer = AnswersListSerializer(instance=answers, many=True)
        return serializer.data

#Вывод вопросов для create
class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['text', 'answer_type',]
        model = Questions


#Вывод ответов
class AnswersListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'answer', 'many_options', 'one_option', ]
        model = Answers

#Вывод текстовых ответов
class AnswersTextSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['answer', ]
        model = Answers

class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        question_id = self.context.get('request').parser_context['kwargs']['question_pk']
        request = self.context.get('request', None)
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(question_id=question_id)

# ответ выбором одного варианта
class AnswerOneChoiceSerializer(serializers.ModelSerializer):
    one_option = UserFilteredPrimaryKeyRelatedField(many=False, queryset=AnswerOptions.objects.all())

    class Meta:
        fields = ['one_option']
        model = Answers


# ответ выбором нескольких вариантов
class AnswerMultipleChoiceSerializer(serializers.ModelSerializer):
    many_options = UserFilteredPrimaryKeyRelatedField(many=True, queryset=AnswerOptions.objects.all())

    class Meta:
        fields = ['many_options']
        model = Answers

#Варианты ответа
class AnswerOptionsListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', ]
        model = AnswerOptions

#Опросы, пройденные пользователем
class UserIdPollListSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Polls
