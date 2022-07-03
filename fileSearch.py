import configparser
import sys

def searchById(id, fman=''):
    if fman=='':
        lm = ''
    else:
        if sys.platform == "linux" or sys.platform == "linux2":
            lm=("/home/michael/server-side/storage/")
        elif sys.platform == "win32":
            lm=("C:/Users/MichaelODeli/OneDrive/DEVELOP/work/home-server/server-side/storage/")
    cfg = configparser.ConfigParser()
    with open(lm+'settings.ini', 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    wayConf = cfg.get('settings', 'way')
    if cfg.has_option('prefixes', id[0]):
        categ = cfg.get('prefixes', id[0])
        wayParam = categ + 'folder'
        wayConf = wayConf + cfg.get('settings', wayParam)
        libName = cfg.get('libs', categ)
        with open(lm+libName, 'r', encoding='utf-8') as fp:
            cfg.read_file(fp)
        if cfg.has_option(categ, id)==True:
            return [
                [categ, id, cfg.get(categ, id).split('/')[0], cfg.get(categ, id).split('/')[1]]
            ]
        else:
            return [['Not found']]


# def confReaderOptions(name, searchType):
#     if searchType == 'keywords':
#         cats = 'keywords'
#     if searchType == 'filename':
#         cats = name.replace('storageLib_', '').replace('.ini', '').lower()
#     cfg = configparser.ConfigParser()
#     with open(name, 'r', encoding='utf-8') as fp:
#         cfg.read_file(fp)
#     return(cfg.items(cats, raw=True))

# def search(filename, searchType):
#     cfg = configparser.ConfigParser()
#     with open('settings.ini', 'r', encoding='utf-8') as fp:
#         cfg.read_file(fp)
#     filename = filename.lower().replace(' ', '-')
#     libNames = cfg.items('libs')
#     founded = []
#     for n in libNames:
#         g = confReaderOptions(n[1], searchType)
#         for f in g:
#             if filename.lower() in f[1].lower():
#                 foundName = f[1]
#                 id = f[0]
#                 founded.append([id, foundName])
#             if filename.lower() in f[0].lower():
#                 foundName = f[1]
#                 id = f[0]
#                 founded.append([id, foundName])
#     fidex = []
#     if founded!=[]:
#         for naming in founded:
#             id = naming[0]
#             try:
#                 categ = cfg.get('prefixes', id[0])
#             except configparser.NoOptionError:
#                 return[['Not found']]
#             channel = naming[1].split('/')[0]
#             filename = naming[1].split('/')[1]
#             fidex.append([categ, id, channel, filename])
#         return(fidex)
#     else: return[['Not found']]

def confReaderOptions(name, searchType):
    if searchType == 'keywords':
        cats = 'keywords'
    if searchType == 'filename' or searchType == 'channel' or searchType == 'all' or searchType == 'type':
        cats = name.replace('storageLib_', '').replace('.ini', '').lower()
    cfg = configparser.ConfigParser()
    with open(name, 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    return(cfg.items(cats, raw=True))

def search(filename, searchType):
    cfg = configparser.ConfigParser()
    with open('settings.ini', 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    # filename = filename.lower().replace(' ', '-')
    filename = filename.lower()
    libNames = cfg.items('libs')
    lister = []
    for k in libNames: lister.append(k[0])
    if filename in lister and searchType == 'type':
        libr = 'storageLib_'+filename.title()+'.ini'
        tying = filename.lower()
        c = confReaderOptions(libr, searchType)
        fidex = []
        for fle in c:
            id = fle[0]
            if id !='-1':
                channel = fle[1].split('/')[0]
                filename = fle[1].split('/')[1]
                fidex.append([tying, id, channel, filename])
        return(fidex)
    elif searchType != 'type':
        founded = []
        for n in libNames:
            g = confReaderOptions(n[1], searchType)
            for f in g:
                if str(f[0])!='-1':
                    channel_ = f[1].split('/')[0]
                    filename_ = f[1].split('/')[1]
                    if searchType == 'filename' or searchType == 'channel':
                        if searchType == 'filename':
                            tofind = filename_
                        if searchType == 'channel':
                            tofind = channel_
                        if filename.lower() in tofind.lower():
                            foundName = f[1]
                            founded.append([f[0], foundName])
                    elif searchType == 'all':
                        if filename.lower() in f[0].lower():
                            foundName = f[1]
                            founded.append([f[0], foundName])
                        if filename.lower() in f[1].lower():
                            foundName = f[1]
                            founded.append([f[0], foundName])
                    else: return[['Incorrect searchType']]
        fidex = []
        if founded!=[]:
            for naming in founded:
                id = naming[0]
                # try:
                categ = cfg.get('prefixes', id[0])
                # except configparser.NoOptionError:
                # return[['Not found']]
                channel = naming[1].split('/')[0]
                filename = naming[1].split('/')[1]
                fidex.append([categ, id, channel, filename])
            return(fidex)
        else: return[['Not found']]
    else: return[['Not found']]

# print(search(filename='youtube', searchType='type'))