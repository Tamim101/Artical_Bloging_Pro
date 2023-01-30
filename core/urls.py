from django.urls import path


from . import views


urlpatterns = [
    path('', views.Home, name='home'),
     path('blog/', views.Blog, name='blog'),
     path('single-blog/<str:pk>/', views.singel_blog, name='singel_blog'),
    path('login/', views.login, name='login'),
     path('about/', views.about_us, name='about'),
    # Admin 
        path('index/', views.index, name='index'),
        path('logoutuser/', views.logoutuser, name='logoutuser'),
        path('user/', views.user, name='user'),
         path('get_blog_post/', views.get_blog_post, name='get_blog_post'),
        path('deleteUser/<int:pk>', views.deleteUsers, name='deleteUser'),
            path('create_post/', views.create_post, name='create_post'),
            path('delete_blog/<int:pk>', views.delete_blog, name='delete_blog'),
            # path('edit_blog/<int:pk>', views.edit_blog, name='edit_blog'),
               path('sing_up/', views.sing_up, name='sing_up'),
                path('team/', views.our_Team, name='team'),
                     path('our_team_list/', views.our_Team_list, name='our_Team_list'),
                      path('delete_team/<int:pk>', views.delete_team, name='delete_team'),
                       path('create_team/', views.create_team, name='create_team'),
                        path('inx/', views.inx, name='inx'),
]