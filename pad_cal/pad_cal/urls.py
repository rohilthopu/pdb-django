"""pad_cal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from dungeon import views as dv
from monsterdatabase import views as mv

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', dv.homeView),
    path('add/', dv.addDungeonView),
    path('all/dungeons', dv.allDungeons),
    path('all/encounters', dv.allEncounters),
    path('all/skills', dv.allSkills),
    path('dungeon/<int:d_id>/', dv.dungeonView),
    path('encounter/<str:m_name>/', dv.monsterView),
    path('monsterdb/na/', mv.cardListNA),
    path('monster/na/<int:card_id>/', mv.cardViewNA),
]
