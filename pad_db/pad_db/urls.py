from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

# # API imports
from guerrilla import apiviews as gav
from monsters import apiviews as mav
from skills import apiviews as sav
from dungeons import apiviews as dav

from data_manager import views as search_api

urlpatterns = [


    # REST API Endpoints
    path('rest/monster/<int:card_id>/', mav.MonsterObject.as_view()),
    path('rest/monsters/', mav.MonsterList.as_view()),
    path('rest/skills/', sav.SkillList.as_view()),
    path('rest/skill/<int:skill_id>/', sav.SkillObject.as_view()),
    path('rest/guerrilla/', gav.GuerrillaList.as_view()),
    path('rest/dungeons/', dav.DungeonList.as_view()),
    path('rest/dungeon/<int:dungeon_id>/', dav.DungeonObject.as_view()),
    path('rest/floors/', dav.AllFloorsList.as_view()),
    path('rest/floors/<int:dungeon_id>/', dav.FloorList.as_view()),
    path('rest/floor/<int:dungeon_id>/<int:floor_number>/',
         dav.FloorObject.as_view()),

    # ES based endpoints
    path('search/<str:index>/<str:query>/', search_api.search),
    path('monsters/<int:card_id>/', search_api.get_monster_by_id),
    path('skills/<int:skill_id>/', search_api.get_skill_by_id),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
