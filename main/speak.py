import torch
import sounddevice as sd
import time
import datetime
import num2word

lang = "cyrillic"      #определение языка и модели
model_id = 'v4_cyrillic'

device = torch.device('cpu')  #использование ram памяти 


model , _ = torch.hub.load(repo_or_dir='snakers4/silero-models',   #получение модели с помощью библиотеки torch
                           model = 'silero_tts',
                           language=lang,
                           speaker=model_id)
model.to(device)

def speaker(text):  
    sample_rate = 48000   #определение дискретизации 
    speaker = "kz_M2"  #Выбор спикера
    put_accent = True  #Настройка речи
    put_yo = True
    audio = model.apply_tts(text=text,         #Создание аудио
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)
    print(text)

    sd.play(audio , sample_rate)  #проигрыватель аудио
    time.sleep(len(audio) / sample_rate)
    sd.stop()

hour = int(datetime.datetime.now().hour)
if hour>= 0 and hour<12:
    speaker("Қайырлы таң")
  
elif hour>= 12 and hour<18:
    speaker("Қайырлы күн")   
  
else:
    speaker("Қайырлы кеш")

speaker("Мен жұмыс істеуге дайынмын!")

