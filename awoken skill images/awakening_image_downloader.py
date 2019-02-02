import urllib.request

awakening_base_link = "http://www.puzzledragonx.com/en/img/awoken/"
awakening_link_end = ".png"

for i in range(1, 67):
    link = awakening_base_link + str(i) + awakening_link_end

    filename = link.split('/')[-1]

    urllib.request.urlretrieve(link, filename)
