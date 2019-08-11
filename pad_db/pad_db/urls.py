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
    path('api/monster/<int:card_id>/', mav.MonsterObject.as_view()),
    path('api/monsters/', mav.MonsterList.as_view()),
    path('api/skills/', sav.SkillList.as_view()),
    path('api/skill/<int:skill_id>/', sav.SkillObject.as_view()),
    path('api/guerrilla/', gav.GuerrillaList.as_view()),
    path('api/dungeons/', dav.DungeonList.as_view()),
    path('api/dungeon/<int:dungeon_id>/', dav.DungeonObject.as_view()),
    path('api/floors/', dav.AllFloorsList.as_view()),
    path('api/floors/<int:dungeon_id>/', dav.FloorList.as_view()),
    path('api/floor/<int:dungeon_id>/<int:floor_number>/', dav.FloorObject.as_view()),
    path('search/<str:query>/', sv.search),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
