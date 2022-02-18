import configparser

import fileManager as fman

def searchById(id):
    if fman.isVideoIDExist(id)==True:
        cfg = configparser.ConfigParser()
        with open('storageLib.ini', 'r', encoding='utf-8') as fp:
            cfg.read_file(fp)
        wayConf = cfg.get('settings', 'way')
        if id[0]=='y' or id[0]=='f' or id[0]=='s':
            if id[0]=='y':
                libName = cfg.get('libs', 'youtubelib')
                wayConf=wayConf+'youtube/'
                categ='youtube'
            if id[0]=='f':
                libName = cfg.get('libs', 'filmslib')
                wayConf=wayConf+'films/'
                categ='films'
            if id[0]=='s':
                libName = cfg.get('libs', 'serialslib')
                wayConf=wayConf+'serials/'
                categ='serials'
            with open(libName, 'r', encoding='utf-8') as fp:
                cfg.read_file(fp)
            fullway = wayConf + cfg.get(categ, id)
            # return [fullway, cfg.get(categ, id).split('/')[0], cfg.get(categ, id).split('/')[1]]
            # return [categ, id, cfg.get(categ, id).split('/')[0], cfg.get(categ, id).split('/')[1]]
            return [
                [categ, id, cfg.get(categ, id).split('/')[0], cfg.get(categ, id).split('/')[1]]
            ]
    else:
        return [['Not found']]
def searchByFilename(filename):
    return None

def confReader(name):
    cfg = configparser.ConfigParser()
    with open(name, 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
        return(cfg.sections())

def getContent(foundCategory, foundChannel):
    if foundCategory == 'youtube':
        name = 'storageLib_Yt.ini'
    if foundCategory == 'serials':
        name = 'storageLib_Films.ini'
    if foundCategory == 'films':
        name = 'storageLib_Serials.ini'
    cfg = configparser.ConfigParser()
    with open(name, 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    lister = []
    for element in cfg.options(foundCategory):
        if element!=str(-1):
            if cfg.has_option(foundChannel, element)==True:
                lister.append([foundCategory, element, cfg.get(foundCategory, element).split('/')[0], cfg.get(foundCategory, element).split('/')[1]])
    return lister

def searchByChannel(channel):
    cfg = configparser.ConfigParser()
    with open('storageLib.ini', 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    channelname = channel.lower().replace(' ', '-')
    channelsplit = channel.lower().split(' ')
    libNames = [cfg.get('libs', 'youtubelib'), cfg.get('libs', 'serialslib'), cfg.get('libs', 'filmslib')]
    apd = []
    k = 1
    for n in libNames:
        g = confReader(n)
        del g[0]
        apd.append(g)
    for element in apd:
        category = element[0]
        for ele in element:
            eleo=ele.lower()
            k = channelname
            if eleo.find(k)!=(-1):
                foundChannel = ele
                foundCategory = category
            else: pass
    try:
        found=[foundCategory, foundChannel]
        return getContent(found[0], found[1])
    except UnboundLocalError:
        return [['Not found']]

# print(searchByChannel(channel='сосед'))