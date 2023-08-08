import json
import os
import logging

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from math import sqrt

from month import Month
from provinceHexagon import ProvinceHexagon

# TODO: put constants into config file
DATA_TOKEN_REPORTS = 'reports'
DATA_TOKEN_PLAYER_NUMBER = 'player_number'
DATA_TOKEN_PLAYER_FACTION_NAME = 'player_faction_name'
REPORT_FACTION_TOKEN = 'faction'
REPORT_REGIONS_TOKEN = 'regions'
MAX_MAP_LEVEL = 2
MAP_HEX_SIZE = 25


def get_max_col(provinces):
    max_col = 0
    for province_datas in provinces.values():
        keys = list(province_datas.keys())
        province_data = province_datas[keys[0]]
        coords = province_data['location']
        if int(coords[0]) > max_col:
            max_col = int(coords[0])
    return max_col


def get_max_row(provinces):
    max_row = 0
    for province_datas in provinces.values():
        keys = list(province_datas.keys())
        province_data = province_datas[keys[0]]
        coords = province_data['location']
        if int(coords[1]) > max_row:
            max_row = int(coords[0])
    return max_row


class AtlantisManager:
    def __init__(self):
        self.province_hexagons = None
        self.map_frame = None
        self.win_map_canvas = None
        self.win_region_map_text_box = None
        self.win_province_map_area = None
        self.win_province_list = None
        self.win_province_text_box = None
        self.win_region_list_area = None
        self.win_item_catalogue_list = None
        self.win_item_list_text_box = None
        self.win_item_catalogue_area = None
        self.win_skill_catalogue_list = None
        self.win_skill_list_text_box = None
        self.win_skill_catalogue_area = None

        logging.basicConfig(filename='atlantis_Manager.log',
                            format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%d.%m.%Y:%H:%M:%S',
                            filemode='w',
                            level=logging.DEBUG)

        self.game_data = {
            DATA_TOKEN_PLAYER_NUMBER: -1,
            DATA_TOKEN_PLAYER_FACTION_NAME: "",
            DATA_TOKEN_REPORTS: {}
        }

        self.app_window_root = Tk()
        self.app_window_root.title("Atlantis Manager")
        self.app_window_root.option_add("*tearOff", False)

        main = Frame(self.app_window_root)
        main.pack(fill="both", expand=True, padx=1, pady=(4, 0))

        menubar = Menu(self.app_window_root)
        self.app_window_root.config(menu=menubar)

        file_menu = Menu(menubar)

        menubar.add_cascade(menu=file_menu, label="File")

        file_menu.add_command(label="Save Data", command=self.save_data)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_command(label="Load Reports", command=self.load_reports)

        self.app_notebook = Notebook(main)
        self.app_notebook.pack(fill=BOTH, expand=True)

        # Player Info
        self.player_info_area = Text(self.app_notebook)
        self.player_info_area.insert(END, "Player Info")
        self.player_info_area.pack(fill=BOTH, expand=True)
        self.app_notebook.add(self.player_info_area, text="Player Info")
        self.app_notebook.select(self.player_info_area)

        self.render_skill_catalogue(self.app_notebook)
        self.render_item_catalogue(self.app_notebook)
        self.render_province_catalogue(self.app_notebook)
        self.render_map_tab(self.app_notebook)

        # Object Catalogue
        object_catalogue_area = Text(self.app_notebook)
        object_catalogue_area.insert(END, "Buildings and Ships")
        object_catalogue_area.pack(fill=BOTH, expand=True)
        self.app_notebook.add(object_catalogue_area, text="Buildings and Ships")

        self.app_window_root.bind("<KeyPress>", lambda event: self.check_for_changes())
        self.app_window_root.bind("<Control-o>", lambda event: self.import_data())
        self.app_window_root.bind("<Control-s>", lambda event: self.save_data())

    def app_mainloop(self):
        self.app_window_root.mainloop()

    def get_report_dictionary(self):
        if DATA_TOKEN_REPORTS in self.game_data.keys():
            return self.game_data[DATA_TOKEN_REPORTS]
        else:
            return None

    def add_report(self, report_data):
        faction_number = int(report_data['faction']['number'])
        report_month_name = report_data['date']['month']
        report_month_enum = Month[report_month_name.strip()]
        report_year = int(report_data['date']['year'])
        time_key = Month.get_time_key(report_month_enum, report_year)
        report_dict_key = f'{faction_number}_{time_key}'
        self.game_data[DATA_TOKEN_REPORTS][report_dict_key] = report_data
        return report_dict_key

    def import_data(self):
        data_file_path = filedialog.askopenfilename()
        try:
            with open(data_file_path, "r") as data_file_handle:
                self.game_data = json.loads(data_file_handle.read())

                self.display_player_info()
                self.update_skill_catalogue_list()
                self.update_item_catalogue_list()

        except (AttributeError, FileNotFoundError):
            print("Open operation cancelled")
            return

    # skill list
    def render_skill_catalogue(self, parent_widget):
        self.win_skill_catalogue_area = Frame(parent_widget, relief=RIDGE, borderwidth=10)

        self.win_skill_catalogue_area.columnconfigure(1, weight=1)
        self.win_skill_catalogue_area.rowconfigure(0, weight=1)

        frame_left = Frame(master=self.win_skill_catalogue_area, relief=GROOVE, borderwidth=5)
        frame_right = Frame(master=self.win_skill_catalogue_area, relief=GROOVE, borderwidth=5)

        self.win_skill_list_text_box = Text(master=frame_right, wrap=WORD)

        self.win_skill_catalogue_list = Listbox(frame_left, selectmode=SINGLE)

        self.update_skill_catalogue_list()

        self.win_skill_catalogue_list.bind(
            '<<ListboxSelect>>',
            lambda event: self.on_skill_listbox_select(event))

        skill_list_scrollbar = Scrollbar(frame_left)
        self.win_skill_catalogue_list.config(yscrollcommand=skill_list_scrollbar.set)
        skill_list_scrollbar.config(command=self.win_skill_catalogue_list.yview)

        self.win_skill_catalogue_area.pack(side=TOP, fill=BOTH, expand=True)

        frame_left.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        frame_right.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.win_skill_list_text_box.pack(side=TOP, fill=BOTH, expand=True)
        self.win_skill_catalogue_list.pack(side=LEFT, fill=BOTH, expand=True)
        skill_list_scrollbar.pack(side=RIGHT, fill=Y)

        parent_widget.add(self.win_skill_catalogue_area, text="Skills")

    def update_skill_catalogue_list(self):
        self.win_skill_catalogue_list.delete(0, END)
        skill_list = self.get_all_skills()

        my_keys = list(skill_list.keys())
        my_keys.sort()
        skill_list = {i: skill_list[i] for i in my_keys}

        for skill_name in skill_list.keys():
            self.win_skill_catalogue_list.insert(END, skill_name)

    def on_skill_listbox_select(self, list_select_event):
        skill_list = self.get_all_skills()

        list_select_event_widget = list_select_event.widget
        try:
            selected_index = int(list_select_event_widget.curselection()[0])
            self.win_skill_list_text_box.delete("0.0", END)
            skill_description = skill_list[list_select_event_widget.get(selected_index)]
            self.win_skill_list_text_box.insert(END, skill_description)
        except IndexError:
            return

    def get_all_skills(self):
        all_skill_reports = {}
        report_dict = self.game_data[DATA_TOKEN_REPORTS]
        for value in report_dict.values():
            if 'skillReports' in value.keys():
                skill_reports = value['skillReports']
                for skill_report in skill_reports:
                    skill_name, *skill_description = skill_report.strip().split(':')
                    if skill_name not in all_skill_reports:
                        all_skill_reports[skill_name] = ':'.join(skill_description)
        return all_skill_reports

    # item list
    def render_item_catalogue(self, parent_widget):
        self.win_item_catalogue_area = Frame(parent_widget, relief=RIDGE, borderwidth=10)

        self.win_item_catalogue_area.columnconfigure(1, weight=1)
        self.win_item_catalogue_area.rowconfigure(0, weight=1)

        frame_left = Frame(master=self.win_item_catalogue_area, relief=GROOVE, borderwidth=5)
        frame_right = Frame(master=self.win_item_catalogue_area, relief=GROOVE, borderwidth=5)

        self.win_item_list_text_box = Text(master=frame_right, wrap=WORD)

        self.win_item_catalogue_list = Listbox(frame_left, selectmode=SINGLE)

        self.update_item_catalogue_list()

        self.win_item_catalogue_list.bind(
            '<<ListboxSelect>>',
            lambda event: self.on_item_listbox_select(event))

        item_list_scrollbar = Scrollbar(frame_left)
        self.win_item_catalogue_list.config(yscrollcommand=item_list_scrollbar.set)
        item_list_scrollbar.config(command=self.win_item_catalogue_list.yview)

        self.win_item_catalogue_area.pack(side=TOP, fill=BOTH, expand=True)

        frame_left.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        frame_right.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.win_item_list_text_box.pack(side=TOP, fill=BOTH, expand=True)
        self.win_item_catalogue_list.pack(side=LEFT, fill=BOTH, expand=True)
        item_list_scrollbar.pack(side=RIGHT, fill=Y)

        parent_widget.add(self.win_item_catalogue_area, text="Items")

    def update_item_catalogue_list(self):
        self.win_item_catalogue_list.delete(0, END)
        item_list = self.get_all_items()

        my_keys = list(item_list.keys())
        my_keys.sort()
        item_list = {i: item_list[i] for i in my_keys}

        for item_name in item_list.keys():
            self.win_item_catalogue_list.insert(END, item_name)

    def on_item_listbox_select(self, list_select_event):
        item_list = self.get_all_items()

        list_select_event_widget = list_select_event.widget

        try:
            selected_index = int(list_select_event_widget.curselection()[0])
            self.win_item_list_text_box.delete("0.0", END)
            item_description = item_list[list_select_event_widget.get(selected_index)]
            self.win_item_list_text_box.insert(END, item_description)
        except IndexError:
            return

    def get_all_items(self):
        all_item_reports = {}
        report_dict = self.game_data[DATA_TOKEN_REPORTS]
        for value in report_dict.values():
            if 'itemReports' in value.keys():
                item_reports = value['itemReports']
                for item_report in item_reports:
                    item_name, *item_description = item_report.strip().split(',')
                    item_name, item_id = item_name.strip().split('[')
                    item_id = f'[{item_id}'
                    if item_name not in all_item_reports:
                        item_description = ','.join(item_description)
                        all_item_reports[item_id] = f'{item_name} {item_id}\n{item_description}'
        return all_item_reports

    # province list
    def render_province_catalogue(self, parent_widget):
        self.win_region_list_area = Frame(parent_widget, relief=RIDGE, borderwidth=10)

        self.win_region_list_area.columnconfigure(1, weight=1)
        self.win_region_list_area.rowconfigure(0, weight=1)

        frame_left = Frame(master=self.win_region_list_area, relief=GROOVE, borderwidth=5)
        frame_right = Frame(master=self.win_region_list_area, relief=GROOVE, borderwidth=5)

        self.win_province_text_box = Text(master=frame_right, wrap=WORD)

        self.win_province_list = Listbox(frame_left, selectmode=SINGLE)

        self.update_province_list()

        self.win_province_list.bind(
            '<<ListboxSelect>>',
            lambda event: self.on_province_listbox_select(event))

        province_list_scrollbar = Scrollbar(frame_left)
        self.win_province_list.config(yscrollcommand=province_list_scrollbar.set)
        province_list_scrollbar.config(command=self.win_province_list.yview)

        self.win_region_list_area.pack(side=TOP, fill=BOTH, expand=True)

        frame_left.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        frame_right.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.win_province_text_box.pack(side=TOP, fill=BOTH, expand=True)
        self.win_province_list.pack(side=LEFT, fill=BOTH, expand=True)
        province_list_scrollbar.pack(side=RIGHT, fill=Y)

        parent_widget.add(self.win_region_list_area, text="Regions")

    def update_province_list(self):
        self.win_province_list.delete(0, END)
        province_list = self.get_all_provinces()

        my_keys = list(province_list.keys())
        my_keys.sort()
        province_list = {i: province_list[i] for i in my_keys}

        for province_coords in province_list.keys():
            self.win_province_list.insert(END, province_coords)

    def on_province_listbox_select(self, list_select_event):
        province_list = self.get_all_provinces()

        list_select_event_widget = list_select_event.widget

        try:
            selected_index = int(list_select_event_widget.curselection()[0])
            # get the latest report for player number
            all_descriptions = province_list[list_select_event_widget.get(selected_index)]
            show_description = None
            current_time_key = ""
            current_player_number = ""
            for key in all_descriptions.keys():
                player_number, *time_key_items = key.split('_')
                time_key = '_'.join(time_key_items)
                if show_description is None:
                    show_description = all_descriptions[key]
                    current_time_key = time_key
                    current_player_number = player_number
                    logging.info(f'add report {current_time_key}')
                else:
                    if Month.left_time_key_larger(time_key, current_time_key):
                        show_description = all_descriptions[key]
                        logging.info(f'overwrite report {current_time_key} with {time_key}')
                        current_time_key = time_key
                        current_player_number = player_number
                    elif time_key == current_time_key:
                        if player_number.strip() == str(self.game_data[DATA_TOKEN_PLAYER_NUMBER]):
                            show_description = all_descriptions[key]
                            current_time_key = time_key
                            current_player_number = player_number
                            logging.info(f'overwrite report {current_time_key} for local player report')
                    else:
                        logging.info(f'skip report {time_key}')

            self.win_province_text_box.delete("0.0", END)
            self.win_province_text_box.insert(END,
                                              f'turn {current_time_key} for player number {current_player_number}\n')
            self.win_province_text_box.insert(END, show_description)

        except IndexError:
            return

    def get_all_provinces(self, level=-1):
        all_province_reports = {}
        report_dict = self.game_data[DATA_TOKEN_REPORTS]
        for report_data in report_dict.values():
            if REPORT_REGIONS_TOKEN in report_data.keys():
                province_reports = report_data[REPORT_REGIONS_TOKEN]
                for province_report in province_reports:
                    if 'location' in province_report.keys():
                        coords = province_report['location']
                        if len(coords) == 2:
                            coord_z = 1
                        else:
                            coord_z = coords[2]
                        coord_x = coords[0]
                        coord_y = coords[1]
                    province_coord_name = f'{coord_x}, {coord_y}, {coord_z}'

                    current_faction_number = int(report_data['faction']['number'])
                    report_month_name = report_data['date']['month']
                    report_month_enum = Month[report_month_name.strip()]
                    report_year = int(report_data['date']['year'])
                    current_time_key = Month.get_time_key(report_month_enum, report_year)

                    province_report_key = f'{current_faction_number}_{current_time_key}'

                    if -1 == level or int(coord_z) == level:
                        if province_coord_name not in all_province_reports:
                            all_province_reports[province_coord_name] = {}
                        all_province_reports[province_coord_name][province_report_key] = province_report

        return all_province_reports

    # province map
    def render_map_tab(self, parent_widget):
        self.win_province_map_area = Frame(parent_widget, relief=RIDGE, borderwidth=10)
        self.win_province_map_area.columnconfigure(1, weight=1)
        self.win_province_map_area.rowconfigure(0, weight=1)

        frame_left = Frame(master=self.win_province_map_area, relief=GROOVE, borderwidth=5)
        self.map_frame = Frame(master=self.win_province_map_area, relief=GROOVE, borderwidth=5)

        self.win_region_map_text_box = Text(master=frame_left, wrap=WORD, width=30)

        self.render_map()

        self.win_province_map_area.pack(side=TOP, fill=BOTH, expand=True)

        frame_left.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.map_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.win_region_map_text_box.pack(side=LEFT, fill=BOTH, expand=True)

        parent_widget.add(self.win_province_map_area, text="Map")

    def render_map(self, canvas_width=0, canvas_height=0):
        self.map_frame = Frame(master=self.win_province_map_area, relief=GROOVE, borderwidth=5)
        self.map_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.win_map_canvas = Canvas(master=self.map_frame, width=canvas_width, height=canvas_height)

        map_y_scrollbar = Scrollbar(self.map_frame)
        self.win_map_canvas.config(yscrollcommand=map_y_scrollbar.set)
        map_y_scrollbar.config(command=self.win_map_canvas.yview)

        map_x_scrollbar = Scrollbar(self.map_frame, orient=HORIZONTAL)
        self.win_map_canvas.config(xscrollcommand=map_x_scrollbar.set)
        map_x_scrollbar.config(command=self.win_map_canvas.xview)

        map_x_scrollbar.pack(side=BOTTOM, fill=X)
        map_y_scrollbar.pack(side=RIGHT, fill=Y)
        self.win_map_canvas.pack(side=TOP, fill=BOTH, expand=True)

        # TODO: make canvas clickable with reaction to clicked
        #       on province.

    def update_province_map(self, level):
        provinces = self.get_all_provinces(level)
        max_col = get_max_col(provinces)
        max_row = get_max_row(provinces)
        self.render_map(max_col * 5, max_row * 5)
        self.initialise_map_grid(max_col, max_row, MAP_HEX_SIZE, level)

        # TODO: find province type of each province and get colour from
        #       config file to paint hex.
        for coords in provinces.keys():
            tags = coords.replace(', ', '_')
            self.win_map_canvas.itemconfigure(tags, fill="#53ca53")

        # TODO: find known provinces (waypoints from visited provinces) and mark on map
        #       paint respective hexes with secondary colour (lighter version of province
        #       type colour from config.

    def initialise_map_grid(self, max_column, max_row, hex_side_size, level):
        self.province_hexagons = []

        for column_index in range(max_column + 1):
            if column_index % 2 == 1:
                offset = hex_side_size * sqrt(3) / 2
            else:
                offset = 0

            for row_index in range(max_row + 1):

                if column_index % 2 == 1:
                    translated_row_index = row_index * 2 + 1
                else:
                    translated_row_index = row_index * 2

                # coords = f'{column_index}, {translated_row_index}, {level}'
                tags = f'{column_index}_{translated_row_index}_{level}'
                province_hex = ProvinceHexagon(self.win_map_canvas,
                                               column_index * (hex_side_size * 1.5),
                                               (row_index * (hex_side_size * sqrt(3))) + offset,
                                               hex_side_size,
                                               "white",
                                               tags)

                self.province_hexagons.append(province_hex)

                """
                self.win_map_canvas.create_text(column_index * (hex_size * 1.5) + (hex_size / 2),
                                                (row_index * (hex_size * sqrt(3))) + offset + (hex_size / 2),
                                                text=coords)
                                                """

    def display_player_info(self):
        pass

    def save_data(self):
        file_path = filedialog.asksaveasfilename()
        try:
            json_string = json.dumps(self.game_data, indent=2)

            with open(file_path, 'w') as atlantis_data_file_handle:
                atlantis_data_file_handle.write(json_string)

        except (AttributeError, FileNotFoundError):
            print("Save operation cancelled")
            return

    def load_reports(self):
        logging.info('--- load reports ---')

        report_file_paths = filedialog.askopenfilenames()

        for report_file_path in report_file_paths:
            with open(report_file_path) as report_file_handle:
                report_file_content = report_file_handle.read()
            report_file_content = report_file_content.replace("\"\\", "\"")
            report_data = json.loads(report_file_content)
            time_key = self.add_report(report_data)

            faction_number = int(report_data['faction']['number'])
            report_month_name = report_data['date']['month']
            report_year = int(report_data['date']['year'])

            self.player_info_area.delete("0.0", END)
            self.player_info_area.insert(END, f'Player number {faction_number}\n'
                                              f'Report for {report_month_name} in year {report_year}\n'
                                              f'report data key: {time_key}')

        self.update_skill_catalogue_list()
        self.update_item_catalogue_list()
        self.update_province_list()
        self.update_province_map(level=1)

        # first report sets player number
        # TODO: settings pane to change current player number
        if -1 == self.game_data[DATA_TOKEN_PLAYER_NUMBER]:
            self.game_data[DATA_TOKEN_PLAYER_NUMBER] = faction_number
            self.game_data[DATA_TOKEN_PLAYER_FACTION_NAME] = report_data['faction']['name']
            logging.info(f'Main faction set to '
                         f'{self.game_data[DATA_TOKEN_PLAYER_FACTION_NAME]} '
                         f'({self.game_data[DATA_TOKEN_PLAYER_NUMBER]})')

        logging.info('--- report loaded ---')

    def check_for_changes(self):
        pass


if __name__ == '__main__':
    atlantis_manager_app = AtlantisManager()
    atlantis_manager_app.app_mainloop()
