import glob
import os

list = glob.glob('*.*')
for element in list:
    wayto = os.path.abspath(element)
    wayto = wayto.split('\\')
    del wayto[-1]
    del wayto[-1]
    wayto.append('cgi-bin')
    wayto.append(element)
    wayto='/'.join(wayto)
    wayfrom = os.path.abspath(element)
    command = 'mklink "'+wayto+'" "'+wayfrom+'"'
    os.system(command)