Lightweight a movie and TV series data parser like title, alternate title, release date, runtime and episode titles for TV series from imdb.com and kinopoisk.ru without using third-party packages.

Install:

    pip install imkin

Example 1:

    import imkin
    
    film = imkin.new('https://www.imdb.com/title/tt0068646/')
    
    print(film.title)
    
    print(film.alternate)
    
    print(film.year)
    
    print(film.time)
    
    print(film)

Example 2:

    import imkin
    
    series = imkin.new('https://www.imdb.com/title/tt2356777/')
    
    print(len(series.titles))
    
    print(series.titles['1.1'])
