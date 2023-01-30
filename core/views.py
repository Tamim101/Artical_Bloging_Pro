from django.shortcuts import render
from django.contrib import auth
from core.models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# Create your views here.
def Home(request):
    allTeam = ourTeam.objects.all()
    return render(request,'onepage-slider.html' ,{'allTeam': allTeam})

def Blog(request):
    blog = blog_model.objects.all().order_by('-create_at')
    return render(request,'blog.html',{"blog":blog})

def singel_blog(request,pk):
    blog = blog_model.objects.get(id=pk)
    obj = blog_model.objects.all().order_by('-create_at')
    return render(request,'single-post.html',{"blog":blog,'obj':obj})


def login(request):
    if request.method == 'POST':

        email = request.POST['email']

        print(email)
        password = request.POST['password']
        if email and password:
           user = auth.authenticate(email=email,password=password)
           print(user,'jhsdbfjhbsdfhb')
           if user:
              if user.is_active:
                 auth.login(request, user)
                 context = {
                    'authMsg': 'login',
                    'context_instance': request
                }
                 return render(request, 'admin_panel/templates/index.html', context)

        return render(request, 'login.html')

    return render(request, 'login.html')


# Admin
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='login/')
def index(request):
    return render(request,'admin_panel/templates/index.html')


@staff_member_required(login_url='login/')
def logoutuser(request):
    if request.method == "POST":
        auth.logout(request)
        trashOldMsg(request)
        messages.success(request, 'Log Out successful')
        context = {
            'authMsg': 'logout',
        }
        return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


@staff_member_required(login_url='login/')
def user(request):
    alluser = User.object.all().order_by('-create_at')
    # userName = currentUser(request)
    return render(request, 'admin_panel/templates/user.html', {'all_user': alluser})



def new_user(request):
    return render(request, 'new-user.html')


@staff_member_required(login_url='login/')
def deleteUsers(request, pk):
    try:
        deletedUser =  User.object.get(id=pk)
        if deletedUser.is_staff != True:
            deletedUser.delete()
        alluser = User.object.all().order_by('-create_at')

        return render(request, 'admin_panel/templates/user.html', {'all_user': alluser})
    except:
        alluser = User.object.all().order_by('-create_at')

        return render(request, 'admin_panel/templates/user.html', {'all_user': alluser })



def create_post(request):
            return render(request, 'admin_panel/templates/createpost.html')

# from django.core.files.images import get_image_dimensions
@staff_member_required(login_url='login/')
def create_post(request):
    if request.method == 'GET':
        all_post = blog_model.objects.all().order_by('-create_at')

        return render(request, 'admin_panel/templates/createpost.html', {'all_post': all_post})
    else:
        topic = request.POST['topic']
        title = request.POST['title']
        short_description = request.POST['short_description']
        description = request.POST['description']
        thumbnail = request.FILES.get('thumbnail')
        # w, h = get_image_dimensions(thumbnail)
        # if w == 301 & h == 168:
        #     print(w, h)
        # else:
        #     trashOldMsg(request)
        #     messages.error(request, "Image size should be 300px width * 300px height")
        #     print('unsuccessful')
        #     return render(request, 'admin_panel/templates/createpost.html')

        create_blog = blog_model(

            title=title,
            description=description,
            topic=topic,
            short_description=short_description,
            thumbnail=thumbnail,


        )
        try:
            create_blog.save()
            trashOldMsg(request)
            messages.success(request, "Blog Create Successful")
            print('successful')
            all_blog = blog_model.objects.all().order_by('-created_at')
            return render(request, 'admin_panel/templates/createpost.html', {'all_blog': all_blog})
        except:
            return render(request, 'admin_panel/templates/createpost.html')

    return render(request, 'admin_panel/templates/createpost.html')


from django.core.files.storage import FileSystemStorage

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    print(filesize)
    print(fieldfile_obj.file._height)
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

@staff_member_required(login_url='login/')
def get_blog_post(request):
    blog = blog_model.objects.all().order_by('-create_at')
    return render(request,'admin_panel/templates/lost_blog.html',{'blog':blog})



@staff_member_required(login_url='login/')
def delete_blog(request, pk):
    try:
        # deletedblog = get(id=pk)

        # deletedblog.delete()
        blog = blog_model.objects.get(id=pk)
        blog.delete()

        return render(request,'admin_panel/templates/lost_blog.html',{'blog':blog})

    except:
        blog = blog_model.objects.all()

        return render(request,'admin_panel/templates/lost_blog.html',{'blog':blog})
@staff_member_required(login_url='login/')
def sing_up(request):
    if request.method == 'GET':
        print('nothing')
        all_user = User.object.all()
        print(all_user)
        return render(request, 'admin_panel/templates/sign_up.html')
    else:
        print("how")
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        con_password = request.POST['password2']

        if len(password) > 4:
            if password == con_password:
                create_user = User(username=username, email=email, password=password)
                create_user.password = make_password(create_user.password)
                if User.object.filter(email=email).exists():
                    trashOldMsg(request)
                    messages.error(request, 'Your email is already used.')
                    return render(request, 'admin_panel/templates/login.html')
                elif User.object.filter(username=username).exists():
                    trashOldMsg(request)
                    messages.error(request, 'Your email is already username.')

                    return render(request, 'admin_panel/templates/sign_up.html')
                else:
                    trashOldMsg(request)
                    messages.success(request, 'Account Create Successful')
                    create_user.save()
                print('password action')

            else:
                print('password not match.')
                trashOldMsg(request)
                messages.error(request, 'Password not match')
                return render(request, 'admin_panel/templates/sign_up.html')

        return render(request, 'admin_panel/templates/sign_up.html')
