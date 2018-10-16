from django.shortcuts import render, redirect
from .models import Issue
from .forms import IssueForm


# Create your views here.
def IssueTrackerView(request):
    template = 'datasources.html'

    source = Issue.objects.all()

    form = IssueForm()

    context = {'source': source, 'form': form}
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            # verify that it doesnt already exist
            data = form.cleaned_data
            exists = False
            for item in source:
                if item.itemName.lower() == data.get('itemName').lower() and item.itemID == int(data.get('itemID')):
                    exists = True
            if not exists:
                newIssue = Issue()
                newIssue.server = data.get('server')
                newIssue.itemType = data.get('itemType')
                newIssue.itemName = data.get('itemName')
                newIssue.itemID = int(data.get('itemID'))
                newIssue.description = data.get('description')
                newIssue.save()
                return redirect('/issues/')
            else:
                return redirect('/issues/')

    return render(request, template, context)
