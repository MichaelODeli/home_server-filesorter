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
"""
# obsolete
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
"""

def confReaderOptions(name):
    cfg = configparser.ConfigParser()
    if name == 'storageLib_Films.ini':
        cats = 'films'
    if name == 'storageLib_Yt.ini':
        cats = 'youtube'
    if name == 'storageLib_Serials.ini':
        cats = 'serials'
    with open(name, 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    return(cfg.items(cats, raw=True))

def search(filename):
    cfg = configparser.ConfigParser()
    with open('storageLib.ini', 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    filename = filename.lower().replace(' ', '-')
    libNames = [cfg.get('libs', 'youtubelib'), cfg.get('libs', 'serialslib'), cfg.get('libs', 'filmslib')]
    founded = []
    for n in libNames:
        g = confReaderOptions(n)
        for f in g:
            if filename.lower() in f[1].lower():
                foundName = f[1]
                id = f[0]
                founded.append([id, foundName])
            if filename.lower() in f[0].lower():
                foundName = f[1]
                id = f[0]
                founded.append([id, foundName])
    fidex = []
    if founded!=[]:
        for naming in founded:
            id = naming[0]
            if id[0]=='y':
                categ='youtube'
            if id[0]=='f':
                categ='films'
            if id[0]=='s':
                categ='serials'
            channel = naming[1].split('/')[0]
            filename = naming[1].split('/')[1]
            fidex.append([categ, id, channel, filename])
        return(fidex)
    else: return[['Not found']]

# print(searchByFilename(filename='корпорация'))