# run as module
import configparser
import glob
import os
g = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')+'/'
import HTML
import datetime
import sys
import traceback
cfg = configparser.ConfigParser()
# print(g)
with open(g+'settings.ini', 'r', encoding='utf-8') as fp:
    cfg.read_file(fp)

def optlist(libname, searchType):
    g = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')+'/'
    cfgll = configparser.ConfigParser()
    with open(g+libname, 'r', encoding='utf-8') as fp:
        cfgll.read_file(fp)
    lst = []
    i = cfgll.options(searchType)
    for opt in i:
        g = cfgll.get(searchType, opt)
        # p = cfgll.get('keywords', opt)
        # lstq = [opt, g, p]
        lstq = [opt, g]
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

def catsmeow():
    # cfg = configparser.ConfigParser()
    # with open('settings.ini', 'r', encoding='utf-8') as fp:
    #     cfg.read_file(fp)
    catlist = cfg.options('libs')
    return catlist

def filesListSplitFunc(listing, mode, wayConfig):
    g = []
    for fileWay in listing:
        fileWay = fileWay.replace('\\', '/')
        if mode == True:
            fileWay = fileWay.replace(wayConfig, '')
        fileWay = fileWay.split('/')
        g.append(fileWay)
    return g

def filesListFullFunc(listing, mode, wayConfig):
    g = []
    for fileWay in listing:
        fileWay = fileWay.replace('\\', '/')
        if mode == True:
            fileWay = fileWay.replace(wayConfig, '')
        g.append(fileWay)
    return g

def listRebuild(mode):
    g = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')+'/'
    catlist = catsmeow()
    # cfg = configparser.ConfigParser()
    new = []
    for libType in catlist:
        # with open('settings.ini', 'r', encoding='utf-8') as fp:
        #     cfg.read_file(fp)
        libPrefix = libType[0]
        folderConf = libType + 'folder'
        confDir = libType + '/'
        libName = cfg.get('libs', libType)
        wayConf = cfg.get('settings', 'way')
        folderDir = cfg.get('settings', folderConf)
        way = wayConf + folderDir + '/*/*.*'
        fileList = glob.glob(way, recursive=True)
        filesListFull = filesListFullFunc(fileList, False, wayConf)
        filesListSplited = filesListSplitFunc(fileList, False, wayConf)
        i = 0
        for flway in filesListFull:
            fileWay = None
            filname = filesListSplited[i][-1]
            fileWay = flway.replace(filname, '')
            restricted1 = ['#', '$', '%', '+', '*', '&', '?', '=', '---', '--', '___', '__', '   ', '  ']
            restricted2 = ['-']
            for j in restricted1:
                filname=filname.replace(j, '')
            for j in restricted2:
                filname=filname.replace(j, ' ')
            os.rename(flway, fileWay+filname)
            i+=1
        fileList = glob.glob(way, recursive=True)
        filesListFull = filesListFullFunc(fileList, True, wayConf)
        filesListSplited = filesListSplitFunc(fileList, True, wayConf)
        if mode == 'full':
            f = open(g+libName, 'w')
            f.close()
            cfgly = configparser.ConfigParser()
            with open(g+libName, 'r', encoding='utf-8') as fp:
                cfgly.read_file(fp)
            cfgly.remove_section('keywords')
            cfgly.remove_section(libType)
            cfgly.add_section(libType)
            cfgly.set(libType, '-1', 'None')
            with open(g+libName, 'w', encoding='utf-8') as fp:
                cfgly.write(fp)
        if mode == 'update':
            pass
        cfgl = configparser.ConfigParser()
        with open(g+libName, 'r', encoding='utf-8') as fp:
            cfgl.read_file(fp)
        way = wayConf
        k = 0
        optlisting = optlist(libName, libType) # из файла с параметрами
        for fileway in filesListSplited:
            file = filesListFull[k]
            file = file.replace(confDir, '')
            channel = fileway[1]
            id = libPrefix+str(1 + int(cfgl.options(libType)[-1].replace(libPrefix, '')))
            if cfgl.has_section(channel) == True:
                if checkDoubles(optlisting, file)==True:
                    pass
                else:
                    cfgl.set(libType, id, file)
                    cfgl.set(channel, id, 'True')
            else:
                cfgl.add_section(channel)
                cfgl.set(channel, '-1', 'None')   
                cfgl.set(libType, id, file)
                cfgl.set(channel, id, 'True')
            k+=1
        for filewayl in optlisting:
            filel = filewayl[1]
            filewayle = way + confDir + filel
            if os.path.exists(filewayle)==True:
                pass
            else:
                idl = filewayl[0]
                if idl!=str(-1):
                    channel = (filewayl[1].split('/'))[0]
                    cfgl.remove_option(libType, idl)
                    cfgl.remove_option(channel, idl)
        with open(g+libName, 'w', encoding='utf-8') as fp:
            cfgl.write(fp)
           

