#!/usr/bin/env python3
from time import sleep
from collections import namedtuple
from urllib.error import URLError
from urllib.parse import urlparse, urljoin, quote
from .parsers import KinopoiskParser, ImdbParser
from .parsers import KinopoiskSeriesParser, ImdbSeriesParser
from .utils import request, parser_run, titles_human


def new(url):
    if urlparse(url).netloc not in ("www.imdb.com", "www.kinopoisk.ru"):
        raise ValueError("only www.imdb.com and www.kinopoisk.ru are allowed")
    if "kinopoisk" in url:
        parser_film = KinopoiskParser
        parser_series = KinopoiskSeriesParser
        if "https" in url:
            url = url.replace("https", "http")
    else:
        parser_film = ImdbParser
        parser_series = ImdbSeriesParser
    try:
        response = request(url)
    except URLError:
        return None
    p = parser_run(parser_film(),
        response.read().decode("utf8", errors="ignore"))
    Film = namedtuple("Film", "title alternate year time")
    f = Film(p.title, p.alternate, p.year, p.time)
    if p.isfilm:
        return f
    Film = namedtuple("Film", Film._fields + ("titles",))
    sleep(1)
    try:
        response = request(urljoin(url, "episodes/"))
    except URLError:
        return f
    ps = parser_run(parser_series(),
        response.read().decode("utf8", errors="ignore"))
    titles = titles_human(ps.seasons)
    s = Film(p.title, p.alternate, p.year, p.time, titles)
    if "imdb" in url:
        u = urljoin(url, "episodes?season=")
        try:
            season_last = int(ps.season)
        except ValueError:
            return s
        for i in range(1, season_last):
            try:
                response = request(u+str(i))
            except URLError:
                continue
            ps = parser_run(parser_series(),
                response.read().decode("utf8", errors="ignore"))
            titles.update(titles_human(ps.seasons))
            sleep(0.5)
        s = Film(p.title, p.alternate, p.year, p.time, titles)
    return s
