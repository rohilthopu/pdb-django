import requests
import json
import csv
from io import StringIO
from typing import List, Any


link = "https://00e9e64bac344d9e4019c1d18f7ab571a8206863643bb8a8d5-apidata.googleusercontent.com/download/storage/v1/b/mirubot-data/o/paddata%2Fraw%2Fna%2Fdownload_dungeon_data.json?qk=AD5uMEsv8EseR0qELxuse9fuUjsPiUOkes-oKGmTU6EG-glF35X6V9ax9sOAFpAxUPpo-FlquG17q_nFvCMsBme3mYLROWjKiG6V4vodLo8Ge5vmRYoCL-_0dgxrvREDKss4C9pt0Hh2f08MgnofgGksd1LvLjE1E7xYz4PpYd2y8GWBjrMNvIJvpOlzad3UeTUmdcJp79PVDHL55Iu6jZIojIGmlO7IQRHqRHbAo4AYpE2VNFEMz80d0xJm5NQ7tdXCG52K916Ftf416kok9zM-Qyl7j3hpLQxPB43DICHJZMV7UBRT5ITqincoiQ7L3WXqmanRtsufOs-dmQqrxg0qDBt6jt_qviOVsyHUqunTftBgvwOfeh-1V_M55mVhMz_claUHa_vtOdQnoF6ubXWGgJODx33dj88fD7k0sWP2x2rBzankGxBSPYuoXNuZ51rcuqALrqG9ka4fcaJ6q2S75R5RrQ9mgMObHFNNFHRoFqUnGVJR_Iua9ty6jAboiTK8turPpqY9lFqt2gDj6E_Qc_GLYSz9ETr4IrXjqZ_zRtqQsxPmOZvT1XZu2CrqEZfHPvKEIEey6kHBMYyM51wHTc3MuOZHIDObygts1jSx47voN0c89YNxV8ShaxtrVeqOOQqs8lVhi1dzmp4CoYj4arbcJ2HsU_XxKMOBmMZklW2KpW_tYC6peD2tnSBgF8E3-MHniAGyI3xHrDrWyZdmdwhTkstzLsfKCoUZdlEl-ElpCUTCxQMTxJV6taqrCy05kGfS9t4intf0z39C0UXUDodUr4PlKFHK4z_b_B1GTmr_eQEzViqPa8WKDKi6BH3Z0NO8vYpH"
# sd = "https://00e9e64bacad1046a9a397ab3824fe20b80569c246caaa88e8-apidata.googleusercontent.com/download/storage/v1/b/mirubot-data/o/paddata%2Fpadguide%2FsubDungeonList.json?qk=AD5uMEsPgcxzM8u9JA_9KH834aHI10wfbGArTs621xkfCxHLKLEuXLh1CBTQynQsYcYM8vqmFyF6rpYYRZfTcCeCUEZDnUDiPjI3zIgQ3H9EjGrRtYddZUkrjH8xTIitatVg5Wtp9uTXgJmpnNmb66PVPEPcPPKjgkK6nCL626RmA7QHdJD_Evw8fQplNl7PriulWwrrq2hFz23JecNYKQoVStWOcaqk8IsZK99s8aZa4bpXBo-xLg2vuJ4zMVVnpqT5DJ5egKy6G9K-LDCfiVvpS86mXXd4VcEn1B2rmi81afU1rCG_qGD8S6OSzMv3jLTBg3s8f04lkgTfXfke3KGuNrKWXm5yyT2tfBqc8YIea0mn9xhKY4Phh7nJBsn2TVz5el_0-nRDp-jBbCGv0lGmyJ4OECgLGImzc2Tp5NKNLxHkpY4K05sSVB3elvTGwGL0dqwt6bcGT3ZgyW-WIc-extDFWggJjcsfEDULtFDffvax1nep5onamKlW1VHrGSLzjkbwd-bkKGcQ4ka1MkoWytJl9d74vN5QUPqmWKiNiqYAW7NabaNfOQJdloA3koHGKY-m4Ty6KIzvQv7q1FwChb9aLcSMGYukjq6tqmPNeNb6cmTs6jDlrXh5JgO8LgUdr5JWewpTUcGrmrnsuIqZACTIYzmrNnsJ0VUga-R-ZEGzPtpUPqWsAaAcl9AZA27YRQADDCjgjGAbj4JKuNtK5iD2OZRk-hhrOLOeMhE9LbF1W_Z0BufSB4TpvWK15imEodXMAyOrAxr1Rr9WVM5nuGU7K8qTBNa95iZ7BW9LtlXcjd9scnw"
# sd_list = json.loads(requests.get(sd).text)['items']
#
# stuff = {}
#
# for item in sd_list:
#     name = item['TSD_NAME_US']
#     tsd_seq = item['TSD_SEQ']
#
#     stuff[name] = int(tsd_seq)
#
#
# for key, val in sorted(stuff.items()):
#     print(key, val)

dungeons = json.loads(requests.get(link).text)

if dungeons['v'] > 6:
    print('Warning! Version of dungeon file is not tested: {}'.format(dungeons['v']))

dungeon_info = dungeons['dungeons']

dungeons = []
cur_dungeon = None

for line in dungeon_info.split('\n'):
    info = line[0:2]
    data = line[2:]
    data_values = next(csv.reader(StringIO(data), quotechar="'"))
    if info == 'd;':
        print(data_values)
    elif info == 'f;':
        print('\t\t', data_values)
    elif info == 'c;':
        pass
    else:
        raise ValueError('unexpected line: ' + line)

