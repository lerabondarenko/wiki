from django.shortcuts import render, redirect
import markdown2
from . import util
from django import forms
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    # returns rendered .md
    md = util.get_entry(title)
    error = True
    html = None

    if md is not None:
        html = markdown2.markdown(md)
        error = False

    return render(request, "encyclopedia/title.html", {
        "title": md,
        "html": html,
        "error": error,
        "entry": title
    })


class EntryForm(forms.Form):

    title = forms.CharField(label="Title:", required=False, widget=forms.TextInput(
        attrs={
            'name': 'title',
            'placeholder': 'Name for the new entry...',
            'required': 'True',
            'class': 'form-control w-50'
        }))

    content = forms.CharField(label="Description:", required=False, widget=forms.Textarea(
        attrs={
            'name': 'content',
            'rows': 6,
            'cols': 50,
            'heith': '60vh',
            'placeholder': 'Description for the new entry...',
            'required': 'True',
            'class': 'form-control w-50',
        }))


def create(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        md = util.get_entry(title)
        if md is not None:
            return render(request, "encyclopedia/error.html")
        else:
            util.save_entry(title, content)
            html = markdown2.markdown(content)
            error = False

            return render(request, "encyclopedia/title.html", {
                "title": content,
                "html": html,
                "error": error,
                "entry": title
            })
    if request.method == "GET":
        form = EntryForm(request.POST)
        return render(request, "encyclopedia/create.html", {
            "form": form
        })


def edit(request, entry):
    if request.method == "GET":
        md = util.get_entry(entry)
        form = EntryForm(initial={'title': entry, 'content': md})

        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "entry": entry
        })

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html = markdown2.markdown(content)

        return render(request, "encyclopedia/title.html", {
            "title": content,
            "html": html,
            "entry": title
        })


def search(request):
    title = request.GET.get('q')
    md = util.get_entry(title)
            
    if md is not None:
        html = markdown2.markdown(md)
        error = False
        return render(request, "encyclopedia/title.html", {
            "title": md,
            "html": html,
            "error": error,
            "entry": title
        })
        
    else:
        entries = util.list_entries()
        results = [entry for entry in entries if title.lower() in entry.lower()]
        return render(request, "encyclopedia/search-results.html", {"results": results})

   
def random_page(request):
    entry = util.list_entries()
    page = random.choice(entry)

    return redirect('title', title=page)
