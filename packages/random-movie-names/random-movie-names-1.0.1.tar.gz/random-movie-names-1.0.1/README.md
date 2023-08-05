# random-movie-names

This is a python package, for generating random movie names

`random_movie_names = RandomMovieNames()`
`print(random_movie_names.generate())`

**['TheRiver']**


`random_movie_names = RandomMovieNames(5)`
`print(random_movie_names.generate())`

**['Coronavirus', 'NiagaraNiagara', 'Joker', 'Changeling', 'Diadelosmuertos', 'CombatWombat']**

`random_movie_names = RandomMovieNames({'min': 5, 'max': 10})`
`print(random_movie_names.generate())`

**['HustleFlow', 'FullLove', 'Lolita', 'Inframundo', 'ASimplePlan']**


`random_movie_names = RandomMovieNames({'exactly': 2})`
`print(random_movie_names.generate())`

**['ThisIsEngland', 'RidingGiants']**


`random_movie_names = RandomMovieNames({'exactly': 5, 'join': ' '})`
`print(random_movie_names.generate())`

**TheMaoYears TheConjuring ShortTerm OutofReach TakeMetoTarzana GodGrewTiredofUs**


`random_movie_names = RandomMovieNames({'exactly': 5, 'maxLength': 4})`
`print(random_movie_names.generate())`

**['Conspiracy', 'OutoftheAshes', 'WhatAboutME', 'MissAmericana', 'Bridegroom', 'Benched']**


`random_movie_names = RandomMovieNames({'exactly': 3, 'namesPerString': 2})`
`print(random_movie_names.generate())`

**['TheBiggestFan DirtyHarry', 'BlueRidge LaSoufriere', 'Stardust TheWheel', 'ChapterVerse TheCreativeBrain']**


`random_movie_names = RandomMovieNames({'exactly': 3, 'namesPerString': 2, 'separator': '-'})`
`print(random_movie_names.generate())`

**['BatmanHush-TyingtheKnot', 'Murder-WomaninMotion', 'Misfits-TheElevenOClock']**


`random_movie_names = RandomMovieNames({'exactly': 2, 'namesPerString': 2, 'formatter': lambda name: name.upper()})`
`print(random_movie_names.generate())`

**['ACHRISTMASCAROL AWARMWIND', 'MARSHALL RADIATOR']**


`random_movie_names = RandomMovieNames({'exactly': 2, 'namesPerString': 2, 'formatter': lambda name: name.capitalize()})`
`print(random_movie_names.generate())`

**['Dosparaelcamino Pentagram', 'Scuzz Theragewithin']**
