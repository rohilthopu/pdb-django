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
from monsterdatabase import views as mv
from monsterdatabasejp import views as jpv
from guerrilladungeon import views as gv

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', gv.DungeonView),
    path('monsterdb/na/', mv.cardListNA),
    path('monster/na/<int:card_id>/', mv.cardViewNA),
    path('monsterdb/jp/', jpv.cardListJP),
    path('monster/jp/<int:card_id>/', jpv.cardViewJP)
]
