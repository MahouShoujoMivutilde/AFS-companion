#! python3

from os import listdir, path, remove, system, makedirs
from time import sleep
from sys import stdin
from random import random
import re
import argparse

default_wdir = path.join(path.expanduser('~'), 'AFS_OUTPUT') # <=> %HOMEPATH%\AFS_OUTPUT\
default_audio = '-c:a aac -b:a 576k -cutoff 18000'
default_verbosity = '-stats -hide_banner -loglevel 16' # только прогресс кодирования
avs_name = 'frameserver_tmp_{}.avs'
console_settings = 'mode con: cols=100 lines=20 && chcp 65001 && cls && ' if not stdin else ''
# TODO: более быстрые настройки для ffmpeg

def get_args():
    parser = argparse.ArgumentParser(description = "AFS-компаньон") 
    parser.add_argument("--wdir", "-w", required = False, default = default_wdir, help = "Путь к папке, куда из AME/PP CC будут отправляться .avi файлы-прокси")
    return parser.parse_args()


def get_file(folder):
    for i in listdir(folder):
        if '.avi' in path.splitext(i):
            return path.join(folder, i)


def write_avs(name):
    folder = path.split(name)[0]
    with open(path.join(folder, avs_name), 'w') as avs:  # , 'utf-8'.... но AviSynth всё равно не умеет :с
        avs.write('AviSource("{}")'.format(name))


def simple_coder(curret_file):
    def get_scale(string):
        try:
            return '-vf scale={sc[0]}:{sc[1]} -sws_flags lanczos'.format(sc=[int(_) for _ in re.search('scale=(\-)?\d+,(\-)?\d+', string)[0][6:].split(',')])
        except:
            return ''

    def get_crf(string):
        try:
            crf = int(re.search('-crf \d+', string)[0][5:])
            if crf in range(52):
                return crf
            else:
                raise Exception('actually not in [0-51] range')
        except:
            return 18

    out_name = path.splitext(curret_file)[0]
    cmd = console_settings + 'ffmpeg {verbosity} -y -i "{avs}" {scale} -c:v libx264 -crf {rate_factor} -pix_fmt yuv420p -movflags faststart {audio} "{out} fs_x264.mp4"'.format(
        avs = path.join(path.split(curret_file)[0], avs_name),
        out = out_name,
        audio = '-an' if ' -an' in out_name else default_audio,
        scale = get_scale(out_name),
        rate_factor = get_crf(out_name),
        verbosity = default_verbosity
    )
    
    return system(cmd)


def error_output(e = ''):
    if stdin:
        print(e)
    else:
        system('Pause>nul|(echo Тут когда-то было очень информативное сообщение об ошибке, и если повезет - после нажатия enter, ты, человек, его увидишь... )')


def fmt_cf(string):
    name = path.split(string)[1]
    if len(name) > 39:
        name = name[:18] + '...' + name[-18:]
    return name


def main(wdir):
    curret_file = get_file(wdir)
    if curret_file:
        write_avs(curret_file)
        res = simple_coder(curret_file)
        if res != 0:
            raise Exception('Что-то пошло не так при кодировании, удачи тебе выяснить, что\n\n ^__^\n\n\n...Например, у видео могло быть разрешение, неделимое на 2 по какой-то из сторон')
        
        print('{} - закодированно последним♥ 15s tm\n'.format(fmt_cf(curret_file)))

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
            error_output(e)
            sleep(10)