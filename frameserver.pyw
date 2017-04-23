#! python3

from os import listdir, path, remove, system, makedirs
from time import sleep
from sys import argv, stdin
import re

try:
    from send2trash import send2trash
except:
    print('''...не то что бы это очень нужно, но всё же было бы клево, если бы здесь был пакет send2trash ^__^
          pip install send2trash
          (ибо иногда AFS не может удалить временный .avi файл, при этом он нигде не открыт и успешно удаляется руками...
          ...поэтому, здесь есть костыль для разруливания таких ситуаций...
          ....НО........
          *драматичная пауза*
          что если нужный тебе .avi файл СЛУЧАЙНО попадает в папку для подхвата файлов из AFS, и после удаляется через os.remove?
          ....чтобы облегчить восстановление - и используется удаление через send2trash, название которого как бы намекает...)''')

default_wdir = path.join(path.expanduser('~'), 'AFS_OUTPUT') # <=> %HOMEPATH%\AFS_OUTPUT\
default_audio = '-c:a aac -b:a 576k -cutoff 18000'
default_verbosity = '-stats -hide_banner -loglevel 16' # только прогресс кодирования
avs_name = 'frameserver_tmp.avs'
console_settings = 'mode con: cols=100 lines=20 && chcp 65001 && cls && '
# TODO: более быстрые настройки для ffmpeg

def get_file(folder):
    for i in listdir(folder):
        if '.avi' in path.splitext(i):
            return path.join(wdir, i)


def write_avs(name):
    with open(path.join(wdir, avs_name), 'w') as avs:  # , 'utf-8'.... но AviSynth всё равно не умеет :с
        avs.write('AviSource("{}")'.format(name))


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

def simple_coder(curret_file):
    out_name = path.splitext(curret_file)[0]
    system(console_settings + 'ffmpeg {verbosity} -y -i "{avs}" {scale} -c:v libx264 -crf {rate_factor} -pix_fmt yuv420p {audio} "{out} fs_x264.mp4"'.format(
            avs = path.join(wdir, avs_name),
            out = out_name,
            audio = '-an' if ' -an' in out_name else default_audio,
            scale = get_scale(out_name),
            rate_factor = get_crf(out_name),
            verbosity = default_verbosity
        )
    )


def error_output(e = ''):
    system('Pause>nul|(echo Тут когда-то было очень информативное сообщение об ошибке, и если повезет - после нажатия enter, ты, человек, его увидишь... )')
    print(e)


def rm_avi(fn):
    try:
        send2trash(fn) # чисто гипотетически - вдруг в папку вывода случайно попадает обычный .avi 
    except:
        try:
            remove(fn)
        except:
            pass


def mk_wdir(fp):
    if not path.isdir(fp):
        makedirs(fp)
    return fp


def get_wdir():
    if len(argv) > 1:
        d = ' '.join(argv[1:])
        if path.isdir(d):
            return d
        else:
            print('...?? д-директория не существует?')
            return mk_wdir(default_wdir)
    else:
        if stdin: # Если есть консоль <=> запуск не в фоне
            while True:
                wdir = input('Директория для подхвата .avi из AFS\n...или просто enter для использования пути по умолчанию:\n    {}\n>>> '.format(default_wdir))
                if path.isdir(wdir):
                    return wdir
                elif wdir == '':
                    break
                else:
                    print('...кажется, директория не существует...\nЕще раз!♥\n')
        return mk_wdir(default_wdir)


def fmt_cf(string):
    name = path.split(string)[1]
    if len(name) > 39:
        name = name[:18] + '...' + name[-18:]
    return name


def main():
    curret_file = get_file(wdir)
    result = False
    if curret_file:
        write_avs(curret_file)
        simple_coder(curret_file)
        result = True
        try:
            remove(path.join(wdir, avs_name))
        except:
            pass
    return result, curret_file


if __name__ == '__main__':
    wdir = get_wdir()
    print('{} - принято♥\n\n'.format(wdir))
    while True:
        try:
            encoded, curfile = main()
            if encoded:
                print('{} - закодированно последним♥ Быть может, даже успешно... 15s tm\n'.format(fmt_cf(curfile)))
                sleep(15)
                rm_avi(curfile)
            else:
                sleep(3)
        except Exception as e:
            error_output(e)
            sleep(10)