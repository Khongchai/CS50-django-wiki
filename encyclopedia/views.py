from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect


class AddNewEntryForm(forms.Form):
    formTitle = forms.CharField(label="", max_length=20, min_length=1, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'class': 'mediumMargin'}))
    formDescription = forms.CharField(label="", 
    widget=forms.Textarea(attrs={'placeholder': 'Enter description', 'class': 'mediumMargin textAreaSize'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request):
    if request.method == "GET":
        query = request.GET.get('q')
        return HttpResponseRedirect(reverse("encyclopedia:reqTitle", args=[query]))
      

def reqTitle(request, requestedTitle):
    tobeDisplayed = util.get_entry(requestedTitle)
    if tobeDisplayed is None:
        tobeDisplayed = "Error: the requested page could not be found"
    return render(request, "encyclopedia/entry.html", {
        "entry": tobeDisplayed
    })

def createPage(request):
    if request.method == "POST":
        submittedForm = AddNewEntryForm(request.POST)
        if submittedForm.is_valid():
            formTitle = submittedForm.cleaned_data["formTitle"]
            formDescription = submittedForm.cleaned_data["formDescription"]
            formExists = util.get_entry(formTitle)

            if formExists is None:
                util.save_entry(formTitle, formDescription)
                return HttpResponseRedirect(reverse("encyclopedia:reqTitle", args=[formTitle])) 

            return render(request, "encyclopedia/createPage.html", {
                "form": submittedForm,
                "alertMessage": "An article with such title already existed."
            })
        else:
            return render(request, "encyclopedia/createPage.html", {
                "form": submittedForm
            })
    return render(request, "encyclopedia/createPage.html", {
        "form": AddNewEntryForm()
    })

def editPage(request):
    if request.method == "POST":
        markup = request.POST.get('entryField')
        print(markup)
    return render(request, "encyclopedia/editPage.html")












