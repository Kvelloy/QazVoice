import os
import webbrowser
import sys
import subprocess
import config
import speak
import random
import requests
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import translator
import pyglet
import wikipedia
import num2word
import geocoder 
import datetime

#функция для мотиваций
motivation_list = [
    "Жетістік - бұл соңғы нүкте емес. Қозғалуды тоқтатпаңыз!",
    "Бүгінгі істі ертеңге қалдырмаңыз. Ертеңгі күн болмай қалуы да мүмкін!",
    "Сіз қазір қай жерде екенініз маңызды емес, жолыңыз қай жерге апаратыны маңызды.",
    "Егер де табындылық болса, әр мақсатқа жете аласыз!",
    "Сіздің шектеулеріңіз-бұл сіздің шектеулерге деген сеніміңіз.",
    "Өзіңізге сеніңіз, сонда сіз екі есе күшті боласыз.",
    "Болашақты болжаудың ең сенімді жолы - оны жасау.",
    "Сәтсіздіктерден қорықпаңыз. Олар тек табысқа жету қадамдары.",
    "Егер сіз тырыспасаңыз, сіз қазірдің өзінде ұтылып тұрсыз.",
    "Жаңа нәрсені бастаудың ең жақсы уақыты кеше болды. Келесі ең жақсы уақыт-қазір."
]
motivations = motivation_list[:]

def motivation():
    global motivations
    if len(motivations) == 0:
        motivations = motivation_list.copy()
    else:
        random_motivation = random.choice(motivations)
        motivations.remove(random_motivation)
        speak.speaker(random_motivation)

#функция для фактов
facts = [
    "Мұхиттар жер бетінің жетпіс бір пайызын құрайды.",
    "Әлемдегі ең ұзын тау жотасы - Гималай, оның ұзындығы шамамен екі мың төрт жүз шақырым.",
    "Италиядағы Венеция жүз он сегіз кішкентай аралдан тұрады.",
    "Жер бетінде жануарлардың миллион бес жүз мыңнан астам түрі белгілі.",
    "Ғалам шамамен он үш миллиард жаста деп есептеледі.",
    "Шахмат Үндістанда ойлап табылған.",
    "Айдағы тауларда Альпі, Карпат және Гималай сияқты атаулар бар.",
    "Бамбук-планетадағы ең жылдам өсетін өсімдік түрі.",
    "Колибри-артқа ұшуға қабілетті жалғыз құс.",
    "Вакуум дыбысты жібере алмайды, сондықтан ғарыш мүлдем үнсіз.",
    "Піл сүйегі қырық пайыз судан тұрады.",
    "Жирафтардың мойнында адам сияқты омыртқалардың саны бірдей.",
    "Адам күлімсіреу үшін елуден астам бұлшықетті пайдаланады.",
    "Әлемде барлығы жеті мыңнан астам түрлі тіл бар.",
    "Жердегі су Күн жүйесіндегі барлық судың бір пайызынан азын құрайды.",
    "Эверест тауы жылына шамамен төрт миллиметрге өседі.",
    "Бүркіттер олжаны үш шақырымға дейінгі қашықтықтан көре алады.",
    "Австралияда адамдарға қарағанда қой көбірек.",
    "Күн негізінен сутегі мен гелийден тұрады.",
    "Адам ағзасындағы барлық қан тамырларының ұзындығы тоқсан алты мың шақырымнан асады."
]

fact = facts[:]

def facting():
    global fact
    if len(fact) == 0:
        fact = facts[:]
    else:
        random_fact = random.choice(fact)
        fact.remove(random_fact)
        speak.speaker(random_fact)

