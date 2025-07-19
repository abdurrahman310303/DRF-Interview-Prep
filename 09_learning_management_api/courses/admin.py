from django.contrib import admin
from .models import (
    Category, Instructor, Course, Lesson, Enrollment, LessonProgress,
    Quiz, Question, Answer, QuizAttempt, Assignment, Submission,
    CourseReview, Certificate
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'expertise', 'years_experience', 'rating', 'is_active']
    list_filter = ['is_active', 'years_experience', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'expertise']
    readonly_fields = ['rating', 'created_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'user__first_name'


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ['title', 'lesson_type', 'duration_minutes', 'order', 'is_free_preview']
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'difficulty_level', 'price', 'status', 'rating']
    list_filter = ['difficulty_level', 'status', 'category', 'is_free', 'created_at']
    search_fields = ['title', 'description', 'instructor__user__first_name', 'instructor__user__last_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['rating', 'created_at', 'updated_at']
    inlines = [LessonInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'instructor', 'category')
        }),
        ('Course Details', {
            'fields': ('difficulty_level', 'duration_hours', 'prerequisites', 'learning_objectives')
        }),
        ('Media', {
            'fields': ('thumbnail', 'preview_video')
        }),
        ('Pricing & Access', {
            'fields': ('price', 'is_free', 'max_students')
        }),
        ('Status', {
            'fields': ('status', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'lesson_type', 'duration_minutes', 'order', 'is_free_preview']
    list_filter = ['lesson_type', 'is_free_preview', 'course__category']
    search_fields = ['title', 'content', 'course__title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['course', 'order']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'progress_percentage', 'status']
    list_filter = ['status', 'enrollment_date', 'course__category']
    search_fields = ['student__username', 'student__email', 'course__title']
    readonly_fields = ['enrollment_date', 'completion_date']
    ordering = ['-enrollment_date']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['get_student', 'lesson', 'is_completed', 'completion_date', 'time_spent_minutes']
    list_filter = ['is_completed', 'completion_date']
    search_fields = ['enrollment__student__username', 'lesson__title']
    
    def get_student(self, obj):
        return obj.enrollment.student.username
    get_student.short_description = 'Student'
    get_student.admin_order_field = 'enrollment__student__username'


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz__lesson__course']
    search_fields = ['question_text', 'quiz__title']
    inlines = [AnswerInline]
    ordering = ['quiz', 'order']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'time_limit_minutes', 'passing_score', 'max_attempts']
    list_filter = ['passing_score', 'lesson__course__category']
    search_fields = ['title', 'instructions', 'lesson__title']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'max_score', 'passed', 'completed_at']
    list_filter = ['passed', 'started_at', 'quiz__lesson__course']
    search_fields = ['student__username', 'quiz__title']
    readonly_fields = ['started_at', 'completed_at']
    ordering = ['-started_at']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'due_date', 'max_points', 'submission_format']
    list_filter = ['due_date', 'lesson__course__category']
    search_fields = ['title', 'description', 'lesson__title']
    ordering = ['due_date']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'submitted_at', 'grade', 'status']
    list_filter = ['status', 'submitted_at', 'assignment__lesson__course']
    search_fields = ['student__username', 'assignment__title']
    readonly_fields = ['submitted_at']
    ordering = ['-submitted_at']


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'course__category']
    search_fields = ['student__username', 'course__title', 'review_text']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['get_student', 'get_course', 'certificate_id', 'issued_date', 'is_valid']
    list_filter = ['is_valid', 'issued_date']
    search_fields = ['certificate_id', 'enrollment__student__username', 'enrollment__course__title']
    readonly_fields = ['certificate_id', 'issued_date']
    
    def get_student(self, obj):
        return obj.enrollment.student.username
    get_student.short_description = 'Student'
    get_student.admin_order_field = 'enrollment__student__username'
    
    def get_course(self, obj):
        return obj.enrollment.course.title
    get_course.short_description = 'Course'
    get_course.admin_order_field = 'enrollment__course__title'
