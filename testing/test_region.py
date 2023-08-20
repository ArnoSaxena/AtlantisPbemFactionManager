from data.region import Region


def test_initialise_region():
    test_x_coord = 5
    test_y_coord = 42
    test_z_coord = 23
    test_region = 'foobar'

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)

    assert sud.coords == (test_x_coord, test_y_coord, test_z_coord)
    assert sud.region_type == test_region
    assert isinstance(sud.reports, dict)
    assert len(sud.reports) == 0


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


def test_add_region_report():
    test_faction_number = 42
    test_time_key = '2_1'
    test_region_report = {
                'location': [5, 4, 3],
                'terrain': 'foobar',
                'foo': 'bar'
        }

    region_report_key = f'{test_faction_number}_{test_time_key}'

    sud = Region(5, 4, 3, 'foobar')
    sud.add_region_report(test_faction_number, test_time_key, test_region_report)

    assert len(sud.reports) == 1
    assert region_report_key in sud.reports.keys()
    assert sud.reports[region_report_key] == test_region_report


def test_merge_different_date_report_data():
    test_faction_number = 42
    test_x_coord = 5
    test_y_coord = 4
    test_z_coord = 1
    test_region = 'foobar'
    test_region_report_01 = {
        'location': [test_x_coord, test_y_coord],
        'terrain': test_region,
        'foo': 'bar'
    }
    test_region_report_02 = {
        'location': [test_x_coord, test_y_coord],
        'terrain': test_region,
        'bar': 'foo'
    }

    test_time_01 = '4_7'
    test_time_02 = '2_7'

    test_region = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    test_region.add_region_report(test_faction_number, test_time_01, test_region_report_01)

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    sud.add_region_report(test_faction_number, test_time_02, test_region_report_02)

    sud.merge(test_region)

    report_dict_key_01 = f'{test_faction_number}_{test_time_01}'
    report_dict_key_02 = f'{test_faction_number}_{test_time_02}'

    assert len(sud.reports) == 2
    assert report_dict_key_01 in sud.reports.keys()
    assert report_dict_key_02 in sud.reports.keys()
    assert sud.reports[report_dict_key_01] == test_region_report_01
    assert sud.reports[report_dict_key_02] == test_region_report_02


def test_merge_same_report_data():
    test_faction_number = 42
    test_x_coord = 5
    test_y_coord = 4
    test_z_coord = 1
    test_region = 'foobar'
    test_region_report_01 = {
        'location': [test_x_coord, test_y_coord],
        'terrain': test_region,
        'foo': 'bar'
    }
    test_region_report_02 = {
        'location': [test_x_coord, test_y_coord],
        'terrain': test_region,
        'bar': 'foo'
    }

    test_time_key = '4_7'
    report_dict_key = f'{test_faction_number}_{test_time_key}'

    test_region = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    test_region.add_region_report(test_faction_number, test_time_key, test_region_report_02)

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    sud.add_region_report(test_faction_number, test_time_key, test_region_report_01)

    sud.merge(test_region)

    assert len(sud.reports) == 1
    assert report_dict_key in sud.reports.keys()
    assert sud.reports[report_dict_key] == test_region_report_01


def test_get_latest_report_no_given_faction():
    test_faction_number = 42
    test_x_coord = 5
    test_y_coord = 4
    test_z_coord = 1
    test_region = 'foobar'
    test_region_report_01 = {
        'location': [test_x_coord, test_y_coord],
        'terrain': test_region,
        'foo': 'bar'
    }
    test_region_report_02 = {
        'location': [test_x_coord, test_y_coord],
        'terrain': test_region,
        'bar': 'foo'
    }

    test_time_01 = '4_7'
    test_time_02 = '2_7'

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    sud.add_region_report(test_faction_number, test_time_01, test_region_report_01)
    sud.add_region_report(test_faction_number, test_time_02, test_region_report_02)

    actual = sud.get_latest_report()

    assert 'foo' in actual.keys()
    assert actual['foo'] == 'bar'


def test_get_latest_report_different_faction():
    test_faction_number = 42
    test_x_coord = 5
    test_y_coord = 4
    test_z_coord = 1
    test_region = 'foobar'
    test_region_report_01 = {
        'location': [test_x_coord, test_y_coord],
        'terrain': test_region,
        'foo': 'bar'
    }
    test_region_report_02 = {
        'location': [test_x_coord, test_y_coord],
        'terrain': test_region,
        'bar': 'foo'
    }

    test_time_01 = '4_7'
    test_time_02 = '2_7'

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)
    sud.add_region_report(test_faction_number, test_time_01, test_region_report_01)
    sud.add_region_report(test_faction_number, test_time_02, test_region_report_02)

    actual = sud.get_latest_report(23)

    assert actual is None


def test_get_latest_report_no_reports():
    test_x_coord = 5
    test_y_coord = 4
    test_z_coord = 1
    test_region = 'foobar'

    sud = Region(test_x_coord, test_y_coord, test_z_coord, test_region)

    actual = sud.get_latest_report()

    assert actual is None

