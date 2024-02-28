import time
st = time.time()

import json
import queue
import os
import sys
import threading
from fuzzywuzzy import process
import sounddevice as sd    
import vosk                 
import word
import commands          
import speak
from gui import App
from ttt import chat_gpt




q = queue.Queue()  #Создаем очередь

model = vosk.Model("vosk-model-kz-0.15")    #Создание модели

try:
    default_device = sd.default.device  #Определяем устройство ввода звука по умолчанию

    samplerate = int(sd.query_devices(default_device[0], 'input')['default_samplerate'])  #получаем частоту микрофона
except:
    speak.speaker('Микрофонды қос')  #при ошибке завершаем программу
    sys.exit(1)


def callback(indata, frames, time, status):
    q.put(bytes(indata))  #Добавляем в очередь полученные данные


def recognize(data):
    
    if len(data) < 7:   #пропускаем слова если его длина меньше 7
        return
    
    #если нет фразы обращения к ассистенту, то завершаем код
    data = data.split()
    trigger = 0
    _ , per1 = process.extractOne(data[0], word.TRIGGERS)
    _ , per2 = process.extractOne(data[0], word.CHAT_GPT_TRIGGERS)
    if per1 >= 55:
        data = " ".join(data)
        data_vct = data.split()  
        clear_data = [w for w in data_vct for t in word.TRIGGERS if t not in w or w not in t]   #удаляем из команды имя асистента
        data_vct = ' '.join(clear_data)
        #получаем вектор полученного текста
        #сравниваем с вариантами, получая наиболее подходящий ответ
        # Преобразование команды пользователя в числовой вектор
        answer = None
        ans, procent = process.extractOne(data, word.data_set.keys())
        if procent >= 65:
            answer = word.data_set[ans]
        else:
            speak.speaker("Команда табылмады")
            return
        

        #получение имени функции из ответа из data_set
        func_name = answer.split()[0]

        #озвучка ответа из модели data_set
        speak.speaker(answer.replace(func_name, ''))

        #запуск функции из commands
        if func_name != "wiki":
            exec('commands.' + func_name + '()')
        else:
            commands.wiki(data)

    elif per2 >= 55:
        data.pop(0)
        data = " ".join(data)
        speak.speaker(chat_gpt(data))


def main():
    print('Тыңдап тұрмыз')
    print(time.time() - st)

    


    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=default_device[0], dtype='int16',
                            channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            sd.stop()
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(data)
                recognize(data)
                

    
def main_thread():
    # Вызовите вашу функцию main здесь
    main()

def gui_thread():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_thread)
    gui_thread = threading.Thread(target=gui_thread)

    main_thread.start()
    gui_thread.start()

    main_thread.join()
    gui_thread.join()
