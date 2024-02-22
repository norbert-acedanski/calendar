import argparse

_parser = argparse.ArgumentParser()
_parser.add_argument("--year", action="store",
                     help="Provide year, for which the calendar should be created")
YEAR = int(_parser.parse_args().year)
NUMBER_OF_COLUMNS_IN_TABLE = 8
TABLE_DISTANCE = 1
START_CELL = "B4"
BASE_PROPERTIES = {"text_h_align": 2, "text_v_align": 2}
