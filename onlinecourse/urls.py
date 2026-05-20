from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),
    path("course/<int:course_id>/submit/", views.submit_exam, name="submit_exam"),
    path(
        "submission/<int:submission_id>/result/",
        views.show_exam_result,
        name="show_exam_result",
    ),
]
