# run as module
import configparser
import glob
import os

def optlist(libname, type):
    cfg = configparser.ConfigParser()
    with open(libname, 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    lst = []
    i = cfg.options(type)
    for opt in i:
        g = cfg.get(type, opt)
        p = cfg.get('keywords', opt)
        lstq = [opt, g, p]
        lst.append(lstq)
    return lst

def checkDoubles(oplistin, filenam):
    nl = []
    for element in oplistin:
        nl.append(element[1])
    k = 0
    for element in nl:
        if element == filenam: return True
        else: k+=1
    if k==0: return True
    else: return False

def listRebuild(type):
    cfg = configparser.ConfigParser()
    with open('settings.ini', 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    if cfg.has_option('libs', type):
        libPrefix = type[0]
        folderConf = type + 'folder'
        confDir = type + '/'
        libName = cfg.get('libs', type)
    else:
        return('type '+type+' is not supported')
    wayConf = cfg.get('settings', 'way')
    folderDir = cfg.get('settings', folderConf)
    # way = wayConf + folderDir + '/*/*.mp4'
    way = wayConf + folderDir + '/*/*'+cfg.get('extensions', type)
    ytList = glob.glob(way, recursive=True)
    ytListFull = []
    ytListCleaned = []
    fileWaySplit = []
    fileWaySplitCleaned = []
    for fileWay in ytList:
        fileWay = fileWay.replace('\\', '/')
        ytListFull.append(fileWay)
    filesListFull = ytListFull
    for fileWay in ytList:
        fileWay = fileWay.replace('\\', '/')
        fileWay = fileWay.split('/')
        fileWaySplit.append(fileWay)
    filesListSplited = fileWaySplit
    i = 0
    for flway in filesListFull:
        fileWay = None
        filname = filesListSplited[i][-1]
        fileWay = flway.replace(filname, '')
        if filname.find(' ')!=(-1):
            filname = filname.replace(' ', '-')
            os.rename(flway, fileWay+filname)
        i+=1
    ytList = glob.glob(way, recursive=True)
    for fileWay in ytList:
        fileWay = fileWay.replace('\\', '/')
        fileWay = fileWay.replace(wayConf, '')
        ytListCleaned.append(fileWay)
    for fileWay in ytList:
        fileWay = fileWay.replace('\\', '/')
        fileWay = fileWay.replace(wayConf, '')
        fileWay = fileWay.split('/')
        fileWaySplitCleaned.append(fileWay)
    filesListFullc = ytListCleaned
    filesListSplitedc = fileWaySplitCleaned
    cfg = configparser.ConfigParser()
    with open(libName, 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    way = wayConf
    k = 0
    optlisting = optlist(libName, type) # из файла с параметрами
    for fileway in filesListSplitedc:
        file = filesListFullc[k]
        file = file.replace(confDir, '')
        category = fileway[0]
        channel = fileway[1]
        videoname = fileway[2]
        id = cfg.options('keywords')
        id = id[-1]
        id = id.replace(libPrefix, '')
        id = str(1 + int(id))
        id = libPrefix+id
        if cfg.has_section(channel) == True:
            # filey = file.replace('.mp4', '')
            filey = file
            if checkDoubles(optlisting, filey)==True:
                pass
            else:
                cfg.set(type, id, file)
                filen = file.replace('.mp4', '')
                cfg.set('keywords', id, filen)
                cfg.set(channel, id, 'True')
        else:
            cfg.add_section(channel)
            cfg.set(channel, '-1', 'None')   
            cfg.set(type, id, file)
            filen = file.replace('.mp4', '')
            cfg.set('keywords', id, filen)
            cfg.set(channel, id, 'True')
        k+=1
    print('found '+str(k)+' files')
    for filewayl in optlisting:
        # print(filewayl)
        # filel = filewayl[2]
        filel = filewayl[1]
        filewayle = way + confDir + filel
        if os.path.exists(filewayle)==True:
            # print('found '+filel)
            pass
        else:
            idl = filewayl[0]
            if idl!=str(-1):
                channel = (filewayl[2].split('/'))[0]
                # channel = (filewayl[1].split('/'))[0]
                cfg.remove_option('keywords', idl)
                cfg.remove_option(type, idl)
                cfg.remove_option(channel, idl)
    with open(libName, 'w', encoding='utf-8') as fp:
        cfg.write(fp)

def isVideoIDExist(id):
    cfg = configparser.ConfigParser()
    with open('settings.ini', 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    if cfg.has_option('prefixes', id[0])==True:
        categ = cfg.get('prefixes', id[0])
        libName = cfg.get('libs', categ)
        with open(libName, 'r', encoding='utf-8') as fp:
            cfg.read_file(fp)
            if cfg.has_option(categ, id)==True:
                return True
            else:
                return False
    else: 
        return False

def getLinkId(id):
    cfg = configparser.ConfigParser()
    with open('settings.ini', 'r', encoding='utf-8') as fp:
        cfg.read_file(fp)
    wayConf = cfg.get('settings', 'way')
    if isVideoIDExist(id)==True:
        if cfg.has_option('prefixes', id[0]):
            categ = cfg.get('prefixes', id[0])
            wayParam = categ + 'folder'
            wayConf = wayConf + cfg.get('settings', wayParam)+'/'
            libName = cfg.get('libs', categ)
            with open(libName, 'r', encoding='utf-8') as fp:
                cfg.read_file(fp)
            fullway = wayConf + cfg.get(categ, id)
            return fullway
        else: 
            return False # check usage!
    else: return None
listRebuild(type='youtube')