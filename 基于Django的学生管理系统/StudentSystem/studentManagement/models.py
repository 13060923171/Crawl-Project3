from django.db import models

# Create your models here.
# 课程表
class CourseModel(models.Model):
    cour_id = models.CharField(max_length=15, verbose_name='学生ID')
    course = models.CharField(max_length=30, verbose_name='课程')
    grade = models.IntegerField(default=60, verbose_name='分数')
    class Meta():
        db_table = 'course'
    def __str__(self):
        return '学生Id：  课程：  分数： '.format(self.cour_id, self.course, self.grade)

# 学生信息表
class StudentInformationModel(models.Model):
    stu_id = models.CharField(max_length=15, verbose_name='学生ID')
    stu_name = models.CharField(max_length=30, verbose_name='学生姓名')
    stu_phone = models.CharField(max_length=20, verbose_name='学生电话')
    str_addr = models.TextField(verbose_name='学生地址')
    stu_faculty = models.CharField(max_length=20, verbose_name='院系')
    stu_major = models.CharField(max_length=30, verbose_name='专业')
    # 取消外键（外键是可用的）
    # stu_course = models.ForeignKey('CourseModel', on_delete=True)
    class Meta():
        db_table = 'studentinformation'

# 学生用户名密码表
class StudentModel(models.Model):
    stu_id = models.CharField(max_length=15, verbose_name='学生ID')
    username = models.CharField(max_length=10, verbose_name='用户名')
    password = models.CharField(max_length=10, verbose_name='密码')
    class Meta():
        db_table = 'student'

