from django.shortcuts import render, redirect
from django.template import loader
from api import news_all as news
from django.contrib.auth.decorators import login_required
from .models import Interest
from api import user_specific
from django.contrib import messages
from users import views as user_views


def index(request):
    top_news = news.get_all()
    sources = news.get_source()
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    languages = ({'name': 'Arabic', 'id': 'ar'}, {'name': 'German', 'id': 'de'}, {'name': 'English', 'id': 'en'},
                 {'name': 'Spanish', 'id': 'es'}, {'name': 'French', 'id': 'fr'}, {'name': 'Hebrew', 'id': 'he'},
                 {'name': 'Italian', 'id': 'it'}, {'name': 'Dutch', 'id': 'nl'}, {'name': 'Norwegian', 'id': 'no'},
                 {'name': 'Portuguese', 'id': 'po'},
                 {'name': 'Russian', 'id': 'ru'}, {'name': 'Northern Sami', 'id': 'se'}, {'name': 'Udmurt', 'id': 'ud'},
                 {'name': 'Chinese', 'id': 'zh'},
                 )
    if request.user.is_authenticated:
        check = user_views.check_paid(request)
        if check is not None:
            context = {'news': top_news['articles'], 'status_check': check.status, 'sources': sources,
                       'categories': categories, 'languages': languages}
            return render(request, 'index.html', context)
        else:
            context = {'news': top_news['articles'], 'sources': sources, 'categories': categories,
                       'languages': languages}
            return render(request, 'index.html', context)
    else:
        context = {'news': top_news['articles']}
        return render(request, 'index.html', context)


@login_required
def personal(request):
    users = request.user
    check = Interest.objects.filter(user=users).exists()
    top_news = news.get_all()
    sources = news.get_source()
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    languages = ({'name': 'Arabic', 'id': 'ar'}, {'name': 'German', 'id': 'de'}, {'name': 'English', 'id': 'en'},
                 {'name': 'Spanish', 'id': 'es'}, {'name': 'French', 'id': 'fr'}, {'name': 'Hebrew', 'id': 'he'},
                 {'name': 'Italian', 'id': 'it'}, {'name': 'Dutch', 'id': 'nl'}, {'name': 'Norwegian', 'id': 'no'},
                 {'name': 'Portuguese', 'id': 'po'},
                 {'name': 'Russian', 'id': 'ru'}, {'name': 'Northern Sami', 'id': 'se'}, {'name': 'Udmurt', 'id': 'ud'},
                 {'name': 'Chinese', 'id': 'zh'},
                 )
    if check:
        interest = Interest.objects.get(user=users)
        cat = interest.category
        sou = interest.sources
        results = user_specific.personal(sou)
        user_cat_news = {}
        for cats in cat.split(','):
            temp = (news.category(cats, 10))
            user_cat_news[cats] = temp['articles']
        if results:
            return render(request, 'personal.html',
                          {'context': results, 'cat': cat.split(','), 'sou': sou, 'news': top_news['articles'],
                           'cat_news': user_cat_news, 'sources': sources, 'categories': categories,
                           'languages': languages})
        else:
            return render(request, 'personal.html', {'context': 'error'})
    else:
        return render(request, 'personal.html', {'context': 'error'})


@login_required
def edit(request):
    users = request.user
    check = Interest.objects.filter(user=users).exists()
    if check:
        interest = Interest.objects.get(user=users)
        user_category = interest.category
        user_sources = interest.sources
    else:
        user_sources = ''
        user_category = ''

    top_news = news.get_all()
    sources = news.get_source()
    all_category = ['business', 'health', 'general', 'science', 'sports', 'technology', 'entertainment']
    languages = ({'name': 'Arabic', 'id': 'ar'}, {'name': 'German', 'id': 'de'}, {'name': 'English', 'id': 'en'},
                 {'name': 'Spanish', 'id': 'es'}, {'name': 'French', 'id': 'fr'}, {'name': 'Hebrew', 'id': 'he'},
                 {'name': 'Italian', 'id': 'it'}, {'name': 'Dutch', 'id': 'nl'}, {'name': 'Norwegian', 'id': 'no'},
                 {'name': 'Portuguese', 'id': 'po'},
                 {'name': 'Russian', 'id': 'ru'}, {'name': 'Northern Sami', 'id': 'se'}, {'name': 'Udmurt', 'id': 'ud'},
                 {'name': 'Chinese', 'id': 'zh'},
                 )
    return render(request, 'customize.html',
                  {'news': top_news['articles'], 'sources': sources, 'user_source': user_sources,
                   'user_category': user_category, 'all_category': all_category,  'languages': languages})


