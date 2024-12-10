from rest_framework import permissions

class CheckCreateCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'преподаватель'   #Только преподаватель может create курсы

class CheckTeacherCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Преподаватель может просматривать все курсы
        return obj.created_by == request.user  # Только владелец курса может его create/delete



class CheckCreateAssignment(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'преподаватель'  # Только преподаватели могут создавать задания

class CheckTeacherAssignmentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Преподаватель гана баардык заданияларды коро алат
        return obj.course.created_by == request.user  # Только владелец курса озгорто алат



class CheckCreateExam(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'преподаватель'  #преподаватель гана создавать эте алат экзаменди клиентке доступ жок

class CheckTeacherExamOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Преподаватель экзамендерди коро алат
        return obj.course.created_by == request.user  # курстун владелецине эле доступ берилет озгортконго




class TeacherReview(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:     # Преподаватель может только просматривать отзывы
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:     # Преподаватель может просматривать отзывы на свои курсыноне редактировать
            return obj.course.created_by == request.user  # Проверкачто преподаватель создал курс
        return False

#-----------------------student-----------------------

# class IsStudent(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'клиент'
#                                             #	Просмотр доступных курсов.
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return False


#    Прохождение курсов и сдача экзаменов.
class StudentLesson(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == 'клиент'  # Проверяем что пользователь студент и курс доступен ему

class StudentExam(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == 'клиент'  # Проверяем, что пользовательстудент и экзамен доступен ему

class StudentReview(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True     # Просмотр отзывов доступен всем
        return request.method == 'POST' and request.user.role == 'клиент'
        # Создание отзывов доступно только клиентам

class StudentCertificate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user      #Разрешить доступ только к сертификатам принадлежащим текущему студенту


