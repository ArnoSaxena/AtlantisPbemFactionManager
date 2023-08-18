from month import Month


class StaticHelper:
    DATA_TOKEN_REPORTS = 'reports'
    DATA_TOKEN_PLAYER_NUMBER = 'player_number'
    DATA_TOKEN_PLAYER_FACTION_NAME = 'player_faction_name'
    REPORT_FACTION_TOKEN = 'faction'
    REPORT_REGIONS_TOKEN = 'regions'
    REPORT_REGION_TERRAIN_TOKEN = 'terrain'
    REPORT_REGION_LOCATION_TOKEN = 'location'
    REPORT_REGION_EXITS_TOKEN = 'exits'
    REPORT_REGION_EXIT_TERRAIN_TOKEN = 'terrain'
    REPORT_REGION_EXIT_COORDS_TOKEN = 'location'

    @staticmethod
    def get_max_col(provinces):
        max_col = 0
        for province_datas in provinces.values():
            keys = list(province_datas.keys())
            province_data = province_datas[keys[0]]
            coords = province_data['location']
            if int(coords[0]) > max_col:
                max_col = int(coords[0])
            if StaticHelper.REPORT_REGION_EXITS_TOKEN in province_data.keys():
                for province_exit_key in province_data[StaticHelper.REPORT_REGION_EXITS_TOKEN].keys():
                    seen_coords = province_data[StaticHelper.REPORT_REGION_EXITS_TOKEN][province_exit_key]['location']
                    if int(seen_coords[0]) > max_col:
                        max_col = int(seen_coords[0])
        return max_col

    @staticmethod
    def get_max_row(provinces):
        max_row = 0
        for province_datas in provinces.values():
            keys = list(province_datas.keys())
            province_data = province_datas[keys[0]]
            coords = province_data['location']
            if int(coords[1]) > max_row:
                max_row = int(coords[0])
            if StaticHelper.REPORT_REGION_EXITS_TOKEN in province_data.keys():
                for province_exit_key in province_data[StaticHelper.REPORT_REGION_EXITS_TOKEN].keys():
                    seen_coords = province_data[StaticHelper.REPORT_REGION_EXITS_TOKEN][province_exit_key]['location']
                    if int(seen_coords[1]) > max_row:
                        max_row = int(seen_coords[0])
        return max_row

    @staticmethod
    def get_time_key_from_report_data(report_data):
        report_month_name = report_data['date']['month']
        report_month_enum = Month[report_month_name.strip()]
        report_year = int(report_data['date']['year'])
        time_key = Month.get_time_key(report_month_enum, report_year)
        return time_key
