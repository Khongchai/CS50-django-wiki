from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
import re


class AddNewEntryForm(forms.Form):
    formTitle = forms.CharField(label="", max_length=20, min_length=1, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'class': 'mediumMargin'}))
    formDescription = forms.CharField(label="", 
    widget=forms.Textarea(attrs={'placeholder': 'Enter description', 'class': 'mediumMargin textAreaSize'}))

class TextAreaOnly(forms.Form):
    description = forms.CharField(label="", 
    widget=forms.Textarea(attrs={'class': 'mediumMargin textAreaSize', 'id': 'content'}))


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
        #try changing here to clean data
        #then if that's ok, and you know that no whitte spaces are added, then you're good to just style everything nicely
        formContentNew = request.POST.get('entryField')
        tmp = re.findall(r"[\w]+", formContentNew)
        #title name will be the first that gets detected
        formTitle = tmp[0]
        util.save_entry(formTitle, formContentNew)

        return HttpResponseRedirect(reverse("encyclopedia:reqTitle", args=[formTitle])) 

    """
    #change submit = get, editing = post
        if request.method == "GET":
            submittedChange = AddNewEntryForm(request.GET)
            if (submittedChange.is_valid()):
                formTitles = submittedChange.cleaned_data["formTitle"]
                formDescription = submittedChange.cleaned_data["formDescription"]

                titles = re.findall(r"[\w]+", formTitles)
                title = titles[0]

                

                return (HttpResponseRedirect(reverse("encyclopedia:reqTitle", args=[title])))

            else:
                return HttpResponseRedirect("Error")
        else:
            markup = re.split(r"[\r\n]+", (request.POST.get('entryField')))
            
            #right now it does not work with HTML page, find a way to do that
            markupHeaders = [char for char in markup if "#" in char]
            markupDescriptions = [char for char in markup if "#" not in char]

            #first member of markupHeaders is the name of the fil

            #in case there are more than 1 headings
            forms = []
            for i in range(len(markupHeaders)):
                forms.append(AddNewEntryForm(initial={'formTitle': markupHeaders[i], 'formDescription': markupDescriptions[i]}))
                
            
            return render(request, "encyclopedia/editPage.html", {
                "forms": forms
            })
            
    
"""











