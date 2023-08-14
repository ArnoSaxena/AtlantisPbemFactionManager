from data.region import Region


def test_initialise_region():
    test_x_coord = 5
    test_y_coord = 42
    test_z_coord = 23
    test_region = 'foobar'

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)

    assert sud.coords == (test_x_coord, test_y_coord, test_z_coord)
    assert sud.region_type == test_region
    assert sud.reports == {}


def test_region_get_key():
    test_x_coord = 5
    test_y_coord = 42
    test_z_coord = 23
    test_region = 'foobar'
    test_key = f'{test_x_coord}_{test_y_coord}_{test_z_coord}'

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)

    actual = sud.get_key()

    assert actual == test_key


def test_region_get_key_from_coordinates():
    test_x_coord = 5
    test_y_coord = 42
    test_z_coord = 23
    test_key = f'{test_x_coord}_{test_y_coord}_{test_z_coord}'

    actual = Region.get_key_from_coordinates(test_x_coord, test_y_coord, test_z_coord)

    assert actual == test_key


def test_add_report():
    test_data = {
        'faction':
            {
                'number': 42
            },
        'date':
            {
                'month': 'April',
                'year': 7
            }
    }
    test_report_key = '42_4_7'

    test_x_coord = 5
    test_y_coord = 42
    test_z_coord = 23
    test_region = 'foobar'

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    sud.add_report(test_data)

    assert len(sud.reports) == 1
    assert test_report_key in sud.reports.keys()
    assert sud.reports[test_report_key] == test_data


def test_merge_reports_different_report_data():
    test_data_01 = {
        'faction': {'number': 42},
        'date': {
                'month': 'April',
                'year': 7
        }
    }
    test_report_key_01 = '42_4_7'

    test_data_02 = {
        'faction': {'number': 42},
        'date': {
            'month': 'February',
            'year': 7
        }
    }
    test_report_key_02 = '42_2_7'

    test_x_coord = 5
    test_y_coord = 42
    test_z_coord = 23
    test_region = 'foobar'

    test_region = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    test_region.add_report(test_data_01)

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    sud.add_report(test_data_02)

    sud.merge_reports(test_region)

    assert len(sud.reports) == 2
    assert test_report_key_01 in sud.reports.keys()
    assert test_report_key_02 in sud.reports.keys()
    assert sud.reports[test_report_key_01] == test_data_01
    assert sud.reports[test_report_key_02] == test_data_02


def test_merge_reports_same_report_data():
    test_data = {
        'faction': {'number': 42},
        'date': {
                'month': 'April',
                'year': 7
        }
    }
    test_report_key = f'42_4_7'

    test_x_coord = 5
    test_y_coord = 42
    test_z_coord = 23
    test_region = 'foobar'

    test_region = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    test_region.add_report(test_data)

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    sud.add_report(test_data)

    sud.merge_reports(test_region)

    assert len(sud.reports) == 1
    assert test_report_key in sud.reports.keys()
    assert sud.reports[test_report_key] == test_data

