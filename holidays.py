import datetime
import requests

from config import YEAR

NEW_YEAR = datetime.datetime(year=YEAR, month=1, day=1)
EPIPHANY = datetime.datetime(year=YEAR, month=1, day=6)
easter_in_selected_year = requests.get(f"https://www.calendardate.com/easter_{YEAR}.htm",
                                       verify=False).text.split(f"Easter {YEAR} is on")[1].split(", ")[1]
EASTER_DAY = datetime.datetime.strptime(f"{YEAR} {easter_in_selected_year}", '%Y %B %d')
EASTER_MONDAY = EASTER_DAY + datetime.timedelta(days=1)
LABOUR_DAY = datetime.datetime(year=YEAR, month=5, day=1)
CONSTITUTION_DAY = datetime.datetime(year=YEAR, month=5, day=3)
PENTECOST = EASTER_DAY + datetime.timedelta(weeks=7)
CORPUS_CHRISTI_DAY = EASTER_DAY + datetime.timedelta(days=60)
ASSUMPTION_OF_THE_BLESSED_VIRGIN_MARY_DAY = datetime.datetime(year=YEAR, month=8, day=15)
ALL_SAINTS_DAY = datetime.datetime(year=YEAR, month=11, day=1)
INDEPENDENCE_DAY = datetime.datetime(year=YEAR, month=11, day=11)
CHRISTMAS_DAY_1 = datetime.datetime(year=YEAR, month=12, day=25)
CHRISTMAS_DAY_2 = datetime.datetime(year=YEAR, month=12, day=26)
NATIONAL_DAYS_OFF = [NEW_YEAR, EPIPHANY, EASTER_DAY, EASTER_MONDAY, LABOUR_DAY, CONSTITUTION_DAY, PENTECOST,
                     CORPUS_CHRISTI_DAY, ASSUMPTION_OF_THE_BLESSED_VIRGIN_MARY_DAY, ALL_SAINTS_DAY, INDEPENDENCE_DAY,
                     CHRISTMAS_DAY_1, CHRISTMAS_DAY_2]
