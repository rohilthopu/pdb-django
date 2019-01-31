import json

import requests

link = "https://00e9e64bacd4831327f8f0f8c1a92750980f631d58c7442953-apidata.googleusercontent.com/download/storage/v1/b/mirubot-data/o/paddata%2Fpadguide%2FdungeonMonsterList.json?qk=AD5uMEvgh1bOinBeC3VuCBH-_xn4s4Ph-NAMdECFADwHYbIROcfEptxQb5csx2kPAh_kPBcBt7O0f17VPOZ91_2pYg5zupJ1hf4yhi0b-XtKp8YkVKZWns6duGpvrprFIWhrRgb_tqGw6JSHPufTustj0e3JxEYGbS8I0zG67IrIsgw5FPoEEFKrp5cb6yn9hl7Xc6uw-ZE8PQfrbtiO9i4BR2skLqUeEtuEeiUVGf3tcYYWP7DFkdEmyjqz4sMC01mQgzBczhvHJ4E3uw52wQIIQeEWwxD3Q37HCxGjCOEQhJUfX_Sh2vJ3zwUnL-jjwmrK8pGi7qZk8ebSIjh-WbEmhCYajQE_tlQsWljt1am8eMzWQ9tNns0_KfZxhcKgl37TTqf5stfnKuWkexXujnQja9btuek4YWUleAXyvktlCjMKdCuHZR6UC2F1ORSVHeoXaduhjEnUDr7Zc8Mnhpf6zBHT2Pr3g9bus-ZKoEq-M_d8IVZ3hbCYWstD0nWew1wIJIOFcZVx5zzwTWvdiXfslEMkFB06IfCmbniU5XYFz45sK0SPv_tF-qXp9rJwPX6-LC8Peq8LxlZILBzY68OnoYyuc_7DZ7jETjISkt5n5WDtvBOLzCsItuULviQmH3My2ZNgXBLT-HiOugn02ZWerO0SSOJahtEvUP05p36qUY3SeTssL7h0gewumqVT09MYcsUIWfkk_4GyUAF7qZxazWbexXHBS3Qv50bas-5fbk6NPOeXxb-ZBRnXEwFF9nwjcryGcfyhbN5esdHywAoVLIDMt-1dv09EmZ09FRDJhLxbfY2A5l0"

jsonData = json.loads(requests.get(link).text)

for item in jsonData['items']:
    monster = {}

    monster['hp'] = item['HP']
    monster['atk'] = item['ATK']
    monster['def'] = item['DEF']

    turn = item['TURN']
    dungeon = item['DUNGEON_SEQ']

    m = item['MONSTER_NO']

    print(monster, turn, dungeon, m)
