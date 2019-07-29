from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from monsters import views as mv
from guerrilla import views as gv
from dungeons import views as dv

# # API imports
from guerrilla import apiviews as gav
from monsters import apiviews as mav
from skills import apiviews as sav
from dungeons import apiviews as dav

urlpatterns = [
    # Guerrilla Dungeons
    path('', gv.guerrilla_view),
    path('monsters/', mv.monster_list),
    path('monster/<int:card_id>/', mv.monster_view),

    # # Site Locations
    # path('monsterdb/na/', mv.monster_list),
    # path('monster/na/<int:card_id>/', mv.monster_view),
    # path('dungeons/na/', dv.dungeonListView),
    # path('dungeons/na/<int:d_id>/', dv.dungeonView),
    # path('leaderboard', kv.leaderboardView),

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

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
