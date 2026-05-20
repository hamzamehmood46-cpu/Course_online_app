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
        Course.objects.prefetch_related("lessons__questions__choices", "learners"),
        pk=course_id,
    )
    questions = [
        question
        for lesson in course.lessons.all()
        for question in lesson.questions.all()
    ]

    if not questions:
        raise Http404("No questions are available for this course.")

    selected_choice_ids = []
    for question in questions:
        selected_choice_id = request.POST.get(f"question_{question.id}")
        if not selected_choice_id:
            continue
        selected_choice_ids.append(selected_choice_id)

    total_score = sum(question.is_get_score(selected_choice_ids) for question in questions)
    possible_score = sum(question.grade for question in questions)
    correct_answers = sum(
        1 for question in questions if question.is_get_score(selected_choice_ids) == question.grade
    )
    score = int((total_score / possible_score) * 100) if possible_score else 0
    enrollment = course.learners.filter(
        first_name__iexact=request.POST.get("user_name", "")
    ).first() or course.learners.first()

    submission = Submission.objects.create(
        course=course,
        user_name=(
            f"{enrollment.first_name} {enrollment.last_name}"
            if enrollment
            else request.POST.get("user_name") or "Student"
        ),
        score=score,
        total_questions=len(questions),
        total_correct=correct_answers,
    )
    return redirect("show_exam_result", submission_id=submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("course"),
        pk=submission_id,
    )
    course = submission.course
    questions = [
        question
        for lesson in course.lessons.prefetch_related("questions__choices").all()
        for question in lesson.questions.all()
    ]
    question_results = []
    for question in questions:
        correct_choices = [
            choice.choice_text for choice in question.choices.all() if choice.is_correct
        ]
        question_results.append(
            {
                "question_text": question.question_text,
                "correct_choices": correct_choices,
                "grade": question.grade,
            }
        )
    possible_score = sum(question.grade for question in questions)
    total_score = int((submission.score / 100) * possible_score) if possible_score else 0
    enrollment = course.learners.filter(
        first_name__iexact=submission.user_name.split(" ")[0]
    ).first()
    passed = submission.score >= 60
    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        {
            "submission": submission,
            "course": course,
            "enrollment": enrollment,
            "passed": passed,
            "total_score": total_score,
            "possible_score": possible_score,
            "question_results": question_results,
        },
    )
