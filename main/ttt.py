import translator
import num2word


symbol_dict = {
    '-' : 'minus',
    '+' : 'plus',
    '*' : 'multiply',
    '/' : 'divide',
    '=' : 'equal',
    '%' : 'percent',
    '@' : 'at',
    '#' : 'hash',
    '$' : 'dollar',
    '€' : 'euro',
    '£' : 'pound sterling',
    '¥' : 'yen',
    '₽' : 'ruble',
    '^' : 'power of',
    '<' : 'less than',
    '>' : 'greater than',
    '|' : 'vertical bar',
    '\\' : 'backslash',
    '~' : 'tilde',
    '_' : 'underscore',
    'π' : 'pi',
    'α' : 'alpha',
    'β' : 'beta',
    'γ' : 'gamma',
    'δ' : 'delta',
    'ε' : 'epsilon',
    'ζ' : 'zeta',
    'η' : 'eta',
    'θ' : 'theta',
    'ι' : 'iota',
    'κ' : 'kappa',
    'λ' : 'lambda',
    'μ' : 'mu',
    'ν' : 'nu',
    'ξ' : 'xi',
    'ο' : 'omicron',
    'π' : 'pi',
    'ρ' : 'rho',
    'σ' : 'sigma',
    'τ' : 'tau',
    'υ' : 'upsilon',
    'φ' : 'phi',
    'χ' : 'chi',
    'ψ' : 'psi',
    'ω' : 'omega'
}


def replace_symbols(text, symbol_dict):
    text = num2word.replace_numbers_with_words(text)
    replaced_text = ""
    for char in text:
        if char in symbol_dict:
            replaced_text += " " + symbol_dict[char] + " "
        else:
            replaced_text += char
    return replaced_text


import openai

import time

openai.api_key = "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"

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "assistant", "content": "You are a useful assistant who answers accurately with proper grammar. Don't write hyphens"}, 
                {"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

    model=model,

    messages=messages,

    temperature=0.3,

    )

    return response.choices[0].message["content"]


def chat_gpt(text):
    text = translator.translate_kz_to_en(text)

    text = get_completion(text)

    text = replace_symbols(text, symbol_dict)

    text = translator.translate_en_to_kz(text)

    return text

