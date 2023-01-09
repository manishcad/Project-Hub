from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def Paginator_function(model_obj, num_of_obj, page_num):
    page = Paginator(model_obj, num_of_obj)
    try:
        profiles = page.get_page(page_num)
    except PageNotAnInteger:
        profiles = page.get_page(1)
    except EmptyPage:
        profiles = page.get_page(page.num_pages)

    return profiles
