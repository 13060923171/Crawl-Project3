from django.contrib import admin
from studentManagement.models import StudentInformationModel, CourseModel, StudentModel
# Register your models here.

class StudentInformationLine(admin.TabularInline):
    model = CourseModel
    extra = 3


class StudentInformationAdmin(admin.ModelAdmin):
    # 显示的字段，先后顺序表示显示顺序
    list_display = ['stu_id', 'stu_name', 'stu_phone', 'str_addr', 'stu_faculty', 'stu_major']
    # 以哪个来过滤
    list_filter = ['stu_id', 'stu_name']
    # 以哪个字段来搜索，admin中就会出现一个搜索栏
    search_fields = ['stu_name', 'str_addr', 'stu_faculty', 'stu_major']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['cour_id', 'course', 'grade']
    # inlines = [StudentInformationLine, ]  # 谁的外键就写在哪边

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'stu_id', 'username', 'password']
    search_fields = ['stu_id', 'username']

admin.site.register(StudentInformationModel, StudentInformationAdmin)
admin.site.register(CourseModel, CourseAdmin)
admin.site.register(StudentModel, StudentAdmin)
