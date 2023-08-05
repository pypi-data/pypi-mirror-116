from abc import ABC, abstractmethod

import numberize.dawgs as dawgs


class Linguist(ABC):
    @staticmethod
    @abstractmethod
    def get_number(token: str):
        """
        E.g. 'two' -> 2, 'twenty-five' -> 25, "п'ять" -> 5, "миллион" -> 1E6
        'horse' -> None
        :param token: simple numeral
        :return: corresponding number, returns None if token is not a numeral
        """


class EnLinguist(Linguist):
    @staticmethod
    def get_number(token: str):
        if '-' in token:
            parts = token.split('-')
            if len(parts) != 2:
                return
            left = dawgs.en_nums.get(parts[0])
            if not left or left < 20 or left > 90:
                return
            right = dawgs.en_nums.get(parts[1])
            if not right or right > 9 or right < 1:
                return
            return left + right
        return dawgs.en_nums.get(token)


class RuLinguist(Linguist):
    def __init__(self, morph):
        self.analyzer = morph

    def get_number(self, token: str):
        if token[-1] == '.' and len(token) > 3:
            token = token[:-1]
        for form in self.analyzer.normal_forms(token):
            number = dawgs.ru_nums.get(form)
            if number:
                return number


class UkLinguist(Linguist):
    def __init__(self, morph):
        self.analyzer = morph

    def get_number(self, token: str):
        if token[-1] == '.' and len(token) > 3:  # TokTokTokenizer sometimes
            token = token[:-1]              # doesn't tokenize points "тисяча."
        for form in self.analyzer.normal_forms(token):
            number = dawgs.uk_nums.get(form)
            if number:
                return number
