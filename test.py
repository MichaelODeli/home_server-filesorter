import configparser
cfg = configparser.ConfigParser()
with open('storageLib_Youtube.ini', 'r', encoding='utf-8') as fp:
    cfg.read_file(fp)

def read(cfg):
    return cfg.get('youtube', 'y1')

def setu(cfg):
    cfg.set('youtube', 'y1', 'passed')

print(read(cfg))
setu(cfg)
print(read(cfg))