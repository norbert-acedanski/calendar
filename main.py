import calendar
import copy
import datetime
import os
import string

import xlsxwriter

from config import BASE_PROPERTIES, NUMBER_OF_COLUMNS_IN_TABLE, NUMBER_OF_MONTHS_IN_A_COLUMN, \
    NUMBER_OF_MONTHS_IN_A_ROW, START_CELL, TABLE_DISTANCE, YEAR

from holidays import Holidays, NationalDaysOff

MONTHS = [month.upper() for month in calendar.month_name[1:]]
MONTH_COLORS = {0: "#50BDE8", 1: "#2F8CC7", 2: "#4DB1B1", 3: "#81C383", 4: "#FAB64B", 5: "#F28568",
                6: "#EC6091", 7: "#BF3B77", 8: "#A15875", 9: "#90529B", 10: "#7968AC", 11: "#6981BF"}
EXCEL_COLUMNS = list(string.ascii_uppercase) + [f"{first_letter}{second_letter}"
                                                for first_letter in string.ascii_uppercase
                                                for second_letter in string.ascii_uppercase]

if __name__ == "__main__":
    if not os.path.isdir("output_files"):
        os.mkdir("output_files")
    workbook = xlsxwriter.Workbook(f"output_files/calendar_{YEAR}.xlsx")
    base_format = workbook.add_format(BASE_PROPERTIES)
    worksheet = workbook.add_worksheet(name="Calendar")
    start_cell_column, start_cell_row_index = list(START_CELL)
    start_cell_column_index = EXCEL_COLUMNS.index(start_cell_column)
    months_table_data = {index: {} for index in range(12)}
    # Add title to the calendar
    worksheet.merge_range(f"{start_cell_column}{int(start_cell_row_index) - 2}:"
                          f"{EXCEL_COLUMNS[start_cell_column_index + 7]}{int(start_cell_row_index) - 2}",
                          f"Calendar {YEAR}",
                          workbook.add_format(dict(**BASE_PROPERTIES,
                                                   **{"bg_color": "yellow", "bold": True, "font_size": 20})))
    # Store number of rows for each month
    for month_index in range(12):
        number_of_rows = 5
        if month_index in [0, 2, 4, 6, 7, 9, 11]:
            if datetime.datetime(year=YEAR, month=month_index + 1, day=1).weekday() > 4:
                number_of_rows = 6
        elif month_index in [3, 5, 8, 10]:
            if datetime.datetime(year=YEAR, month=month_index + 1, day=1).weekday() > 5:
                number_of_rows = 6
        else:
            if datetime.datetime(year=YEAR, month=month_index + 1, day=1).weekday() == 0 and not calendar.isleap(YEAR):
                number_of_rows = 4
        months_table_data[month_index]["number_of_rows"] = number_of_rows
    # Prepare months titles and weekdays for each month
    row_length = 0
    for row in range(NUMBER_OF_MONTHS_IN_A_COLUMN):
        for col in range(NUMBER_OF_MONTHS_IN_A_ROW):
            start_cell_column = f"{EXCEL_COLUMNS[start_cell_column_index + 
                                                 (NUMBER_OF_COLUMNS_IN_TABLE + TABLE_DISTANCE)*col]}"
            start_cell_row = int(start_cell_row_index) + row_length + row*(TABLE_DISTANCE + 2)
            end_cell_column = f"{EXCEL_COLUMNS[start_cell_column_index + NUMBER_OF_COLUMNS_IN_TABLE*(col + 1) - 1 + 
                                               TABLE_DISTANCE*col]}"
            end_cell_row = int(start_cell_row_index) + row_length + row*(TABLE_DISTANCE + 2)
            months_table_data[col + row*NUMBER_OF_MONTHS_IN_A_ROW].update(
                {"start": {"column": start_cell_column, "row": int(start_cell_row)},
                 "end": {"column": end_cell_column, "row": int(end_cell_row)}})
            worksheet.merge_range(f"{start_cell_column}{start_cell_row}:{end_cell_column}{end_cell_row}",
                                  MONTHS[col + row*NUMBER_OF_MONTHS_IN_A_ROW],
                                  workbook.add_format(dict(**BASE_PROPERTIES,
                                                           **{"bg_color":
                                                              MONTH_COLORS[col + row*NUMBER_OF_MONTHS_IN_A_ROW]})))
            for week_index, week_day in enumerate(["T", *calendar.day_name]):
                worksheet.write(f"{EXCEL_COLUMNS[EXCEL_COLUMNS.index(start_cell_column) + 
                                                 week_index]}{start_cell_row + 1}", week_day[:3],
                                workbook.add_format(dict(**BASE_PROPERTIES,
                                                         **{"bg_color": MONTH_COLORS[col +
                                                                                     row*NUMBER_OF_MONTHS_IN_A_ROW]})))
        row_length += max(month_columns["number_of_rows"]
                          for month_columns in list(months_table_data.values())
                          [row*NUMBER_OF_MONTHS_IN_A_ROW:row*NUMBER_OF_MONTHS_IN_A_ROW + NUMBER_OF_MONTHS_IN_A_ROW])
    # Border cells for each month
    border_format_dict = dict(**BASE_PROPERTIES, **{"top": 1, "bottom": 1, "left": 1, "right": 1})
    border_format = workbook.add_format(border_format_dict)
    for month_index, month in months_table_data.items():
        for column_name in EXCEL_COLUMNS[EXCEL_COLUMNS.index(month["start"]["column"]):
                                         EXCEL_COLUMNS.index(month["end"]["column"]) + 1]:
            for row_index in range(month["start"]["row"] + 2, month["end"]["row"] + 2 + month["number_of_rows"]):
                worksheet.write(f"{column_name}{row_index}", "", border_format)
    # Change size of rows and columns:
    start_cell_column, start_cell_row_index = list(START_CELL)
    columns = EXCEL_COLUMNS.index(start_cell_column)
    columns_to_hide = list(range(1, columns))
    EMPTY_COLUMN_WIDTH, EMPTY_ROW_HEIGHT, FILLED_COLUMN_WIDTH = 2.14, 7.5, 4.43
    worksheet.set_column(0, 0, width=EMPTY_COLUMN_WIDTH)
    if columns_to_hide:
        worksheet.set_column(columns_to_hide[0], columns_to_hide[-1], width=0)
    worksheet.set_row(0, height=EMPTY_ROW_HEIGHT)
    for month_data in list(months_table_data.values())[:NUMBER_OF_MONTHS_IN_A_ROW]:
        start_column_index = EXCEL_COLUMNS.index(month_data["start"]["column"])
        end_column_index = EXCEL_COLUMNS.index(month_data["end"]["column"])
        worksheet.set_column(start_column_index, end_column_index, width=FILLED_COLUMN_WIDTH)
        worksheet.set_column(end_column_index + 1, end_column_index + 1, width=EMPTY_COLUMN_WIDTH)
        if TABLE_DISTANCE > 1:
            worksheet.set_column(end_column_index + 2, end_column_index + 1 + TABLE_DISTANCE, width=0.0)
    if TABLE_DISTANCE > 1:
        for row, month_data in zip(range(NUMBER_OF_MONTHS_IN_A_COLUMN),
                                   list(months_table_data.values())[::NUMBER_OF_MONTHS_IN_A_COLUMN]):
            row_length = max(month_columns["number_of_rows"] for month_columns in list(months_table_data.values())
                             [row * NUMBER_OF_MONTHS_IN_A_ROW:
                              row * NUMBER_OF_MONTHS_IN_A_ROW + NUMBER_OF_MONTHS_IN_A_ROW])
            for row_to_hide in range(1, TABLE_DISTANCE + 1):
                worksheet.set_row(month_data["start"]["row"] + row_length + 1 + row_to_hide, height=0)
    # Write each day of the month
    days = datetime.datetime(year=YEAR, month=1, day=1).weekday()
    week_number_format = workbook.add_format(dict(**border_format_dict, **{"font_size": 9, "italic": True}))
    for month_index, month in months_table_data.items():
        start_cell_column_index = EXCEL_COLUMNS.index(month["start"]["column"])
        start_cell_row = month["start"]["row"] + 2
        end_cell_column_index = EXCEL_COLUMNS.index(month["end"]["column"])
        end_cell_row = month["end"]["row"] + 2 + month["number_of_rows"]
        month_days = 0
        start_day = datetime.datetime(year=YEAR, month=month_index + 1, day=1).weekday()
        for cell_row in range(start_cell_row, end_cell_row):
            week_index = days // 7 + 1
            worksheet.write(f"{EXCEL_COLUMNS[start_cell_column_index]}{cell_row}", week_index, week_number_format)
            for cell_column in EXCEL_COLUMNS[start_cell_column_index + 1: end_cell_column_index + 1]:
                if cell_row == start_cell_row and \
                        EXCEL_COLUMNS.index(cell_column) - start_cell_column_index - 1 < start_day:
                    continue
                days += 1
                month_days += 1
                try:  # If the day number is bigger, than the number of days in this month, we skip remaining cells
                    current_day = datetime.datetime(year=YEAR, month=month_index + 1, day=month_days)
                except ValueError:
                    days -= 1
                    month_days -= 1
                    break
                day_format = copy.deepcopy(border_format_dict)
                for holiday_class in Holidays.get_in_order():
                    if holiday_class == Holidays.NationalHolidays:
                        continue
                    if current_day in holiday_class.days_off:
                        day_format = dict(**day_format, **{"bg_color": holiday_class.color})
                for national_holidays in Holidays.NationalHolidays.days_off:
                    if current_day == national_holidays:
                        if "bg_color" not in day_format:
                            day_format = dict(**day_format, **{"bg_color": Holidays.NationalHolidays.color})
                        else:
                            day_format["bg_color"] = Holidays.NationalHolidays.color
                worksheet.write(f"{cell_column}{cell_row}", month_days, workbook.add_format(day_format))
    # Write legend next to first 3 months to the right
    start_cell_column, start_cell_row_index = list(START_CELL)
    index = int(start_cell_row_index)
    column = EXCEL_COLUMNS[EXCEL_COLUMNS.index(start_cell_column) +
                           (NUMBER_OF_COLUMNS_IN_TABLE + TABLE_DISTANCE)*NUMBER_OF_MONTHS_IN_A_ROW]
    legend_column_width = 1.06*max(len(f"{holiday_class.name} [{len(holiday_class.days_off)} "
                                       f"DAY{"" if len(holiday_class.days_off) == 1 else "S"}]")
                                   for holiday_class in Holidays.get_in_order())
    worksheet.set_column(f"{column}:{column}", legend_column_width)
    for holiday_class in Holidays.get_in_order():
        if not holiday_class.days_off:
            continue
        day_format = dict(**copy.deepcopy(border_format_dict), **{"bg_color": holiday_class.color})
        worksheet.write(f"{column}{index}", f"{holiday_class.name} [{len(holiday_class.days_off)} "
                                            f"DAY{"" if len(holiday_class.days_off) == 1 else "S"}]",
                        workbook.add_format(day_format))
        index += 1
    index += 1
    names_of_national_holidays = [key for key, value in NationalDaysOff.__dict__.items()
                                  if isinstance(value, datetime.datetime)]
    day_format = dict(**copy.deepcopy(border_format_dict), **{"bg_color": Holidays.NationalHolidays.color})
    for name, date in zip(names_of_national_holidays, Holidays.NationalHolidays.days_off):
        text = " ".join(name.split("_")).title() + f" ({date.strftime("%d %B")})"
        worksheet.write(f"{column}{index}", text, workbook.add_format(day_format))
        if len(text) > legend_column_width:
            legend_column_width = text
            worksheet.set_column(f"{column}:{column}", legend_column_width)
        index += 1
    workbook.close()