#функция для jokes
jokes = [
    "Сіз үшін бәріне дайынмын – сүйіктім! Тіпті сізбен қоштасуға да.",
    "Әйелі күйеуіне:неге үйленбей тұрып кедей екеніңді айтпадың?! Күйеуі:айттымғой, барым да нарым да сен деп",
    "— Әуре болмасаңызшы, шығарып салмай-ақ қойыңыз. — О не дегеніңіз! Қонақ шығарып салғанда, мен сондай бір рахаттанып қаламын!",
    "— Ескі пальтомның түймелері үзіліп бітті. Киюге ұят өзі! — Ештеңе жоқ, ертең сатып әперем.— Пальто ма?— Жоқ, түйме әперем.",
    "— Қазір сіз қай газетті ең жақсы деп айтар едіңіз? — Әрине, біздің аудандық газет. Ет жеген кезде қолыңды сүртсең, майын жақсы алады. Басқа аудандық газетпен қол сүртсең, қолыңа қара сиясы жұғады. Қол сүртуге біздің газет таптырмайды ғой, таптырмайды.",
    "Әрбір шеккен темекі өмірімізді екі сағатқа қысқартады, әрбір ішкен арақ өмірімізді үш сағатқа қысқартады, ал әрбір жұмыс күні өмірімізді сегіз сағатқа қысқартады",
    "Бастықтың қабылдауында: — Мен жазды сондай жек көремін. Күн ысып, терлей бересің, шөлдей бересің.... — Қорықпа, еңбек демалысына сені қыста бірақ жібереміз.",
    "Билік:— Біз жақсы өмір сүрдік, әлі сүреміз...Халық:— Ал біз ше?"
]

joke = jokes[:]

def joking():
    global joke
    if len(joke) == 0:
        joke = jokes[:]
    else:
        random_joke = random.choice(joke)
        joke.remove(random_joke)
        speak.speaker(random_joke)


#функция для советов
advices = [
    "Тұрақты физикалық белсенділік: аптасына кемінде 150 минут спортпен немесе физикалық белсенділікпен айналысуға тырысыңыз. Бұған жаяу жүру, жүгіру, жүзу, йога, спортзал сабақтары және тағы да басқалары кіруі мүмкін.",
    "Дұрыс тамақтану: әртүрлі және теңдестірілген тағамдарға, соның ішінде көптеген жемістерге, көкөністерге, ақуыздарға, дәнді дақылдарға Назар аударыңыз және қант, тұз және қаныққан майларды тұтынуды шектеңіз.",
    "Суды жеткілікті мөлшерде ішіңіз: ылғалдандыру үшін күні бойы жеткілікті мөлшерде су ішіңіз.",
    "Алкоголь мен темекіні тұтынуды шектеу: алкогольді азайтыңыз және мүмкіндігінше темекі шегуден аулақ болыңыз.",
    "Ұйқының қалыпты мөлшері: денені қалпына келтіру үшін жеткілікті сапалы ұйқыны (тәулігіне 7-9 сағат) қамтамасыз етіңіз.",
    "Стрессті басқару: стресс деңгейін төмендету үшін медитация, йога немесе терең тыныс алу сияқты релаксация әдістерін үйреніңіз.",
    "Дұрыс поза және эргономика: дұрыс позаны сақтаңыз және арқа мен буын проблемаларын болдырмау үшін эргономикалық жиһазды пайдаланыңыз.",
    "Отырықшы өмір салтын шектеңіз: әр сағат сайын тұрып, қозғалуға тырысыңыз, әсіресе егер сізде отырықшы жұмыс болса.",
    "Позитивті ойлау: эмоционалды әл-ауқатыңызға қамқорлық жасаңыз және өз денеңіз бен денсаулығыңызға оң көзқараспен қарайтындығыңызға көз жеткізіңіз."
]

advice = advices[:]

def advicing():
    global advice
    if len(advice) == 0:
        advice = advices[:]
    else:
        random_advice = random.choice(advice)
        advice.remove(random_advice)
        speak.speaker(random_advice)
#Функция для музыки
def music():
    music_dir = config.settings["music_dir_path"]
    songs = os.listdir(music_dir)   
    random1 = os.startfile(os.path.join(music_dir, random.choice(songs)))

#Функция для открытия браузера
def browser():     
    webbrowser.open('https://www.google.com', new=2)

#Функция для открытие кино сайта
def kino():
    webbrowser.open('https://kinogo.biz/' , new=2)

#Функция для открытия ютуба
def youtube():
    webbrowser.open('https://www.youtube.com/' , new=2)

#Функция для бесік жыры
def BesikZhyry():
    music2_dir = config.settings["music2_dir_path"]
    songs = os.listdir(music2_dir)   
    random2 = os.startfile(os.path.join(music2_dir, random.choice(songs)))