@login_required
def submit_source(request):
    users = request.user
    check = Interest.objects.filter(user=users).exists()
    if check:
        interest = Interest.objects.get(user=users)
        user_source = interest.sources
        if request.POST['source_id'] in user_source:
            messages.info(request, 'Source Already Selected')
            return redirect('edit')
        else:
            user_source = user_source + ',' + request.POST['source_id']
            update = Interest.objects.get(user=users)
            update.sources = user_source
            update.save()
            messages.success(request, 'Source Updated SuccessFully')
            return redirect('edit')
    else:
        insert = Interest(sources=request.POST['source_id'], user=users)
        insert.save()
        messages.success(request, 'Source Successfully Updated')
        return redirect('edit')


@login_required
def submit_category(request):
    users = request.user
    check = Interest.objects.filter(user=users).exists()
    if check:
        interest = Interest.objects.get(user=users)
        user_category = interest.category
        if request.POST['category_id'] in user_category:
            messages.info(request, 'Category Already Selected')
            return redirect('edit')
        else:
            user_category = user_category + ',' + request.POST['category_id']
            update = Interest.objects.get(user=users)
            update.category = user_category
            update.save()
            messages.success(request, 'Category Updated SuccessFully')
            return redirect('edit')
    else:
        insert = Interest(sources=request.POST['category_id'], user=users)
        insert.save()
        messages.success(request, 'Category Successfully Updated')
        return redirect('edit')


@login_required
def search(request):
    top_news = news.get_all()
    data = news.query(request.POST['query'])
    sources = news.get_source()
    check = user_views.check_paid(request)
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    languages = ({'name': 'Arabic', 'id': 'ar'}, {'name': 'German', 'id': 'de'}, {'name': 'English', 'id': 'en'},
                 {'name': 'Spanish', 'id': 'es'}, {'name': 'French', 'id': 'fr'}, {'name': 'Hebrew', 'id': 'he'},
                 {'name': 'Italian', 'id': 'it'}, {'name': 'Dutch', 'id': 'nl'}, {'name': 'Norwegian', 'id': 'no'},
                 {'name': 'Portuguese', 'id': 'po'},
                 {'name': 'Russian', 'id': 'ru'}, {'name': 'Northern Sami', 'id': 'se'}, {'name': 'Udmurt', 'id': 'ud'},
                 {'name': 'Chinese', 'id': 'zh'},
                 )

    return render(request, 'search.html',
                  {'news': top_news['articles'], 'query': data['articles'], 'key': request.POST['query'],
                   'sources': sources,
                   'categories': categories, 'languages': languages, 'status_check': check.status
                   })


@login_required
def pricing(request):
    if request.method == 'GET':
        sources = news.get_source()
        check = user_views.check_paid(request)
        categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
        languages = ({'name': 'Arabic', 'id': 'ar'}, {'name': 'German', 'id': 'de'}, {'name': 'English', 'id': 'en'},
                     {'name': 'Spanish', 'id': 'es'}, {'name': 'French', 'id': 'fr'}, {'name': 'Hebrew', 'id': 'he'},
                     {'name': 'Italian', 'id': 'it'}, {'name': 'Dutch', 'id': 'nl'}, {'name': 'Norwegian', 'id': 'no'},
                     {'name': 'Portuguese', 'id': 'po'},
                     {'name': 'Russian', 'id': 'ru'}, {'name': 'Northern Sami', 'id': 'se'},
                     {'name': 'Udmurt', 'id': 'ud'},
                     {'name': 'Chinese', 'id': 'zh'},
                     )

        if request.user.is_authenticated:
            check = user_views.check_paid(request)
            if check is not None:
                context = {'status_check': check.status, 'sources': sources,
                           'categories': categories, 'languages': languages, 'status_check': check.status}
                return render(request, 'pricing.html', context)
            else:

                return render(request, 'login.html', {})
        else:
            context = {}
            return render(request, 'login.html', context)
    else:
        pass


