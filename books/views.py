from .forms import BookForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Book, Category, UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import logout



def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        # แก้ไขข้อมูลของผู้ใช้และบันทึก
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')  # หรือไปหน้าอื่นหลังแก้ไขโปรไฟล์สำเร็จ
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'profile_form': profile_form})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'ชื่อผู้ใช้นี้ถูกใช้แล้ว')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'อีเมลนี้ถูกใช้แล้ว')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'ลงทะเบียนสำเร็จ')
                return redirect('login')  # หลังจากลงทะเบียนเสร็จ redirect ไปหน้า login
        else:
            messages.error(request, 'รหัสผ่านไม่ตรงกัน')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home-ld')  # ถ้าล็อกอินสำเร็จ นำผู้ใช้ไปยังหน้า home
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')

    return render(request, 'login.html')


def book_list(request):
    books = Book.objects.all()

    # นับจำนวนหนังสือตามหมวดหมู่
    categories = Category.objects.all()
    category_counts = []
    category_names = []

    for category in categories:
        count = Book.objects.filter(category=category).count()
        category_counts.append(count)
        category_names.append(category.name)

    context = {
        'books': books,
        'categories': category_names,  # ส่งชื่อหมวดหมู่
        'category_counts': category_counts  # ส่งจำนวนหนังสือตามหมวดหมู่
    }
    return render(request, 'book_list.html', context)

def home(request):
    return render(request, 'home.html')

def home_ld_view(request):
    return render(request, 'home-ld.html')

def profile(request):
    return render(request, 'profile.html')
@login_required
def novels(request):
    return render(request, 'novels.html')

@login_required
def comics(request):
    return render(request, 'comics.html')

@login_required
def exam_guides(request):
    return render(request, 'exam-guides.html')

@login_required
def investment(request):
    return render(request, 'investment.html')

@login_required
def law_books(request):
    return render(request, 'law-books.html')

@login_required
def management(request):
    return render(request, 'management.html')

@login_required
def loveordead(request):
    return render(request, 'loveordead.html')

@login_required
def ชีวิตนี้ข้าพอแล้ว(request):
    return render(request, 'ชีวิตนี้ข้าพอแล้ว.html')

@login_required
def ตำนานดาบและคทาแห่งวิสตอเรีย_6(request):
    return render(request, 'ตำนานดาบและคทาแห่งวิสตอเรีย 6.html')

@login_required
def add_book_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category_id = request.POST.get('category')
        published_year = request.POST.get('published_year')
        num_pages = request.POST.get('num_pages')
        cover_image = request.FILES.get('cover_image')

        category = Category.objects.get(id=category_id)
        new_book = Book(
            title=title,
            author=author,
            category=category,
            published_year=published_year,
            num_pages=num_pages,  # บันทึกข้อมูลจำนวนหน้า
            cover_image=cover_image
        )
        new_book.save()

        return redirect('book_list')  # หลังจากบันทึกแล้ว ให้ redirect ไปหน้า book_list

    categories = Category.objects.all()
    return render(request, 'add_book.html', {'categories': categories})


@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)  # แก้ไขข้อมูลหนังสือที่เลือก
        if form.is_valid():
            form.save()  # บันทึกการแก้ไข
            return redirect('book_list')  # เมื่อบันทึกสำเร็จ กลับไปที่หน้า book_list
        else:
            categories = Category.objects.all()  # แสดงฟอร์มที่มีข้อมูลเดิม
            return render(request, 'edit_book.html', {'form': form, 'categories': categories})

    else:
        form = BookForm(instance=book)
        categories = Category.objects.all()
        return render(request, 'edit_book.html', {'form': form, 'categories': categories})

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # กลับไปที่หน้ารายการหนังสือ

    return render(request, 'delete_book.html', {'book': book})

def profile(request):
    user_books = Book.objects.filter(added_by=request.user)  # ดึงหนังสือที่ผู้ใช้เพิ่ม
    return render(request, 'profile.html', {'user_books': user_books})