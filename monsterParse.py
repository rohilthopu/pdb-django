import requests
import json


def parseCard():
    monsterLink = "https://00e9e64bacad6e6aea10255aec8340ded003b3e8d7bea41ea7-" \
                  "apidata.googleusercontent.com/download/storage/v1/b/mirubot/o/paddata%2Fprocessed%2Fna_cards." \
                  "json?qk=AD5uMEuY7949YfxdR-fvlOyf8na5v88dRMqLdKj7HD9afnwf8y1MiFmoNf8AWoe44bAZSTzlJYj8R7tly37PCvABp5PGKaSsA" \
                  "nK-dfm8k_2-jxbq6GoOsrz3S9CJRanDvyeGnvZsoOsHMS7-0n0HYX8D2ZBD22VBols-XBilAvFEBHaUQ315FssibEELiwUBRSUjhDxp" \
                  "CukBNTTtuSE-aZbfc4P3JBI1E3mnR5Op1m19syhFeJyVvrNFccMfK3Nn01DOCLVkHHjqZg6yivqSoczGiHUqCfWZdsSlu_AOBdaoL" \
                  "7Td2ubYXaoNTcKXd7Xxy8IPBM0AOeHMMcEDWeW5FKoVKW7nvtFEhZ7JojfFfT3yyuMJezO9i1MQWFCnCdTGbdfKBt6liG_yKVDqKz" \
                  "PA_phT9OPNCQT7US2qu6jBEUQoFFQCcH4G6nTmZDPGQz19pTPW8jZEgYB5oIIv2t_jivQOJLTvKhho2o14Zb6ui-5OGX05ac48Ykk" \
                  "0Y84K1uKw9Ld8q4nVy4oVL75PYiKYzcbAnLm6TNonXLlvqw4Vt4vWe7cP7iUl3HN6HYa930j03-JTQpr3B7ABSS64TN9SF6t_6pseV" \
                  "c4rLMArrvk_woV2JulAnZuRQrdp9YppUq_FuMfvdREpb4sBEsNZyaPwMff2Jqp5UMdrcJcc9uCSR7csOFuEqQP9_EKefj1t5wG6f1E" \
                  "fZ1usAvMd4uHuMlt4946ADzTwqer5YbqkA81oOs_4v1N8OXu_CxSmMMviILSCjL4JbXWHjOGL"

    # what a fuckin URL this is lmao.

    loadSite = requests.get(monsterLink)
    jsonCollect = json.loads(loadSite.text)

    for card in jsonCollect:
        print(card['card']['name'])



parseCard()