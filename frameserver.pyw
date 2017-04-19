#! python3

from os import listdir, path, remove, system
from time import sleep
import re

default_wdir = r'C:\ENCODE'
default_audio = '-c:a aac -b:a 576k -cutoff 18000'
default_verbosity = '-stats -hide_banner -loglevel 16' # только прогресс кодирования
avs_name = 'frameserver_tmp.avs'
console_size = 'mode con: cols=100 lines=20 && '
# TODO: более быстрые настройки для ffmpeg

def get_file(folder):
    for i in listdir(folder):
        if '.avi' in path.splitext(i):
            return path.join(default_wdir, i)


def write_avs(name):
    with open(path.join(default_wdir, avs_name), 'w') as avs:  # , 'utf-8'.... но AviSynth всё равно не умеет :с
        avs.write('AviSource("{}")'.format(name))  # \nConvertToYV24(matrix="rec709")


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
            raise 'actually not in [0-51] range'
    except:
        return 18

def simple_coder(curret_file):
    out_name = path.splitext(curret_file)[0]  # .replace(' ', '_')
    system(console_size + 'chcp 65001 && cls && ffmpeg {verbosity} -y -i "{avs}" {scale} \
            -c:v libx264 -crf {rate_factor} -pix_fmt yuv420p {audio} "{out} fs_x264.mp4"'.format(
            avs=path.join(default_wdir, avs_name),
            out=out_name,
            audio='-an' if (' no_audio' in out_name or ' -an' in out_name) else default_audio,
            scale=get_scale(out_name),
            rate_factor=get_crf(out_name),
            verbosity=default_verbosity
        )
    )


def error_output(e):
    system('Pause>nul|(echo Тут когда-то было очень информативное сообщение об ошибке, но - увы... :c)')  # .replace('\n', '    ').replace('\r', '')
    print(e)


def main():
    curret_file = get_file(default_wdir)
    result = False
    if curret_file:
        write_avs(curret_file)
        simple_coder(curret_file)
        result = True
        try:
            remove(path.join(default_wdir, avs_name))
        except:
            pass
    return result

if __name__ == '__main__':
    while True:
        try:
            encoded = main()
            if encoded:
                print('encoded, 15s timeout')
                sleep(15)
            else:
                print('nothing found, 3s timeout')
                sleep(3)
        except Exception as e:
            error_output(e)
            sleep(10)