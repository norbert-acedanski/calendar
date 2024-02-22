import argparse

_parser = argparse.ArgumentParser()
_parser.add_argument("--year", action="store",
                     help="Provide year, for which the calendar should be created")
YEAR = int(_parser.parse_args().year)
NUMBER_OF_COLUMNS_IN_TABLE = 8
TABLE_DISTANCE = 1
START_CELL = "B4"
BASE_PROPERTIES = {"text_h_align": 2, "text_v_align": 2}
NUMBER_OF_MONTHS_IN_A_ROW = 3
NUMBER_OF_MONTHS_IN_A_COLUMN = 4
if NUMBER_OF_MONTHS_IN_A_ROW*NUMBER_OF_MONTHS_IN_A_COLUMN != 12:
    raise ValueError(f"A product of {NUMBER_OF_MONTHS_IN_A_COLUMN=} and {NUMBER_OF_MONTHS_IN_A_ROW=} should give 12!")
