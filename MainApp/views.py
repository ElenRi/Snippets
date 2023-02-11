from django.http import Http404
from django.contrib import auth
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, CommentForm
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def snippets_page(request):
    lang = request.GET.get("lang")
    snippets = Snippet.objects.all()
    if lang:
        snippets = snippets.filter(lang=lang)
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'lang': lang
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    comment_form = CommentForm()
    context = {
        'pagename': 'Страница сниппета',
        'snippet': snippet,
        'comment_form': comment_form,
    }
    return render(request, 'pages/snippet_detail.html', context)

@login_required
def add_snippet_page(request):
    if request.method == "GET":  # нужна страница с формой
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', 'form': form}
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":  # получаем данные от формы
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect("snippet-list")

@login_required
def snippets_my(request):
    my_snippets = Snippet.objects.filter(user=request.user)
    context = {'pagename': 'Мои сниппеты', 'snippets': my_snippets}
    return render(request, 'pages/snippets.html', context)

def snippet_delete(request, snippet_id):
    snippet = Snippet.object.get(pk=snippet_id)
    snippet.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            snippet_id = request.POST['snippet_id']
            snippet = Snippet.objects.get(pk=snippet_id)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect(request.META.get('HTTP_REFERER', '/'))


def logout(request):
    auth.logout(request)
    return redirect('home')

# def snippet_create(request):
#     if request.method == "POST":
#         form_data = request.POST
#         snippet = Snippet(name=form_data["name"], lang=form_data["lang"], code=form_data["code"])
#         snippet.save()
#         return redirect('snippet-list')

# def snippet_create(request):
#    if request.method == "POST":
#        form = SnippetForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect("snippet-list")
