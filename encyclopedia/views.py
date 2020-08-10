from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
import re
import random
from markdown2 import Markdown


class AddNewEntryForm(forms.Form):
    formTitle = forms.CharField(label="", max_length=20, min_length=1, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'class': 'mediumMargin'}))
    formDescription = forms.CharField(label="", 
    widget=forms.Textarea(attrs={'placeholder': 'Enter description', 'class': 'mediumMargin textAreaSize'}))

class TextAreaOnly(forms.Form):
    description = forms.CharField(label="", 
    widget=forms.Textarea(attrs={'class': 'textAreaDisplay', 'id': 'content'}))


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
    markdownRead = Markdown()
    tobeDisplayed = markdownRead.convert(tobeDisplayed)
    return render(request, "encyclopedia/entry.html", {
        "entry": TextAreaOnly(initial={"description": tobeDisplayed})
        #"entry": tobeDisplayed
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
        formContentAll = TextAreaOnly(request.POST)
        if formContentAll.is_valid():
            formContentNew = formContentAll.cleaned_data["description"]

            #get all words and form title and first member is always title
            tmp = re.findall(r"[\w]+", formContentNew)
            formTitle = tmp[0]

            util.save_entry(formTitle, formContentNew)
            return HttpResponseRedirect(reverse("encyclopedia:reqTitle", args=[formTitle])) 

    return HttpResponse("Page load failure: code 13902")

def randomize(request):
    allEntries = util.list_entries()
    entriesAmount = len(allEntries)
    
    randomNum = random.randint(0, entriesAmount - 1)
    print(randomNum)

    #add link to random page
    return HttpResponseRedirect(reverse("encyclopedia:reqTitle", args=[allEntries[randomNum]]))











