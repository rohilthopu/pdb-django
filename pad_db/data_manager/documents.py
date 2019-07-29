from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from monsters.models import Monster
from dungeons.models import Dungeon
from skills.models import Skill

@registry.register_document
class MonsterDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'monsters'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Monster
        fields = [
            'name',
            'card_id',
        ]


@registry.register_document
class DungeonDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'dungeons'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Dungeon
        fields = [
            'name',
            'dungeon_id',
            'dungeon_type',
        ]


@registry.register_document
class SkillDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'skills'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Skill
        fields = [
            'name',
            'description',
            'skill_id',
            'skill_type',
        ]