#функция для получения данных о погоде с API openweathermap 
def weather():
    '''Для работы этого кода нужно зарегистрироваться на сайте
    https://openweathermap.org или переделать на ваше усмотрение под что-то другое'''
    try:
        params = {'q': config.settings["city"], 'units': 'metric',
                  'lang': 'en', 'appid': config.settings["weather_api"]}
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        speak.speaker(
            translator.translate_en_to_kz(num2word.replace_numbers_with_words(f"Weather is {w['weather'][0]['description']} {round(w['main']['temp'])} degrees")))
    except:
        speak.speaker(
        "Қате!")

#Функция для подключение игры
def game():
    try:
        subprocess.Popen(config.settings["game_path"])
    except:
        #print('Файл жолы табылмады, оның дұрыстығын тексеріңіз')
        speak.speaker('Файл жолы табылмады, оның дұрыстығын тексеріңіз')
    
#Функция для подключение телеграмма
def telegram():
     os.system(config.settings["telegram_path"])

#Функция для подключение VsCode
def vscode():
     os.system(config.settings["vscode_path"])

#Отключение бота  
def offBot():
	'''Отключает бота'''
	sys.exit()

#Функция для геолокации
def get_city():
    # Получаем информацию о местоположении по IP-адресу
    location = geocoder.ip('me')

    # Получаем город из информации о местоположении
    city = location.city

    return city

config.settings["city"] = get_city()

def map():
    city = get_city()
    webbrowser.open(f"https://www.google.com/maps/place/{city}")
    
#Функция для шахмата
def chess():
    webbrowser.open('https://www.chess.com/ru' , new=2) 

#Функция для кодфорса
def codeforces():
    webbrowser.open('https://codeforces.com/' , new=2) 

#Функция для новостей
def news():
    webbrowser.open('https://www.nur.kz/' , new=2) 

#Функция для википедии
def wiki(query):
    query = translator.translate_kz_to_en(query)
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences = 2)
    speak.speaker(translator.translate_en_to_kz(num2word.replace_numbers_with_words(results)))
    with open("temp\wiki.txt", "w", encoding="utf-8") as file:
        # Записываем текст на казахском языке в файл
        file.write(translator.translate_en_to_kz(results))
    os.system(f'"notepad.exe" {"wiki.txt"}')
#функция для определения времени
def irlTime():
    now = datetime.datetime.now()
    answer = "Қазір " + str(now.hour) + ":" + str(now.minute)
    speak.speaker(translator.translate_en_to_kz(num2word.replace_numbers_with_words(answer)))

def passive():
	'''Функция заглушка при простом диалоге с ботом'''
	pass

#функция для бейонда
def beyond():
    webbrowser.open('https://ask.bc-pf.org/' , new=2)
#функция для найк стора
def nike():
    webbrowser.open('https://www.nike.com/' , new=2)
#функция для ламоды
def lamoda():
    webbrowser.open('https://www.lamoda.kz/women-home/' , new=2)
#функция для вики
def wiki12():
    webbrowser.open('https://kinogo.biz/' , new=2)
#функция для хранилища
def drive():
    webbrowser.open('https://drive.google.com/drive/my-drive?hl=ru' , new=2)
#функция для линкедин
def linkedin():
    webbrowser.open('https://ru.linkedin.com/', new=2)
#функция для футбольных новостей
def football_news ():
    webbrowser.open('https://www.championat.com/news/football/1.html' , new=2)
#функция для баскетбольных новостей
def basketball_news ():
    webbrowser.open('https://www.championat.com/news/basketball/1.html' , new=2)
#функция для гитхаба
def github():
    webbrowser.open('https://github.com/' , new=2)
#функция для майкрософт
def microsoft():
    webbrowser.open('https://www.microsoft.com/ru-ru/microsoft-365/microsoft-office' , new=2)
#функция для почты
def gmail():
    webbrowser.open('https://mail.google.com/mail/u/0/#inbox' , new=2)
#функция для списка фильмов
def schedule_of_films():
    webbrowser.open('https://www.kinopoisk.ru/lists/movies/top250/?utm_referrer=www.google.com' , new=2)