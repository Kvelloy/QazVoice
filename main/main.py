import json
import queue
import os
import sys
import threading
from sklearn.feature_extraction.text import CountVectorizer     
from sklearn.linear_model import LogisticRegression
import sounddevice as sd    
import vosk                 
import word
import commands          
import speak
from gui import App



vosk.SetLogLevel(1)
q = queue.Queue()  #Создаем очередь

model = vosk.Model(lang="kz")    #Создание модели

try:
    default_device = sd.default.device  #Определяем устройство ввода звука по умолчанию

    samplerate = int(sd.query_devices(default_device[0], 'input')['default_samplerate'])  #получаем частоту микрофона
except:
    speak.speaker('Микрофонды қос')  #при ошибке завершаем программу
    sys.exit(1)
print(default_device)

def callback(indata, frames, time, status):
    q.put(bytes(indata))  #Добавляем в очередь полученные данные


def recognize(data, vectorizer, clf):
    
    if len(data) < 7:   #пропускаем слова если его длина меньше 7
        return
    
    #если нет фразы обращения к ассистенту, то завершаем код

    trigger = 0
    for w in data.split():
        for t in word.TRIGGERS:
            if t in w or w in t:
                trigger = 1
                break
        if trigger == 1:
            break
    if trigger == 0:
        return
    
    
    data_vct = data.split()  
    clear_data = [w for w in data_vct for t in word.TRIGGERS if t not in w or w not in t]   #удаляем из команды имя асистента
    data_vct = ' '.join(clear_data)
    #получаем вектор полученного текста
    #сравниваем с вариантами, получая наиболее подходящий ответ
    # Преобразование команды пользователя в числовой вектор
    command_vector = vectorizer.transform([data_vct])
    # Предсказание вероятностей принадлежности к каждому классу
    predicted_probabilities = clf.predict_proba(command_vector)

    # Задание порога совпадения
    probability = 0.2
    answer = None
    # Поиск наибольшей вероятности и выбор ответа, если он превышает порог
    max_probability = max(predicted_probabilities[0])
    if max_probability >= probability:
        answer = clf.classes_[predicted_probabilities[0].argmax()]
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


def main():
    print('Тыңдап тұрмыз')
    

    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(word.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(word.data_set.values()))


    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=default_device[0], dtype='int16',
                            channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(data)
                recognize(data, vectorizer, clf)

    
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