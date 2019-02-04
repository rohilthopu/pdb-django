import requests
import json

sd = "https://00e9e64bacad1046a9a397ab3824fe20b80569c246caaa88e8-apidata.googleusercontent.com/download/storage/v1/b/mirubot-data/o/paddata%2Fpadguide%2FsubDungeonList.json?qk=AD5uMEsPgcxzM8u9JA_9KH834aHI10wfbGArTs621xkfCxHLKLEuXLh1CBTQynQsYcYM8vqmFyF6rpYYRZfTcCeCUEZDnUDiPjI3zIgQ3H9EjGrRtYddZUkrjH8xTIitatVg5Wtp9uTXgJmpnNmb66PVPEPcPPKjgkK6nCL626RmA7QHdJD_Evw8fQplNl7PriulWwrrq2hFz23JecNYKQoVStWOcaqk8IsZK99s8aZa4bpXBo-xLg2vuJ4zMVVnpqT5DJ5egKy6G9K-LDCfiVvpS86mXXd4VcEn1B2rmi81afU1rCG_qGD8S6OSzMv3jLTBg3s8f04lkgTfXfke3KGuNrKWXm5yyT2tfBqc8YIea0mn9xhKY4Phh7nJBsn2TVz5el_0-nRDp-jBbCGv0lGmyJ4OECgLGImzc2Tp5NKNLxHkpY4K05sSVB3elvTGwGL0dqwt6bcGT3ZgyW-WIc-extDFWggJjcsfEDULtFDffvax1nep5onamKlW1VHrGSLzjkbwd-bkKGcQ4ka1MkoWytJl9d74vN5QUPqmWKiNiqYAW7NabaNfOQJdloA3koHGKY-m4Ty6KIzvQv7q1FwChb9aLcSMGYukjq6tqmPNeNb6cmTs6jDlrXh5JgO8LgUdr5JWewpTUcGrmrnsuIqZACTIYzmrNnsJ0VUga-R-ZEGzPtpUPqWsAaAcl9AZA27YRQADDCjgjGAbj4JKuNtK5iD2OZRk-hhrOLOeMhE9LbF1W_Z0BufSB4TpvWK15imEodXMAyOrAxr1Rr9WVM5nuGU7K8qTBNa95iZ7BW9LtlXcjd9scnw"
sd_list = json.loads(requests.get(sd).text)['items']

stuff = {}

for item in sd_list:
    name = item['TSD_NAME_US']
    tsd_seq = item['TSD_SEQ']

    stuff[name] = int(tsd_seq)


for key, val in sorted(stuff.items()):
    print(key, val)
