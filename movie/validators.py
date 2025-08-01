import re

from rest_framework import serializers


def toshmat_validator(obj):
    if 'toshmat' in obj:
        raise serializers.ValidationError("Toshmat bo'lishi mumkin emas!")
    return obj


def not_characters(obj):
    pattern = "^[a-zA-Z0-9_.-]+$"
    if not re.match(pattern, obj):
        raise serializers.ValidationError(
            'Faqat lotin harflari (a-z, A-Z), raqamlar (0-9), pastki chiziq (_), nuqta (.) va chiziqcha (-) ishlatilishi mumkin. Bo‘sh joy yoki boshqa belgilar kiritish taqiqlangan.')
    return obj