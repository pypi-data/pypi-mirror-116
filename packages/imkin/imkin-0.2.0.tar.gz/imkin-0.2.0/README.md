Lightweight a movie and TV series data parser like title, alternate title, release date, runtime, age rating and episode titles for TV series from imdb.com and kinopoisk.ru without using third-party packages.

Install:

    pip install imkin

Examples:

    import imkin
    
    film = imkin.new('https://www.imdb.com/title/tt0068646/')
    
    print(film.title)
    
    print(film.alternate)
    
    print(film.year)
    
    print(film.time)
    
    print(film.age)
    
    print(film)
    
    
    series = imkin.new('https://www.imdb.com/title/tt2356777/')
    
    print(series.title)
    
    print(len(series.titles))
    
    print(series.titles['1.1'])
    
    
    result = imkin.search('Fargo')
    
    print(result)
