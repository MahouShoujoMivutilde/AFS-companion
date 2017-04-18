#### Скрипт-компаньон для [Advanced FrameServer](http://advancedfs.sourceforge.net/)
Рассчитан на работу вместе [AviSynth](http://avisynth.nl/index.php/Main_Page) и [FFmpeg](http://ffmpeg.zeranoe.com/builds/) 32bit (из-за AviSynth только 32, увы) на `python 3.3+` и на автозапуск в фоне.

Предполагает, что в настройках AFS выбраны параметры `stop serving when idle` и `idle timeout` установлен на 10 секунд - минимальное доступное время.

Временный AVI-файл из AFS дефолтно должен быть сохранен в `C:\ENCODE\`, оттуда скрипт его автоматически подхватит, начиная кодирование с найденными параметрами или своими дефолтными.

Кстати, о параметрах:
* `my file name scale=w,h.avi` в итоге даст масштаб `w` и `h` абсолютно аналогично опции FFmpeg `-vf scale=w:h -sws_flags lanczos`, например:
* * `scale=-2,1080` отмасштабирует до 1080px по высоте, сохраняя при этом делимость на 2 ширины (нужно для кодека x264)
* `my file name -an.avi` уберет аудио - *сделано специально для mp4-анимаций telegram*

Параметры можно комбинировать, разумеется.

Протестировано и успешно работает на
* Adobe Premiere Pro CC 2017 и Adobe Media Encoder CC 2017
* `python 3.6.1`
* `AviSynth 2.6.0.6`
* `FFmpeg 3.2.4 win32 shared`

Из-за AviSynth боится всяких кандзи и прочего юникода в названиях файлов. Увы. 