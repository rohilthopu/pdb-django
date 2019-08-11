from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

# # API imports
from guerrilla import apiviews as gav
from monsters import apiviews as mav
from skills import apiviews as sav
from dungeons import apiviews as dav
from data_manager import views as sv

urlpatterns = [
    # new api endpoints
    path('monster/<int:card_id>/', mav.MonsterObject.as_view()),
    path('monsters/', mav.MonsterList.as_view()),
    path('skills/', sav.SkillList.as_view()),
    path('skill/<int:skill_id>/', sav.SkillObject.as_view()),
    path('guerrilla/', gav.GuerrillaList.as_view()),
    path('dungeons/', dav.DungeonList.as_view()),
    path('dungeon/<int:dungeon_id>/', dav.DungeonObject.as_view()),
    path('floors/', dav.AllFloorsList.as_view()),
    path('floors/<int:dungeon_id>/', dav.FloorList.as_view()),
    path('floor/<int:dungeon_id>/<int:floor_number>/', dav.FloorObject.as_view()),
    path('search/<str:query>/', sv.search),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
