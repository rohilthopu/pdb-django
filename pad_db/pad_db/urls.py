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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from monsterdatabase import views as mv
from monsterdatabasejp import views as jmv
from guerrilladungeon import views as gv
from dungeon import views as dv
from karmaleaderboard import views as kv

# API imports
from guerrilladungeon import apiviews as gav
from monsterdatabase import apiviews as mav
from karmaleaderboard import apiviews as kav
from monsterdatabasejp import apiviews as mjav
from dataversions import apiviews as dvav
from dungeon import apiviews as dav
urlpatterns = [
                  url(r'^admin/', admin.site.urls),

                  # Guerrilla Dungeons
                  path('', gv.DungeonView),

                  # NA Items
                  path('monsterdb/na/', mv.cardList),
                  path('monster/na/<int:card_id>/', mv.cardView),
                  path('monster/na/edit/<int:card_id>/', mv.editCardView),
                  path('dungeons/na/', dv.dungeonListView),
                  path('dungeons/na/<int:d_id>/', dv.dungeonView),
                  path('activeskills/na/', mv.activeSkillListView),
                  path('activeskills/na/<int:skill_id>/', mv.activeSkillView),
                  path('leaderskills/na', mv.leaderSkillListView),
                  path('leaderskills/na/<int:skill_id>/', mv.leaderSkillView),
                  path('leaderskills/na/edit/<int:skill_id>/', mv.editLeaderSkill),
                  path('activeskills/na/edit/<int:skill_id>/', mv.editActiveSkill),

                  # JP Items
                  path('monsterdb/jp/', jmv.cardList),
                  path('monster/jp/<int:card_id>/', jmv.cardView),
                  path('activeskills/jp/', jmv.activeSkillListView),
                  path('activeskills/jp/<int:id>/', jmv.activeSkillView),
                  path('leaderskills/jp', jmv.leaderSkillListView),
                  path('leaderskills/jp/<int:id>/', jmv.leaderSkillView),

                  path('leaderboard', kv.leaderboardView),

                  # API views
                  path('api/guerrilla/', gav.GuerrillaList.as_view()),
                  path('api/monsters/na/', mav.MonsterList.as_view()),
                  path('api/monsters/jp/', mjav.MonsterList.as_view()),
                  path('api/skills/na/', mav.SkillList.as_view()),
                  path('api/skills/jp/', mjav.SkillList.as_view()),
                  path('api/leaderboard/', kav.LeaderboardList.as_view()),
                  path('api/version/', dvav.VersionList.as_view()),
                  path('api/dungeons/', dav.DungeonList.as_view()),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
