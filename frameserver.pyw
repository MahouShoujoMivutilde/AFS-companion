from os import listdir, path, remove, system
from time import sleep
import re

d = r'C:\ENCODE'
avs_name = 'frameserver.avs'

# TODO: более быстрые настройки для ffmpeg

def get_file(folder):
    for i in listdir(folder):
        if '.avi' in path.splitext(i):
            return path.join(d, i)


def write_avs(name):
    with open(path.join(d, avs_name), 'w') as avs:  # , 'utf-8'.... но AviSynth всё равно не умеет :с
        avs.write('AviSource("{}")'.format(name))  # \nConvertToYV24(matrix="rec709")


def get_scale(string):
    try:
        return '-vf scale={sc[0]}:{sc[1]} -sws_flags lanczos'.format(sc=[int(_) for _ in re.search('scale=(\-)?\d+,(\-)?\d+', string)[0][6:].split(',')])
    except:
        return ''


def simple_coder(curret_file):
    out_name = path.splitext(curret_file)[0]  # .replace(' ', '_')
    system('chcp 65001 && cls && ffmpeg -stats -hide_banner -loglevel 16 -y -i "{avs}" {crop_or_scale}\
            -c:v libx264 -crf 18 -pix_fmt yuv420p {audio} "{out} fs_x264.mp4"'.format(
            avs=path.join(d, avs_name),
            out=out_name,
            audio='-an' if (' no_audio' in out_name or ' -an' in out_name) else '-c:a aac -b:a 576k -cutoff 18000',
            crop_or_scale=get_scale(out_name)
        )
    )


def error_output(e):
    system('Pause>nul|(echo Тут когда-то было очень информативное сообщение об ошибке, но - увы... :c)')  # .replace('\n', '    ').replace('\r', '')
    print(e)


def main():
    curret_file = get_file(d)
    result = False
    if curret_file:
        write_avs(curret_file)
        simple_coder(curret_file)
        result = True
        try:
            remove(path.join(d, avs_name))
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