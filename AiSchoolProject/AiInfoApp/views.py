from django.shortcuts import render, redirect
from .models import AiClass, AiStudent, StudentPost
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.


def home(request):
    context = {
        'AiClass': AiClass.objects.all()
    }
    return render(request, 'home.html', context)


def detail(request, class_pk):
    context = {
        'class_obj': AiClass.objects.get(pk=class_pk)
    }
    return render(request, 'detail.html', context)


def add(request, student_pk):
    student = AiStudent.objects.get(pk=student_pk)
    if request.method == "POST":
        # StudentPost를 생성하는 것으로 변경
        StudentPost.objects.create(
            intro=request.POST['intro'],
            writer=student
        )
        return redirect('student', student_pk)
    return render(request, 'add.html')


def student(request, student_pk):
    student = AiStudent.objects.get(pk=student_pk)
    context = {
        'student': student
    }
    return render(request, 'student.html', context)


def edit(request, student_pk):
    if request.method == "POST":
        # 업데이트 하기. update()는 QuerySet에서만 동작
        target_student = AiStudent.objects.filter(pk=student_pk)
        target_student.update(
            name=request.POST['name'],
            phone_num=request.POST['phone_num'],
        )
        return redirect('student', student_pk)
    student = AiStudent.objects.get(pk=student_pk)
    context = {
        'student': student
    }
    return render(request, 'edit.html', context)


def delete(request, class_num, student_pk):
    target_student = AiStudent.objects.get(pk=student_pk)
    target_student.delete()

    class_pk = class_num

    return redirect('detail', class_pk)


ERROR_MSG = {
    'ID_EXIST': '이미 사용 중인 아이디입니다.',
    'ID_NOT_EXIST': '존재하지 않는 아이디입니다.',
    'ID_PW_MISSING': '아이디와 비밀번호를 다시 확인해주세요.',
    'PW_CHECK': '비밀번호가 일치하지 않습니다.',
}


def signup(request):
    context = {
        'error': {
            'state': False,
            'msg': ''
        }
    }
    if request.method == "POST":
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_pw_check = request.POST['user_pw_check']

        user_name = request.POST['user_name']
        phone_num = request.POST['phone_num']
        class_num = request.POST['class_num']

        target_class = AiClass.objects.get(class_num=class_num)

        if (user_id and user_pw):
            user = User.objects.filter(username=user_id)

            # 존재하지 않는 아이디라면 => 써도 되는 아이디
            if len(user) == 0:
                if user_pw == user_pw_check:
                    # 회원가입 진행
                    created_user = User.objects.create_user(
                        username=user_id,
                        password=user_pw
                    )
                    AiStudent.objects.create(
                        user=created_user,
                        participate_class=target_class,
                        name=user_name,
                        phone_num=phone_num
                    )

                    # 회원가입 했으면 자동으로 로그인까지 되어야지
                    auth.login(request, created_user)
                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            # 존재하는 아이디라면 => 쓸 수 없는 아이디
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'signup.html')


def login(request):
    context = {
        'error': {
            'state': False,
            'msg': ''
        }
    }

    if request.method == "POST":
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw):
            if len(user) != 0:

                user = auth.authenticate(
                    username=user_id,
                    password=user_pw
                )

                if user != None:
                    auth.login(request, user)
                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_NOT_EXIST']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']
    return render(request, 'login.html', context)


def logout(request):
    if request.method == "POST":
        auth.logout(request)
    return redirect('home')
