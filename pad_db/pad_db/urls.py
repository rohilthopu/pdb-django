from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from monsterdatabase import views as mv
from guerrilladungeon import views as gv
from dungeon import views as dv
from karmaleaderboard import views as kv

# # API imports
# from guerrilladungeon import apiviews as gav
# from monsterdatabase import apiviews as mav
# from karmaleaderboard import apiviews as kav
# from dataversions import apiviews as dvav
# from dungeon import apiviews as dav
#
# from guerrilla import views as guerrilla_views
# from monsters import views as monster_views
# from dungeons import views as dungeon_views
# from skills import views as skill_views


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

    path('leaderboard', kv.leaderboardView),

    # # API views
    # path('api/guerrilla/', gav.GuerrillaList.as_view()),
    # path('api/monsters/na/', mav.MonsterList.as_view()),
    # path('api/skills/na/', mav.SkillList.as_view()),
    # path('api/leaderboard/', kav.LeaderboardList.as_view()),
    # path('api/version/', dvav.VersionList.as_view()),
    # path('api/dungeons/', dav.DungeonList.as_view()),
    # path('api/floors/', dav.FloorList.as_view()),
    # path('api/enemyskills/', mav.EnemySkillList.as_view()),
    # path('api/encounters/', dav.EncounterList.as_view()),
    #
    # # new api endpoints
    # path('api/live/guerrilla/', guerrilla_views.guerrilla_view),
    # path('api/live/monsters/', monster_views.monsters_view),
    # path('api/live/dungeons/', dungeon_views.dungeons_view),
    # path('api/live/skills/', skill_views.skills_view),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
