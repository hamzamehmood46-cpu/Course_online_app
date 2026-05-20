from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_time = models.BooleanField(default=True)
    courses = models.ManyToManyField(Course, related_name="instructors", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Learner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    courses = models.ManyToManyField(Course, related_name="learners", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_text = models.CharField(max_length=255)
    grade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_choice_ids):
        if any(choice.is_get_score(selected_choice_ids) for choice in self.choices.all()):
            return self.grade
        return 0


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

    def is_get_score(self, selected_choice_ids):
        return self.is_correct and str(self.id) in {str(choice_id) for choice_id in selected_choice_ids}


class Submission(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    user_name = models.CharField(max_length=150, default="Student")
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    total_correct = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at", "-id"]

    def __str__(self):
        return f"{self.user_name} - {self.course.name} ({self.score}%)"
