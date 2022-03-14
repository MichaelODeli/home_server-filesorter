import configparser

def searchById(id):
    cfg = configparser.ConfigParser()
    with open('settings.ini', 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    wayConf = cfg.get('settings', 'way')
    if cfg.has_option('prefixes', id[0]):
        categ = cfg.get('prefixes', id[0])
        wayParam = categ + 'folder'
        wayConf = wayConf + cfg.get('settings', wayParam)
        libName = cfg.get('libs', categ)
        with open(libName, 'r', encoding='utf-8') as fp:
            cfg.read_file(fp)
        if cfg.has_option(categ, id)==True:
            return [
                [categ, id, cfg.get(categ, id).split('/')[0], cfg.get(categ, id).split('/')[1]]
            ]
        else:
            return [['Not found']]


# def confReaderOptions(name, type):
#     if type == 'keywords':
#         cats = 'keywords'
#     if type == 'filename':
#         cats = name.replace('storageLib_', '').replace('.ini', '').lower()
#     cfg = configparser.ConfigParser()
#     with open(name, 'r', encoding='utf-8') as fp:
#         cfg.read_file(fp)
#     return(cfg.items(cats, raw=True))

# def search(filename, type):
#     cfg = configparser.ConfigParser()
#     with open('settings.ini', 'r', encoding='utf-8') as fp:
#         cfg.read_file(fp)
#     filename = filename.lower().replace(' ', '-')
#     libNames = cfg.items('libs')
#     founded = []
#     for n in libNames:
#         g = confReaderOptions(n[1], type)
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

def confReaderOptions(name, type):
    if type == 'keywords':
        cats = 'keywords'
    if type == 'filename' or type == 'channel' or type == 'all':
        cats = name.replace('storageLib_', '').replace('.ini', '').lower()
    cfg = configparser.ConfigParser()
    with open(name, 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    return(cfg.items(cats, raw=True))

def search(filename, type):
    cfg = configparser.ConfigParser()
    with open('settings.ini', 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    filename = filename.lower().replace(' ', '-')
    libNames = cfg.items('libs')
    founded = []
    for n in libNames:
        g = confReaderOptions(n[1], type)
        for f in g:
            if str(f[0])!='-1':
                channel_ = f[1].split('/')[0]
                filename_ = f[1].split('/')[1]
                if type == 'filename' or type == 'channel' or type == 'keywords':
                    if type == 'filename':
                        tofind = filename_
                    elif type == 'channel':
                        tofind = channel_
                    elif type == 'keywords':
                        tofind = f[1]
                    else: return[['Incorrect type']]
                    if filename.lower() in tofind.lower():
                        foundName = f[1]
                        id = f[0]
                        founded.append([id, foundName])
                elif type == 'all':
                    if filename.lower() in f[0].lower():
                        foundName = f[1]
                        id = f[0]
                        founded.append([id, foundName])
                    if filename.lower() in f[1].lower():
                        foundName = f[1]
                        id = f[0]
                        founded.append([id, foundName])
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

# print(search(filename='python', type='keywords'))