def trashOldMsg(req):
    storage = messages.get_messages(req)
    storage.user = True
    for _ in storage:
        pass
    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]



def our_Team(request):
    if request.method == 'GET':
        trashOldMsg(request)
        allTeam = ourTeam.objects.all()

        return render(request, 'team.html', {'allTeam': allTeam})
    else:

        try:
            name = request.POST['name']
            rank = request.POST['rank']
            img = request.FILES['image']
            facebook = request.POST['facebook']
            google = request.POST['google']
            twitter = request.POST['twitter']
            whatapp = request.POST['whatapp']
            w, h = get_image_dimensions(request.FILES['image'])
            print(w, h)
            if w == 370:
                if h == 393:
                    print('done')
                else:

                    trashOldMsg(request)
                    messages.error(request, 'Image size should be 370px width * 393px height.')
                    return render(request, 'team.html')
            else:
                trashOldMsg(request)
                messages.error(request, 'Image size should be 370px width * 600px height.')
                return render(request, 'team.html')
            createTeam = ourTeam(name=name, rank=rank, image=img,facebook=facebook,google=google,whatapp=whatapp,twitter=twitter)
            createTeam.save()
            trashOldMsg(request)
            messages.success(request, 'Team Created Successful')
            allTeam = ourTeam.objects.all()
            return render(request, 'our_team.html', {'allTeam': allTeam})
        except:
            trashOldMsg(request)
            messages.error(request, 'Team Created Unsuccessful')
            return render(request, 'team.html')

@staff_member_required(login_url='login/')
def our_Team_list(request):
    allTeam = ourTeam.objects.all()

    return render(request, 'admin_panel/templates/our_team.html', {'allTeam': allTeam})

@staff_member_required(login_url='login/')
def delete_team(request, pk):
    try:
        # deletedblog = get(id=pk)

        # deletedblog.delete()
        allTeam = ourTeam.objects.get(id=pk)
        allTeam.delete()

        return render(request,'admin_panel/templates/our_team.html',{'allTeam':allTeam})

    except:
        allTeam = ourTeam.objects.all()
        return render(request,'admin_panel/templates/our_team.html',{'allTeam':allTeam})


@staff_member_required(login_url='login/')

def create_team(request):
    if request.method == 'GET':
        trashOldMsg(request)
        allTeam = ourTeam.objects.all()

        return render(request, 'admin_panel/templates/team_create.html', {'allTeam': allTeam})
    else:

        try:
            name = request.POST['name']
            rank = request.POST['rank']
            image = request.FILES['image']
            facebook = request.POST['facebook']
            google = request.POST['google']
            twitter = request.POST['twitter']
            whatapp = request.POST['whatapp']
            # w, h = get_image_dimensions(request.FILES['image'])
            # print(w, h)
            # if w == 370:
            #     if h == 393:
            #         print('done')
            #     else:

            #         trashOldMsg(request)
            #         messages.error(request, 'Image size should be 370px width * 393px height.')
            #         return render(request, 'admin_panel/templates/team_create.html')
            # else:
            #     trashOldMsg(request)
            #     messages.error(request, 'Image size should be 370px width * 600px height.')
            #     return render(request, 'admin_panel/templates/team_create.html')
            createTeam = ourTeam(name=name, rank=rank, image=image,facebook=facebook,google=google,whatapp=whatapp,twitter=twitter)
            createTeam.save()
            trashOldMsg(request)
            messages.success(request, 'Team Created Successful')
            allTeam = ourTeam.objects.all()
            return render(request, 'admin_panel/templates/team_create.html', {'allTeam': allTeam})
        except:
            trashOldMsg(request)
            messages.error(request, 'Team Created Unsuccessful')
            return render(request, 'admin_panel/templates/team_create.html')


# from django.core.mail import send_mail
# from django.conf.global_settings import EMAIL_HOST_USER
# def send_email(request):
#     print('working')
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         note = request.POST['note']
#         number = request.POST['number']
#         if name and email and note and number:

#             print('email')
#             email = send_mail(' from :{}'.format(email), 'Hey, it\'s {}. Phone Number: {} '.format(name, number) + note,
#                               EMAIL_HOST_USER, ['tamimkhan7133@gmail.com', ], fail_silently=False)
#             print(email)

#             return render(request, 'onepage-slider.html')

#         else:
#             return render(request, 'onepage-slider.html')


def about_us(request):
    allTeam = ourTeam.objects.all()
    return render(request,'about.html' ,{'allTeam': allTeam})


def inx(request):
    
    return render(request,'index.html')

