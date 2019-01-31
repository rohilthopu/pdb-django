import requests
import json

link = "https://00e9e64bacfd3b848735fadd3d1b97e7997d487d61da999818-apidata.googleusercontent.com/download/storage/v1/b/mirubot-data/o/paddata%2Fprocessed%2Fna_enemy_skills.json?qk=AD5uMEsPsyb7C69OCiLsb4RrWLsh9M5J8xLAUUp5MyFuAwodpXfC6jp07ZX10RkBIq_4FW2P_yZkvc-opzSIAhNYlql7GxUXPa4pbE2-oOOztRE8CAEJoUnFygb3LqdC_qSuKQ769XRNNhibcxkUe0bq0sdOUo22XSk9ro1DLBeKvDPTTNIlJvjyqPTenKMRUUCwL6_R23rdlYCUxtCf2QArqvaP7utlFo6tqKBTp9AUbasXGr2UF4fb1L_QyOMcGeXWkSekLpKVJ8uOWTdVxCCzRGKh41pM0kL0Tmogpi1LRpRbyVDuyPy4q3NZtt9d9XMrvbiuHCpG3wrExLkQuCsEdha9OAyMEix0efVjL3IdnHwKkWCdba-9SrKcM2ucAFioZI6ReuO_sqPR_RjXSggGO-nmUEGQdVbdmoo-liT6KQ_1bfj6zyUY7asm5V51ZU4bf863I4QCQ4xjMYfDjCdJTz0VhPAjsPCyBjekWp_hGgPUlaO3x-Ra2y5-yOqKTgPzJMlcNVn1lTJH_ENXlQR3HArfju7fxMfoSWozyWMaerVjc8xMTLcikNWguEYtgJ3SiyLDy9pM5zDw0PoVh5nLIX_2r8k9IXUDSZI_HE7HCtS9AMRMB9KQ6zH0Ok63iLfsZ6kANOW0ydpHZaL-3m-A8gkPDBVBDnkSPRGp_PjlLnS6Ibd-u1lLcxlhQjtAiDFDi8Dd5l5SsXq885Vg2aWIp8L9p5CD2H-bx2Jj79nVxV1pgy4JX7SfDcJGyfdxbt6Bb-xA8GYF9Yy6RCNHQfn9ZOzoeLOsjaL9xpoRkNtC998DZo85Oq0"
data = json.loads(requests.get(link).text)


class EnemySkill:
    def __init__(self):
        self.skill_id = None
        self.name = None


for item in data:
    # print(item['enemy_skill_id'])

    name = item['name']
    clean_name = name.replace('\n', ' ') if name is not None else name

    effect = str(item['params'][0])

    clean_effect = effect.replace('\n', ' ') if effect is not None else effect

    print('\t\t', clean_name)
    # print('\t\t', clean_effect)
