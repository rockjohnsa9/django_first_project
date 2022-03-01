from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateQueryset(request, queryset, results=3):
    page = request.GET.get('page')
    paginator = Paginator(queryset, results)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        queryset = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        queryset = paginator.page(page)

    return queryset, paginator
