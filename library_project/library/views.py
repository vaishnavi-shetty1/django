from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Book, IssueBook, Member
from .forms import RegisterForm

def book_list(request):
    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'library/book_list.html', {'books': books})

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'library/book_detail.html', {'book': book})

@login_required
def issue_book(request, id):
    book = get_object_or_404(Book, id=id)

    member, created = Member.objects.get_or_create(user=request.user)

    IssueBook.objects.create(
        book=book,
        member=member
    )
    book.available_copies -= 1
    book.save() 
    return redirect('my_books')

@login_required
def my_books(request):
    issues = IssueBook.objects.filter(member=request.user.member, returned=False)
    return render(request, 'library/my_books.html', {'issues': issues})

@login_required
def return_book(request, id):
    issue = get_object_or_404(IssueBook, id=id)

    issue.returned = True
    issue.book.available_copies += 1
    issue.book.save()
    issue.save()

    return redirect('my_books')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Member.objects.create(user=user)
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'library/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('book_list')
    else:
        form = AuthenticationForm()

    return render(request, 'library/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')