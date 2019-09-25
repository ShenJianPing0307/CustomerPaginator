
from app01.pager import Paginator as MyPaginator
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest

def BookList(request):

    book_queryset = models.Book.objects.all()
    count = book_queryset.count()
    current_page = request.GET.get("p")
    base_url = reverse("book_list")
    paginator = MyPaginator(count,current_page,base_url)
    data =  book_queryset[paginator.start_index:paginator.end_index]

    return render(request,'books2.html',locals())