def isVideoIDExist(id):
    # cfg = configparser.ConfigParser()
    # with open('settings.ini', 'r', encoding='utf-8') as fp:
    #     cfg.read_file(fp)
    if cfg.has_option('prefixes', id[0])==True:
        categ = cfg.get('prefixes', id[0])
        libName = cfg.get('libs', categ)
        with open(g+libName, 'r', encoding='utf-8') as fp:
            cfg.read_file(fp)
            if cfg.has_option(categ, id)==True:
                return True
            else:
                return False
    else: 
        return False

def getLinkId(id):
    # cfg = configparser.ConfigParser()
    # with open('settings.ini', 'r', encoding='utf-8') as fp:
    #     cfg.read_file(fp)
    # wayConf = cfg.get('settings', 'way')
    wayConf = cfg.get('links', 'webdir')+'storage/'
    # if isVideoIDExist(id)==True:
    if cfg.has_option('prefixes', id[0]):
        categ = cfg.get('prefixes', id[0])
        wayParam = categ + 'folder'
        wayConf = wayConf + cfg.get('settings', wayParam)+'/'
        libName = cfg.get('libs', categ)
        with open(g+libName, 'r', encoding='utf-8') as fp:
            cfg.read_file(fp)
        if cfg.has_option(categ, id)==True:
            fullway = wayConf + cfg.get(categ, id)
            return fullway
        else:
            return False
    else: 
        return False # check usage!

def updateList(mode, new):
    separater = '<!-- DONOTDELETE -->'
    wayfy = cfg.get('settings', 'way').replace('storage/', '')
    # indexHTML = wayfy+'index.html'
    searchHTML = wayfy+'search.html'
    updatesHTML = wayfy+'updates.html'
    # lister = [indexHTML, searchHTML, updatesHTML]
    lister = [searchHTML, updatesHTML]
    now = datetime.datetime.now()
    timing = now.strftime(r'%d.%m.%Y %H:%M:%S')
    fut = '<p>The file database has been completely updated. Total files in db - {files}</p>\n'
    putt = '<p>The file database has been partially updated. New {files} files are shown below.</p>\n'
    alert = '<p>Latest filebase update - {time}</p>'
    updt = '<h4>{time} - {searchType} update</h4>\n'
    if mode == 'full':
        upd = separater + '\n' + updt.format(time=timing, searchType='Full') + fut.format(files=str(len(new)))
    elif mode == 'update' and len(new)>0:
        upd = separater + '\n' + updt.format(time=timing, searchType='Partially') + putt.format(files=str(len(new))) + HTML.table(new)
    else:
        upd = separater
    alrt = alert.format(time=timing)
    for file in lister:
        with open(file, 'r', encoding='UTF-8') as f:
            # lines = f.readlines()
            lines = f.read().splitlines()
            # lines.split('\n')
            nf = []
            for element in lines:
                if alert.split('-')[0] in element:
                    nf.append(alrt)
                else:
                    nf.append(element)
            nfn = []
            for element in nf:
                if element == r'\n' or element=='' or element==None:
                    pass
                else:
                    nfn.append(element)
            nf = '\n'.join(nfn)
        with open(file, 'w', encoding='UTF-8') as f:
            f.writelines(nf)
    k = 0
    with open(updatesHTML, 'r', encoding='UTF-8') as f:
        lines = f.read().splitlines()
        nnl = []
        for element in lines:
            if element in separater:
                if k==0:
                    nnl.append(upd)
                else: k+=1
            else:
                nnl.append(element)
        nfn = []
        for element in nnl:
            if element == r'\n' or element=='' or element==None:
                pass
            else:
                nfn.append(element)
        nnl = '\n'.join(nfn)
    with open(updatesHTML, 'w', encoding='UTF-8') as f:
        f.writelines(nnl)

try:
    # print(sys.argv)
    if sys.argv[-1]=='full':
        listRebuild(mode='full')
    elif sys.argv[-1]=='update':
        listRebuild(mode='update')
    else:
        listRebuild(mode='update')
except Exception as e:
    print(traceback.format_exc())

# listRebuild(mode='full')