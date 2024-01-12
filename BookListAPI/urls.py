from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    #path('books/', views.books),
    path('books/', views.BookList.as_view(), name='books'),
    path('books/<int:pk>',views.Book.as_view()),
    path('menu-items/',views.MenuItemView.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItemView.as_view()),
    path('menu-items-view/',views.menu_items),
    path('menu-items-view/<int:pk>',views.single_item),
    path('secret/',views.secret), # token class path
    path('api-token-auth/', obtain_auth_token), # token function path, this method only accept http post call
    path('me',views.me),
    path('manager_view/', views.manager_view),
    path('throttle-check', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth),
    path('groups/manager/users/', views.manager),

    path('ratings', views.RatingsView.as_view()),
    #path('category/<int:pk>',views.category_detail, name='category-detail')#Display a related model fields field as a hyperlink 

]