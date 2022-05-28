def time(s):
    try:
        day, month, year, hour, minutes, seconds = s.split('-')

        if int(year) > 2022 or int(year) < 2010 or int(month) > 12 or int(month) < 1 or int(day) > 31 or\
                int(day) < 1 or int(hour) > 23 or int(hour) < 0 or int(minutes) > 59 or int(minutes) < 0 or\
                int(seconds) > 59 or int(seconds) < 0:
            return False
    except:
        return False
    return True
