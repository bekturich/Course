from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    category_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.category_name


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('преподаватель', 'преподаватель'),
        ('клиент', 'клиент'),
    )
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='клиент')
    full_name = models.CharField(max_length=32)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Course(models.Model):
    LEVEL_CHOICES = (
        ('начальный', 'начальный'),
        ('средний', 'средний'),
        ('продвинутый', 'продвинутый'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name

    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 1)
        return 0

    def get_count_people(self):
        total = self.reviews.all()
        if total.exists():
            if total.count() > 2:
                return '2+'
            return total.count()
        return 0

    def get_count_good_grade(self):
        total = self.reviews.all()
        if total.exists():
            num = 0
            for i in total:
                if i.rating > 3:
                    num += 1
            return f'{round((num * 100) / total.count())}%'
        return 0


class Lesson(models.Model):           #модели Уроков
    title = models.CharField(max_length=100)
    video_url = models.URLField()
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title


class Assignment(models.Model):      #модели Заданий
    title = models.CharField(max_length=32)
    description = models.TextField()
    due_date = models.DateTimeField()  #срок сдачи
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    students = models.ManyToManyField(UserProfile, related_name='assignmentss', blank=True)

    def __str__(self):
        return self.title


class Exam(models.Model):               #модели экзаменов
    title = models.CharField(max_length=52)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    passing_score = models.PositiveIntegerField()   #проходная оценка
    duration = models.DurationField()   #продолжительность

    def __str__(self):
        return self.title


class Certificate(models.Model):       #модели сертификатов
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateField(auto_now_add=True) #выпущено в
    certificate_url = models.URLField()

    def __str__(self):
        return f"{self.student} - {self.course}"


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f"Отзыв от {self.user} для {self.course}"


class Subscription(models.Model):             #модели подписки
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} подписался на {self.course}"


class Payment(models.Model):               #модели оплаты
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  #сумма
    payment_date = models.DateTimeField(auto_now_add=True)
    STATUS_PAYMENT = (
        ('успешно', 'успешно'),
        ('неуспешно', 'неуспешно')
    )
    status = models.CharField(max_length=32, choices=STATUS_PAYMENT)

    def __str__(self):
        return f"Оплата по {self.user} для {self.course}"


class Webinar(models.Model):            #модели вебинары
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='webinars')
    title = models.CharField(max_length=52)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    link = models.URLField() #ссылка

    def __str__(self):
        return f"Вебинар: {self.title} для {self.course}"

