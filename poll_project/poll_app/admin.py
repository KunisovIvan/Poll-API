from django.contrib import admin
from .models import Questions, Answers, Polls, AnswerOptions


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']


class AnswersAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


class PollsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

class AnswerOptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'question']

admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(Polls, PollsAdmin)
admin.site.register(AnswerOptions, AnswerOptionsAdmin)