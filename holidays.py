import datetime
import json
import requests
import warnings
from typing import Any, Dict, Generator, List

from config import YEAR


class NationalDaysOff:
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


class GenericDefaults:
    @classmethod
    def get_in_order(cls) -> Generator[Any, None, None]:
        yield from (val for key, val in cls.__dict__.items() if not key.startswith("__"))


class BaseClass:
    @staticmethod
    def create_days_off(days_off: List[Dict[str, Dict[str, int]]],
                        include_weekends: bool = False) -> List[datetime.datetime]:
        dates = []
        for days_off_range in days_off:
            start_day = days_off_range.get("start", days_off_range.get("single_day"))
            end_day = days_off_range.get("end", days_off_range.get("single_day"))
            delta = datetime.datetime(year=YEAR, month=end_day["month"], day=end_day["day"]) - \
                                     (start_day := datetime.datetime(year=YEAR, month=start_day["month"],
                                                                     day=start_day["day"]))
            dates += [start_day + datetime.timedelta(i) for i in range(delta.days + 1)
                      if (not (start_day + datetime.timedelta(i)).weekday() in [5, 6] or include_weekends)
                      and not start_day + datetime.timedelta(i) in NationalDaysOff.NATIONAL_DAYS_OFF]
        return dates

    @staticmethod
    def load_json_data(file_name: str, holiday_category: str) -> List[Dict[str, Dict[str, int]]]:
        try:
            with open(file=file_name, mode="r") as json_file:
                content = json.load(json_file)
        except FileNotFoundError:
            content = {}
        return content.get(holiday_category, [])


class Holidays(GenericDefaults):
    class NationalHolidays:
        name = "NATIONAL HOLIDAYS"
        days_off = NationalDaysOff.NATIONAL_DAYS_OFF
        color = "#D50A20"

    class NationalHolidaysOnSaturdayReplacementDays:
        name = "NATIONAL HOLIDAYS ON SATURDAY REPLACEMENT DAYS"
        days_off = BaseClass.load_json_data(file_name=f"input_files/calendar_{YEAR}.json", holiday_category=name)
        days_off = BaseClass.create_days_off(days_off=days_off)  # [datetime.datetime(year=YEAR, month=3, day=29)]
        color = "#00A2E8"

    class PlasmaDonationHolidays:
        name = "PLASMA DONATION"
        days_off = BaseClass.load_json_data(file_name=f"input_files/calendar_{YEAR}.json", holiday_category=name)
        days_off = BaseClass.create_days_off(days_off=days_off)
        color = "#A349A4"

    class BloodDonationHolidays:
        name = "BLOOD DONATION"
        days_off = BaseClass.load_json_data(file_name=f"input_files/calendar_{YEAR}.json", holiday_category=name)
        days_off = BaseClass.create_days_off(days_off=days_off)
        color = "#22B14C"

    class Holidays:
        name = "HOLIDAYS"
        days_off = BaseClass.load_json_data(file_name=f"input_files/calendar_{YEAR}.json", holiday_category=name)
        days_off = BaseClass.create_days_off(days_off=days_off)
        color = "#FF7F27"

    class SpecialOccasions:
        name = "SPECIAL OCCASIONS HOLIDAYS"
        days_off = BaseClass.load_json_data(file_name=f"input_files/calendar_{YEAR}.json", holiday_category=name)
        days_off = BaseClass.create_days_off(days_off=days_off)
        color = "#FFAECC"

    class Childcare:
        name = "CHILDCARE"
        days_off = BaseClass.load_json_data(file_name=f"input_files/calendar_{YEAR}.json", holiday_category=name)
        days_off = BaseClass.create_days_off(days_off=days_off)
        color = "#3F48CC"


if len((saturday_holidays := [national_holiday for national_holiday in Holidays.NationalHolidays.days_off
                              if national_holiday.weekday() == 5])) \
        != len(Holidays.NationalHolidaysOnSaturdayReplacementDays.days_off):
    warnings.warn(f"Please input all days, that are a replacement for the Holidays,that are on saturday! "
                  f"{saturday_holidays}")
