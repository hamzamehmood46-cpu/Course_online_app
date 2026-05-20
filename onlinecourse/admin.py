from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Choice, Course, Lesson, Question, Submission


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ("question_text", "grade")


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    fields = ("choice_text", "is_correct")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "lesson", "grade")
    list_filter = ("lesson__course",)
    search_fields = ("question_text", "lesson__title")
    inlines = [ChoiceInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title", "course__name")
    inlines = [QuestionInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "is_correct")
    list_filter = ("is_correct", "question__lesson__course")
    search_fields = ("choice_text", "question__question_text")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user_name", "course", "score", "submitted_at")
    list_filter = ("course", "submitted_at")
    readonly_fields = (
        "course",
        "user_name",
        "score",
        "total_questions",
        "total_correct",
        "submitted_at",
    )