@login_required
def source_selected(request):
    top_news = news.get_all()
    sources = news.get_source()
    check = user_views.check_paid(request)
    source_selected_news = news.source_selected(request.GET['source_id'])
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    languages = ({'name': 'Arabic', 'id': 'ar'}, {'name': 'German', 'id': 'de'}, {'name': 'English', 'id': 'en'},
                 {'name': 'Spanish', 'id': 'es'}, {'name': 'French', 'id': 'fr'}, {'name': 'Hebrew', 'id': 'he'},
                 {'name': 'Italian', 'id': 'it'}, {'name': 'Dutch', 'id': 'nl'}, {'name': 'Norwegian', 'id': 'no'},
                 {'name': 'Portuguese', 'id': 'po'},
                 {'name': 'Russian', 'id': 'ru'}, {'name': 'Northern Sami', 'id': 'se'}, {'name': 'Udmurt', 'id': 'ud'},
                 {'name': 'Chinese', 'id': 'zh'},
                 )
    if source_selected_news:
        return render(request, 'source_selected.html',
                      {'news': top_news['articles'], 'source_news': source_selected_news,
                       'source_selected': source_selected_news[0]['source']['name'], 'sources': sources,
                       'categories': categories, 'languages': languages, 'status_check': check.status})

    else:

        return render(request, 'source_selected.html',
                      {'news': top_news['articles'], 'source_news': source_selected_news,
                       'source_selected': False,
                       'sources': sources, 'categories': categories, 'languages': languages,
                       'check_status': check.status})


@login_required
def category_selected(request):
    top_news = news.get_all()
    sources = news.get_source()
    check = user_views.check_paid(request)
    category_news = news.category_selected(request.GET['category_name'])
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    languages = ({'name': 'Arabic', 'id': 'ar'}, {'name': 'German', 'id': 'de'}, {'name': 'English', 'id': 'en'},
                 {'name': 'Spanish', 'id': 'es'}, {'name': 'French', 'id': 'fr'}, {'name': 'Hebrew', 'id': 'he'},
                 {'name': 'Italian', 'id': 'it'}, {'name': 'Dutch', 'id': 'nl'}, {'name': 'Norwegian', 'id': 'no'},
                 {'name': 'Portuguese', 'id': 'po'},
                 {'name': 'Russian', 'id': 'ru'}, {'name': 'Northern Sami', 'id': 'se'}, {'name': 'Udmurt', 'id': 'ud'},
                 {'name': 'Chinese', 'id': 'zh'},
                 )
    if category_news:
        return render(request, 'category_selected.html',
                      {'news': top_news['articles'], 'category_news': category_news, 'sources': sources,
                       'category_selected': request.GET['category_name'], 'categories': categories,
                       'languages': languages, 'status_check': check.status})

    else:
        return render(request, 'category_selected.html',
                      {'news': top_news['articles'],
                       'category_selected': False,
                       'sources': sources, 'categories': categories})


@login_required
def language_selected(request):
    top_news = news.get_all()
    sources = news.get_source()
    check = user_views.check_paid(request)
    language_selected_news = news.language_selected(request.GET['language_id'])

    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    languages = ({'name': 'Arabic', 'id': 'ar'}, {'name': 'German', 'id': 'de'}, {'name': 'English', 'id': 'en'},
                 {'name': 'Spanish', 'id': 'es'}, {'name': 'French', 'id': 'fr'}, {'name': 'Hebrew', 'id': 'he'},
                 {'name': 'Italian', 'id': 'it'}, {'name': 'Dutch', 'id': 'nl'}, {'name': 'Norwegian', 'id': 'no'},
                 {'name': 'Portuguese', 'id': 'po'},
                 {'name': 'Russian', 'id': 'ru'}, {'name': 'Northern Sami', 'id': 'se'}, {'name': 'Udmurt', 'id': 'ud'},
                 {'name': 'Chinese', 'id': 'zh'},
                 )

    return render(request, 'language_selected.html',
                  {'news': top_news['articles'], 'status_check': check.status, 'sources': sources,
                   'categories': categories, 'languages': languages, 'check_status': check.status,
                   'language_news': language_selected_news, 'selected_language': request.GET['language_id']})


def unauth_pricing(request):
    return render(request,'unauth_pricing.html',{})