from django.shortcuts import render

from books.models import Book


def books_view(request, pub_date=None):
    prev_date = None
    next_date = None

    if pub_date is not None:
        if hasattr(pub_date, 'date'):
            pub_date = pub_date.date()
        books = Book.objects.filter(pub_date=pub_date)
        dates = list(Book.objects.dates('pub_date', 'day', order='ASC'))
        if pub_date in dates:
            index = dates.index(pub_date)
            if index > 0:
                prev_date = dates[index - 1]
            if index < len(dates) - 1:
                next_date = dates[index + 1]
    else:
        books = Book.objects.all()

    context = {
        'books': books,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    return render(request, 'books/books_list.html', context)
