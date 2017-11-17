#! python3

from os import listdir, path, remove, system, makedirs
from time import sleep
from sys import stdin
from random import random
import re
import argparse

default_wdir = path.join(path.expanduser('~'), 'AFS_OUTPUT') # <=> %HOMEPATH%\AFS_OUTPUT\
default_audio = '-c:a aac -b:a 576k -cutoff 18000'
default_rf = '-crf 18'
default_verbosity = '-stats -hide_banner -loglevel 16' # только прогресс кодирования
avs_name = 'frameserver_tmp_{}.avs'
console_settings = 'mode con: cols=100 lines=20 && ' if not stdin else ''

console_settings += 'chcp 65001 && cls && '

# TODO: более быстрые настройки для ffmpeg

def get_args():
    parser = argparse.ArgumentParser(description = 'AFS-компаньон') 
    parser.add_argument('--wdir', '-w', required = False, default = default_wdir, help = 'Путь к папке, куда из AME/PP CC тобой будут отправляться .avi файлы-прокси, по умолчанию: {}'.format(default_wdir))
    return parser.parse_args()


def get_file(folder):
    for i in listdir(folder):
        if '.avi' in path.splitext(i):
            return path.join(folder, i)


def write_avs(name):
    folder = path.split(name)[0]
    with open(path.join(folder, avs_name), 'w') as avs:  # , 'utf-8'.... но AviSynth всё равно не умеет :с
        avs.write('AviSource("{}")'.format(name))


def encode(curret_file):
    patterns = {
        'scale': 'scale=(\-)?\d+,(\-)?\d+', 
        'rate_factor': '-crf \d+', 
        'no_audio': '\ -an'
    }

    def get_scale(string):
        try:
            return '-vf {} -sws_flags lanczos'.format(re.search(patterns['scale'], string).group().replace(',', ':'))
        except Exception as e:
            print('scale: {}'.format(e))
            return ''

    def get_crf(string):
        try:
            rf = re.search(patterns['rate_factor'], string).group()
            assert int(rf.split()[1]) in range(52)
            return rf
        except Exception as e:
            print('crf: {}'.format(e))
            return default_rf

    def get_final_name(string):
        for _, p in patterns.items():
            string = re.sub(p, '', string)
        return ' '.join(string.split())

    out_name = path.splitext(curret_file)[0]
 
    cmd = console_settings + 'ffmpeg {verbosity} -y -i "{avs}" {scale} -c:v libx264 {rate_factor} -pix_fmt yuv420p -movflags faststart {audio} "{out}.mp4"'.format(
        avs = path.join(path.split(curret_file)[0], avs_name),
        out = get_final_name(out_name),
        audio = '-an' if ' -an' in out_name else default_audio,
        scale = get_scale(out_name),
        rate_factor = get_crf(out_name),
        verbosity = default_verbosity
    )

    return system(cmd)


def print_msg(e = ''):
    if stdin:
        print(e)
    else:
        system('Pause>nul|(echo "{}")'.format(e))


def shorten_name(string):
    name = path.split(string)[1]
    if len(name) > 39:
        name = name[:18] + '...' + name[-18:]
    return name


def main(wdir):
    curret_file = get_file(wdir)
    if curret_file:
        write_avs(curret_file)
        res = encode(curret_file)
        if res != 0:
            raise Exception('Что-то пошло не так при кодировании, удачи тебе выяснить, что\n\n ^__^\n\n\n...Например, у видео могло быть разрешение, неделимое на 2 по какой-то из сторон')
        
        print('{} - закодированно последним♥ 15s tm\n'.format(shorten_name(curret_file)))

        try:
            remove(path.join(wdir, avs_name))
            sleep(12)
            remove(curret_file)
        except:
            pass
    else:
        sleep(1)


if __name__ == '__main__':
    args = get_args()

    if not path.isdir(args.wdir):
        makedirs(args.wdir)

    wd = path.abspath(args.wdir)

    print('{} - принято♥\n\n'.format(wd))

    while True:
        try:
            avs_name = avs_name.format(random())
            main(wd)
        except Exception as e:
            print_msg(e)
            sleep(10)