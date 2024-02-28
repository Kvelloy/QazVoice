import re
from num2words import num2words

def replace_numbers_with_words(text):
    def replace(match):
        num = int(match.group(0))
        res =  num2words(num, lang='en')
        return res.replace('-' , ' ')

    # Ищем все числа в строке и заменяем их на числительные
    result = re.sub(r'\d+', replace, text)

    return result

