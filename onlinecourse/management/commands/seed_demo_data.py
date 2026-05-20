from django.core.management.base import BaseCommand

from onlinecourse.models import Choice, Course, Lesson, Question


class Command(BaseCommand):
    help = "Create demo course content for the assignment screenshots."

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            name="Python for Web Development",
            defaults={
                "description": (
                    "A mock online course with lessons and an assessment so the "
                    "assignment flow can be demonstrated end to end."
                ),
            },
        )

        lesson_specs = [
            (
                1,
                "Introduction to Django",
                "Learn how Django apps, URLs, views, and templates work together.",
                [
                    (
                        "Which file usually stores Django model classes?",
                        [
                            ("models.py", True),
                            ("views.py", False),
                            ("settings.py", False),
                        ],
                    ),
                    (
                        "Which command creates database tables from migrations?",
                        [
                            ("python manage.py migrate", True),
                            ("python manage.py runserver", False),
                            ("python manage.py collectstatic", False),
                        ],
                    ),
                ],
            ),
            (
                2,
                "Templates and Bootstrap",
                "Display course details and related lessons using Django templates.",
                [
                    (
                        "Which template tag prints a variable value?",
                        [
                            ("{{ variable }}", True),
                            ("{% variable %}", False),
                            ("[[ variable ]]", False),
                        ],
                    ),
                    (
                        "What does Bootstrap mainly help with?",
                        [
                            ("Responsive styling", True),
                            ("Database migrations", False),
                            ("Python package installation", False),
                        ],
                    ),
                ],
            ),
        ]

        for order, title, content, questions in lesson_specs:
            lesson, _ = Lesson.objects.get_or_create(
                course=course,
                order=order,
                defaults={"title": title, "content": content},
            )
            if lesson.title != title or lesson.content != content:
                lesson.title = title
                lesson.content = content
                lesson.save(update_fields=["title", "content"])

            for question_text, choices in questions:
                question, _ = Question.objects.get_or_create(
                    lesson=lesson,
                    question_text=question_text,
                    defaults={"grade": 1},
                )
                for choice_text, is_correct in choices:
                    Choice.objects.get_or_create(
                        question=question,
                        choice_text=choice_text,
                        defaults={"is_correct": is_correct},
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo course ready. Open /course/{course.id}/ to test the mock exam."
            )
        )
