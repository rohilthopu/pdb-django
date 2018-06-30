from django.shortcuts import render, redirect
from .models import Dungeon
from .forms import DungeonLink
# Create your views here.

def homeView(request):
    template = 'home.html'

    source = Dungeon.objects.all()
    form = DungeonLink()

    context = {'dungeons' : source, 'form' : form}

    if request.method == 'POST':
        form = DungeonLink(request.POST)
        if (form.is_valid()):
            # verify that it doesnt already exist
            data = form.cleaned_data
            exists = False
            for item in source:
                if item.dungeonLink.lower() == data.get('dungeonLink').lower():
                    exists = True
            if (not exists):
                dungeon = Dungeon(dungeonLink=data.get('dungeonLink'))
                dungeon.save()
                return redirect('/home/')
            else:
                return redirect('/home/')
    return render(request, template, context)