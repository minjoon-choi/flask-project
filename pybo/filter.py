# -*- coding: utf-8 -*-
def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    import locale
    locale.setlocale(locale.LC_TIME, 'ko_KR.UTF-8')
    return value.strftime(fmt)