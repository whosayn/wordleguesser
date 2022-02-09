from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'frontend/index.html')

class DB:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(DB, cls).__new__(cls)
        return cls.instance


    def __init__(self, filename):
        self.filename = filename


    def get_words(self):
        with open(self.filename, 'r') as fh:
            words = json.loads(fh.read())
        return words

def _process_absent_letters(words, absent_letters):
    if not absent_letters:
        return words

    result = words
    for letter in absent_letters:
        current_words = []
        for word in result:
            if letter not in word:
                current_words.append(word)
        result = current_words
    return result

def _process_wrong_position_letters(words, wrong_position_letters):
    if not wrong_position_letters:
        return words

    result = words
    for i in range(0, len(wrong_position_letters), 2):
        current_words = []
        letter = wrong_position_letters[i]
        index = int(wrong_position_letters[i+1]) - 1
        for word in result:
            if word[index] != letter:
                current_words.append(word)
        result = current_words

    return result

def _process_correct_position_letters(words, correct_position_letters):
    if not correct_position_letters:
        return words

    result = words
    for i in range(0, len(correct_position_letters), 2):
        current_words = []
        letter = correct_position_letters[i]
        index = int(correct_position_letters[i+1]) - 1
        for word in result:
            if word[index] == letter:
                current_words.append(word)
        result = current_words

    return result


def _process_letter_counts(words, correct_position_letters, wrong_position_letters):
    result = words
    freq_dict = {}

    for char in correct_position_letters + wrong_position_letters:
        if char.isalpha():
            freq_dict[char] = freq_dict.get(char, 0) + 1

    for char, count in freq_dict.items():
        current_words = []
        for word in result:
            if word.count(char) == count:
                current_words.append(word)
        result = current_words

    return result


def process_guess_params(params):
    db = DB('words_dictionary.json')
    words = db.get_words()
    words = [word.upper() for word in words if len(word) == params['length']]
    words = _process_absent_letters(words, params['excludedLetters'])
    words = _process_correct_position_letters(words, params['correctPosLetters'])
    words = _process_wrong_position_letters(words, params['wrongPosLetters'])
    words = _process_letter_counts(words, params['correctPosLetters'], params['wrongPosLetters'])
    return words[:100]

@csrf_exempt
def get_guesses(request):
    if request.method != 'POST':
        return

    body_unicode = request.body.decode('utf-8')
    guess_params = json.loads(body_unicode)
    words = process_guess_params(guess_params)

    return JsonResponse({ 'words': words} )
