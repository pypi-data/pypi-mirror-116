import random
from normalize import normalize
from typing import TypedDict, Optional, Callable, Union


class Options(TypedDict):
    maxLength: Optional[int]
    min: Optional[int]
    max: Optional[int]
    exactly: Optional[int]
    namesPerString: Optional[int]
    separator: Optional[str]
    join: Optional[str]
    formatter: Optional[Callable[[str], str]]


def random_int(less_than: int):
    return random.randint(0, less_than)


class RandomMovieNames:
    options: Options = {
        'min': 1,
        'max': 1,
        'maxLength': 1,
        'namesPerString': 1,
        'formatter': lambda name: name,
        'separator': ' '
    }

    def __init__(self, options: Optional[Union[Options, int]] = None):
        self.total = 0
        self.relativeIndex = 0
        self.token = ""
        self.results: list = []

        if not options:
            self.movie_name()

        if isinstance(options, int):
            self.options['exactly'] = options
            self.options['min'] = options
            self.options['max'] = options

        if 'exactly' in options:
            self.options['min'] = options['exactly']
            self.options['max'] = options['exactly']

        if 'namesPerString' in options and isinstance(options['namesPerString'], int):
            self.options['namesPerString'] = options['namesPerString']

        if 'formatter' in options and isinstance(options['formatter'], Callable):
            self.options['formatter'] = options['formatter']

        if 'separator' in options and isinstance(options['separator'], str):
            self.options['separator'] = options['separator']

        if 'join' in options and isinstance(options['join'], str):
            self.options['join'] = options['join']

    def generate(self):
        self.total = self.options['min'] + random_int(self.options['max'] + 1 - self.options['min'])

        for i in range(self.total * self.options['namesPerString']):
            if self.relativeIndex == self.options['namesPerString'] - 1:
                self.token += self.options['formatter'](self.movie_name())
            else:
                self.token += self.options['formatter'](self.movie_name()) + self.options['separator']

            self.relativeIndex += 1

            if (i + 1) % self.options['namesPerString'] == 0:
                self.results.append(self.token)
                self.token = ''
                self.relativeIndex = 0

        if 'join' in self.options:
            self.results = self.options['join'].join(self.results)

        return self.results

    def movie_name(self):
        if self.options and self.options['maxLength'] > 1:
            return normalize(self.generate_movie_name_with_max_length())
        else:
            return normalize(RandomMovieNames.generate_random_movieName())

    def generate_movie_name_with_max_length(self):
        right_size = False
        name_used = ''
        while not right_size:
            name_used = RandomMovieNames.generate_random_movieName()
            if len(name_used) <= self.options['maxLength']:
                right_size = True
        return name_used

    @staticmethod
    def generate_random_movieName():
        with open('movie-names.txt', 'r') as rf:
            movie_names_list = rf.read().split()
            return movie_names_list[random_int(len(movie_names_list))]


random_movie_names = RandomMovieNames()
print(random_movie_names.generate())
"""
['TheRiver']
"""

random_movie_names = RandomMovieNames(5)
print(random_movie_names.generate())
"""
['Coronavirus', 'NiagaraNiagara', 'Joker', 'Changeling', 'Diadelosmuertos', 'CombatWombat']
"""
random_movie_names = RandomMovieNames({'min': 5, 'max': 10})
print(random_movie_names.generate())
"""
['HustleFlow', 'FullLove', 'Lolita', 'Inframundo', 'ASimplePlan']
"""

random_movie_names = RandomMovieNames({'exactly': 2})
print(random_movie_names.generate())
"""
['ThisIsEngland', 'RidingGiants']
"""

random_movie_names = RandomMovieNames({'exactly': 5, 'join': ' '})
print(random_movie_names.generate())
"""
TheMaoYears TheConjuring ShortTerm OutofReach TakeMetoTarzana GodGrewTiredofUs
"""

random_movie_names = RandomMovieNames({'exactly': 5, 'maxLength': 4})
print(random_movie_names.generate())
"""
['Conspiracy', 'OutoftheAshes', 'WhatAboutME', 'MissAmericana', 'Bridegroom', 'Benched']
"""

random_movie_names = RandomMovieNames({'exactly': 3, 'namesPerString': 2})
print(random_movie_names.generate())
"""
['TheBiggestFan DirtyHarry', 'BlueRidge LaSoufriere', 'Stardust TheWheel', 'ChapterVerse TheCreativeBrain']
"""

random_movie_names = RandomMovieNames({'exactly': 3, 'namesPerString': 2, 'separator': '-'})
print(random_movie_names.generate())
"""
['BatmanHush-TyingtheKnot', 'Murder-WomaninMotion', 'Misfits-TheElevenOClock']
"""

random_movie_names = RandomMovieNames({'exactly': 2, 'namesPerString': 2, 'formatter': lambda name: name.upper()})
print(random_movie_names.generate())
"""
['ACHRISTMASCAROL AWARMWIND', 'MARSHALL RADIATOR']
"""

random_movie_names = RandomMovieNames({'exactly': 2, 'namesPerString': 2, 'formatter': lambda name: name.capitalize()})
print(random_movie_names.generate())
"""
['Dosparaelcamino Pentagram', 'Scuzz Theragewithin']
"""
