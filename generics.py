import datetime
import json
from typing import Any, Dict, Generator, List

from config import YEAR


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
            start_day = datetime.datetime(year=YEAR, month=start_day["month"], day=start_day["day"])
            end_day = datetime.datetime(year=YEAR, month=end_day["month"], day=end_day["day"])
            if start_day > end_day:
                raise ValueError(f"Starting day ({start_day}) of vacation should be before the end date ({end_day})")
            delta = end_day - start_day
            from holidays import NationalDaysOff
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