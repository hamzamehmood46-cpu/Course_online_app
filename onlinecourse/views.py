from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Submission


def home(request):
    course = Course.objects.order_by("id").first()
    if not course:
        return render(request, "onlinecourse/empty_state.html")
    return redirect("course_detail", course_id=course.id)


def course_detail(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related("lessons__questions__choices"),
        pk=course_id,
    )
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course},
    )


def submit_exam(request, course_id):
    if request.method != "POST":
        return redirect("course_detail", course_id=course_id)

    course = get_object_or_404(
        Course.objects.prefetch_related("lessons__questions__choices"),
        pk=course_id,
    )
    questions = [
        question
        for lesson in course.lessons.all()
        for question in lesson.questions.all()
    ]

    if not questions:
        raise Http404("No questions are available for this course.")

    correct_answers = 0
    for question in questions:
        selected_choice_id = request.POST.get(f"question_{question.id}")
        if not selected_choice_id:
            continue
        if question.choices.filter(pk=selected_choice_id, is_correct=True).exists():
            correct_answers += 1

    total_questions = len(questions)
    score = int((correct_answers / total_questions) * 100)
    submission = Submission.objects.create(
        course=course,
        user_name=request.POST.get("user_name") or "Student",
        score=score,
        total_questions=total_questions,
        total_correct=correct_answers,
    )
    return redirect("show_exam_result", submission_id=submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("course"),
        pk=submission_id,
    )
    passed = submission.score >= 60
    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "submission": submission,
            "passed": passed,
        },
    )
