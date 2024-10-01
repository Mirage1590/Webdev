from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, register_view

urlpatterns = [
    path('', views.home, name='home'),
    path('home-ld/', views.home_ld_view, name='home-ld'),
    path('login/', login_view, name='login'),
    path('home-ld/novels/', views.novels, name='novels'),
    path('home-ld/novels/loveordead', views.loveordead, name='loveordead'),
    path('home-ld/novels/ชีวิตนี้ข้าพอแล้ว', views.ชีวิตนี้ข้าพอแล้ว, name='ชีวิตนี้ข้าพอแล้ว'),
    path('home-ld/novels/ตำนานดาบและคทาแห่งวิสตอเรีย 6', views.ตำนานดาบและคทาแห่งวิสตอเรีย_6, name='ตำนานดาบและคทาแห่งวิสตอเรีย 6'),
    path('home-ld/comics/', views.comics, name='comics'),
    path('home-ld/exam-guides/', views.exam_guides, name='exam-guides'),
    path('home-ld/law-books/', views.law_books, name='law-books'),
    path('home-ld/investment/', views.investment, name='investment'),
    path('home-ld/management/', views.management, name='management'),
    path('book_list/', views.book_list, name='book_list'),
    path('add/', views.add_book_view, name='add_book'),
    path('profile/', views.profile, name='profile'),
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('register/', register_view, name='register'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)