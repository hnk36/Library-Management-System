from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MemberForm
from django.http import HttpResponse
from .models import Genre, Book, BookCopy, Borrow, Member
from django.db.models import Count
from django.utils import timezone


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        messages.success(request, 'Your account has been created successfully.')
        return redirect('login')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('book_category')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')



def home(request):
    try:
        genres = Genre.objects.all()
        context = {
            'genres': genres
        }
    except Exception as e:
        print(f'An error occurred: {e}')
        return HttpResponse("An error occurred while fetching the genres.", status=500)
    else:
        return render(request, 'home.html', context)


@login_required
def books_views(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    books = Book.objects.filter(genre=genre)
    return render(request, 'book_list.html', {'genre': genre, 'books': books})


@login_required
def detail_views(request, book_id):
    books = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'books': books})


def register_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member registered successfully.')
            return redirect('book_category')  # Ensure 'home' is a valid URL name in your urls.py
    else:
        form = MemberForm()
    return render(request, 'member.html', {'form': form})

@login_required
def borrow_book(request, book_copy_id):
    book_copy = get_object_or_404(BookCopy, pk=book_copy_id)
    member = Member.objects.filter(email=request.user.email).first()

    if not member:
        messages.error(request, 'You must be registered as a member to borrow a book.')
        return redirect('register_member')

    if request.method == 'POST':
        try:
            if not book_copy.is_available():
                raise ValidationError("This book copy is not available for borrowing.")
            borrow = Borrow.objects.create(
                book_copy=book_copy,
                member=member,
                borrow_date=timezone.now(),
                return_date=timezone.now() + timezone.timedelta(days=14)  # Assuming a 2-week borrowing period
            )
            book_copy.status = 'checked_out'
            book_copy.save()
            messages.success(request, f'You have successfully borrowed {book_copy.book.title}.')
            return redirect('book_category')  # Ensure 'book_category' URL pattern exists
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('detail', book_id=book_copy.book.id)  # Redirect to book detail view

    return render(request, 'book_detail.html', {'book_copy': book_copy})

@login_required
def borrowed_member(request):
    borrow_record = Borrow.objects.select_related('book_copy', 'member').all()
    member_borrow_counts = Borrow.objects.values('member').annotate(borrow_count=Count('book_copy'))
    member_borrow_counts_dict = {item['member']: item['borrow_count'] for item in member_borrow_counts}
    for record in borrow_record:
        record.borrow_count = member_borrow_counts_dict.get(record.member.id, 0)

    return render(request, 'borrowing_member.html', {'borrow_record': borrow_record})

