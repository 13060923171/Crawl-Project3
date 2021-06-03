from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import StudentModel, StudentInformationModel, CourseModel
# Create your views here.

# 主界面
def index(request):
    context = {
        'status': '未登录状态'
    }
    return render(request, 'studentManage/index.html', context)

# 登录界面
def login(request):
    if request.method == "POST":
        id = request.POST.get('id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([id, username, password]):
            return HttpResponse('参数不全')
        else:
            student = StudentModel.objects.filter(username=username, password=password)
            if len(student):
                # request.session['username'] = username
                # 用以下方法，将用户的信息存放到session中，session在中间件中是默认启用的
                request.session['user'] = {
                    'id': id,
                    'username': username,
                    'password': password
                }
                context = {
                    'status': username,
                    'aa': '已登录',
                    'lenght': 1
                }
                return render(request, 'studentManage/index.html', context)

            else:
                context = {
                    'aa': '用户名密码错误'
                }
                return render(request, 'studentManage/login.html', context)
    else:
        context = {
            'status': '未登录状态',
            'length': 0
        }
        return render(request, 'studentManage/login.html', context)

# 退出界面
def logout(request):
    # 注销掉用户，从删除session中保存的信息
    del request.session['user']
    return render(request, 'studentManage/index.html')

# 增加数据 增加只能root用户或者管理员才能操作
def add(request):
    if request.method == "POST":
        root_information = request.session['user']
        id = root_information['id']
        root_id = StudentModel.objects.get(pk=1).stu_id
        if id == root_id:
            stu_id = request.POST.get('stu_id')
            stu_name = request.POST.get('stu_name')
            if not all([stu_id, stu_name]):
                context = {
                    'msg': '学号和名字有遗漏',
                }
                return render(request, 'studentManage/add.html', context)
            stu_phone = request.POST.get('stu_phone')
            stu_addr = request.POST.get('str_addr')
            stu_faculty = request.POST.get('stu_faculty')
            stu_major = request.POST.get('stu_major')
            stu_data = StudentInformationModel()
            stu_data.stu_id = stu_id
            stu_data.stu_name = stu_name
            stu_data.stu_phone = stu_phone
            stu_data.str_addr = stu_addr
            stu_data.stu_faculty = stu_faculty
            stu_data.stu_major = stu_major
            stu_data.save()
            context = {
                'sucess': '增加成功',
            }
            return render(request, 'studentManage/add.html', context)
        else:
            context = {
                'error': '只用root用户和管理员才能操作'
            }
            return render(request, 'studentManage/add.html', context)
    else:
        return render(request, 'studentManage/add.html')


# 查询
def select(request):
    if request.method == "POST":
        id = request.POST.get('stu_id')
        stu_data = StudentInformationModel.objects.get(stu_id=id)
        stu_id = stu_data.stu_id
        stu_name = stu_data.stu_name
        stu_phone = stu_data.stu_phone
        str_addr = stu_data.str_addr
        stu_faculty = stu_data.stu_faculty
        stu_major = stu_data.stu_major
        stu_course = CourseModel.objects.filter(cour_id=id)
        dct = {}
        for stu in stu_course:
            dct[stu.course] = stu.grade
        context = {
            'stu_id': stu_id,
            'stu_name': stu_name,
            'stu_phone': stu_phone,
            'str_addr': str_addr,
            'stu_faculty': stu_faculty,
            'stu_major': stu_major,
            'course_data': dct,
            'msg': True
        }
        return render(request, 'studentManage/select.html', context)
    else:
        root_information = request.session['user']
        id = root_information['id']
        context = {
            'msg': False,
            'id': id
        }
        return render(request, 'studentManage/select.html', context)

# 删除
def delete(request):
    if request.method == "POST":
        id = request.POST.get('id')
        StudentInformationModel.objects.filter(stu_id=id).delete()
        context = {
            'msg': '成功删除'
        }
        return render(request, 'studentManage/delete.html', context)
    else:
        root_information = request.session['user']
        id = root_information['id']
        context = {
            'id': id
        }
        return render(request, 'studentManage/delete.html', context)


# 修改
def update(request):
    user_information = request.session['user']
    id = user_information['id']
    stu_data = StudentInformationModel.objects.get(stu_id=id)
    stu_id = stu_data.stu_id
    stu_name = stu_data.stu_name
    stu_phone = stu_data.stu_phone
    stu_addr = stu_data.str_addr
    stu_faculty = stu_data.stu_faculty
    stu_major = stu_data.stu_major
    context = {
        'stu_id': stu_id,
        'stu_name': stu_name,
        'stu_phone': stu_phone,
        'stu_addr': stu_addr,
        'stu_faculty': stu_faculty,
        'stu_major': stu_major,
    }
    if request.method == "POST":
        stu_id = request.POST.get('stu_id')
        stu_name = request.POST.get('stu_name')
        stu_phone = request.POST.get('stu_phone')
        stu_addr = request.POST.get('stu_addr')
        stu_faculty = request.POST.get('stu_faculty')
        stu_major = request.POST.get('stu_major')
        # StudentInformationModel.objects.filter(stu_id=id).update(stu_id=stu_id, stu_name=stu_name, stu_phone=stu_phone, str_addr=stu_addr, stu_faculty=stu_faculty, stu_major=stu_major)
        # 或者 以下这种，对单个数据进行修改
        stu_data = StudentInformationModel.objects.get(stu_id=id)
        stu_data.stu_id = stu_id
        stu_data.stu_name = stu_name
        stu_data.stu_phone = stu_phone
        stu_data.stu_addr = stu_addr
        stu_data.stu_faculty = stu_faculty
        stu_data.stu_major = stu_major
        stu_data.save()
        context = {
            'stu_id': stu_id,
            'stu_name': stu_name,
            'stu_phone': stu_phone,
            'stu_addr': stu_addr,
            'stu_faculty': stu_faculty,
            'stu_major': stu_major,
            'msg': '修改成功'
        }
        return render(request, 'studentManage/update.html', context)
    else:
        return render(request, 'studentManage/update.html', context)
