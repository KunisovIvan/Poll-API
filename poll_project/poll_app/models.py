from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Polls(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    started_at = models.DateField(auto_now_add=True, verbose_name='Дата старта опроса')
    finished_at = models.DateField(verbose_name='Дата окончания опроса')

    def __str__(self):
        return self.title


class Questions(models.Model):
    ANSWER_TYPES = (
        ('text_answer', 'Ответ текстом'),
        ('radio', 'Один вариант'),
        ('check_boxes', 'Выбор нескольких вариантов')
    )
    answer_type = models.CharField(max_length=20, choices=ANSWER_TYPES, verbose_name='Тип ответа на вопрос')
    text = models.TextField(blank=True, verbose_name='Текст вопроса')
    poll = models.ForeignKey(Polls, blank=True, on_delete=models.CASCADE, related_name="questions", verbose_name='Опрос')

    def __str__(self):
        return self.text

class AnswerOptions(models.Model):
    title = models.TextField(verbose_name='Вариант ответа')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="answer_options")

    def __str__(self):
        return self.title

class Answers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="answers", verbose_name='Вопрос')
    answer = models.TextField(null=True, verbose_name='Ответ')
    many_options = models.ManyToManyField(AnswerOptions, null=True, related_name="answers_many_option")
    one_option = models.ForeignKey(AnswerOptions, null=True, on_delete=models.CASCADE, related_name="answers_one_option")

