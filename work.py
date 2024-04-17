from config import YEAR
from generics import GenericDefaults, BaseClass


class Work(GenericDefaults):

    class Delegations:
        name = "DELEGATIONS"
        days_off = BaseClass.load_json_data(file_name=f"input_files/calendar_{YEAR}.json", holiday_category=name)
        days_off = BaseClass.create_days_off(days_off=days_off)
        color = "#7092BE"

    class Trainings:
        name = "TRAININGS"
        days_off = BaseClass.load_json_data(file_name=f"input_files/calendar_{YEAR}.json", holiday_category=name)
        days_off = BaseClass.create_days_off(days_off=days_off)
        color = "#5AE100"

    class OtherWorkRelatedDays:
        name = "OTHER WORK RELATED DAYS"
        days_off = BaseClass.load_json_data(file_name=f"input_files/calendar_{YEAR}.json", holiday_category=name)
        days_off = BaseClass.create_days_off(days_off=days_off)
        color = "#FFF200"
