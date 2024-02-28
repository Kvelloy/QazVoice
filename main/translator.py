from deep_translator import GoogleTranslator
import time

def translate_en_to_kz(text):
    return GoogleTranslator(source="en" , target="kk").translate(text)

def translate_kz_to_en(text):
    return GoogleTranslator(source="kk" , target="en").translate(text)
