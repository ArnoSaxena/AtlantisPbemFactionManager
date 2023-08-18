from repositoryRegion import RepositoryRegion
from data.region import Region


def test_repositoryRegion_initialise():
    sud = RepositoryRegion()
    assert isinstance(sud.regions, dict)
    assert len(sud.regions) == 0


def test_repositoryRegion_add_regions():
    test_region_01 = Region(5, 6, 7, 'foobar')
    test_region_key_01 = test_region_01.get_key()
    test_region_02 = Region(8, 9, 10, 'barfoo')
    test_region_key_02 = test_region_02.get_key()

    sud = RepositoryRegion()
    actual_01 = sud.add_region(test_region_01)
    actual_02 = sud.add_region(test_region_02)

    assert actual_01
    assert actual_02
    assert len(sud.regions) == 2
    assert test_region_key_01 in sud.regions.keys()
    assert sud.regions[test_region_key_01] == test_region_01
    assert test_region_key_02 in sud.regions.keys()
    assert sud.regions[test_region_key_02] == test_region_02


def test_repositoryRegion_add_existing_region():
    test_region_01 = Region(5, 6, 7, 'foobar')
    test_region_key_01 = test_region_01.get_key()
    test_region_02 = Region(5, 6, 7, 'foobar')

    sud = RepositoryRegion()
    actual_01 = sud.add_region(test_region_01)
    actual_02 = sud.add_region(test_region_02)

    assert actual_01
    assert not actual_02
    assert len(sud.regions) == 1
    assert test_region_key_01 in sud.regions.keys()
    assert sud.regions[test_region_key_01] == test_region_01


def test_repositoryRegion_get_existing_region():
    test_coord_x_01 = 5
    test_coord_y_01 = 6
    test_coord_z_01 = 7
    test_coord_x_02 = 8
    test_coord_y_02 = 9
    test_coord_z_02 = 10

    test_region_01 = Region(test_coord_x_01, test_coord_y_01, test_coord_z_01, 'foobar')
    test_region_02 = Region(test_coord_x_02, test_coord_y_02, test_coord_z_02, 'barfoo')

    sud = RepositoryRegion()
    sud.add_region(test_region_01)
    sud.add_region(test_region_02)

    actual_01 = sud.get_region(test_coord_x_01, test_coord_y_01, test_coord_z_01)
    actual_02 = sud.get_region(test_coord_x_02, test_coord_y_02, test_coord_z_02)

    assert isinstance(actual_01, Region)
    assert actual_01 == test_region_01
    assert isinstance(actual_02, Region)
    assert actual_02 == test_region_02


def test_repositoryRegion_get_not_existing_region():
    test_region_01 = Region(5, 6, 7, 'foobar')
    test_region_02 = Region(8, 9, 10, 'barfoo')

    sud = RepositoryRegion()
    sud.add_region(test_region_01)
    sud.add_region(test_region_02)

    actual = sud.get_region(11, 12, 13)

    assert actual is None


def test_repositoryRegion_get_by_key_existing_region():
    test_coord_x_01 = 5
    test_coord_y_01 = 6
    test_coord_z_01 = 7
    test_region_key_01 = f'{test_coord_x_01}_{test_coord_y_01}_{test_coord_z_01}'

    test_coord_x_02 = 8
    test_coord_y_02 = 9
    test_coord_z_02 = 10
    test_region_key_02 = f'{test_coord_x_02}_{test_coord_y_02}_{test_coord_z_02}'

    test_region_01 = Region(test_coord_x_01, test_coord_y_01, test_coord_z_01, 'foobar')
    test_region_02 = Region(test_coord_x_02, test_coord_y_02, test_coord_z_02, 'barfoo')

    sud = RepositoryRegion()
    sud.add_region(test_region_01)
    sud.add_region(test_region_02)

    actual_01 = sud.get_region_by_key(test_region_key_01)
    actual_02 = sud.get_region_by_key(test_region_key_02)

    assert isinstance(actual_01, Region)
    assert actual_01 == test_region_01
    assert isinstance(actual_02, Region)
    assert actual_02 == test_region_02


def test_repositoryRegion_get_by_key_not_existing_region():
    test_region_01 = Region(5, 6, 7, 'foobar')
    test_region_02 = Region(8, 9, 10, 'barfoo')

    test_region_key = "11_12_13"

    sud = RepositoryRegion()
    sud.add_region(test_region_01)
    sud.add_region(test_region_02)

    actual = sud.get_region_by_key(test_region_key)

    assert actual is None


def test_repositoryRegion_load_regions_from_report_data():
    test_region_report_01 = {
                'location': [5, 4, 3],
                'terrain': 'foobar'
            }
    test_region_report_02 = {
                'location': [7, 8],
                'terrain': 'barfoo'
            }
    test_data = {
        'faction': {'number': 42},
        'date': {
            'month': 'April',
            'year': 7
        },
        'regions': [
            test_region_report_01,
            test_region_report_02
        ]
    }
    test_regions_key_01 = '5_4_3'
    test_regions_key_02 = '7_8_1'

    sud = RepositoryRegion()
    sud.load_regions_from_report_data(test_data)

    assert len(sud.regions) == 2
    assert test_regions_key_01 in sud.regions.keys()
    assert test_regions_key_02 in sud.regions.keys()
    actual_region_01 = sud.regions[test_regions_key_01]
    actual_region_02 = sud.regions[test_regions_key_02]
    assert isinstance(actual_region_01, Region)
    assert isinstance(actual_region_02, Region)
    assert actual_region_01.coords == (5, 4, 3)
    assert actual_region_01.region_type == 'foobar'
    assert actual_region_02.coords == (7, 8, 1)
    assert actual_region_02.region_type == 'barfoo'
    assert len(actual_region_01.reports) == 1
    assert len(actual_region_02.reports) == 1
    test_faction_time_key = '42_4_7'
    assert test_faction_time_key in actual_region_01.reports.keys()
    assert test_faction_time_key in actual_region_02.reports.keys()
    assert actual_region_01.reports[test_faction_time_key] == test_region_report_01
    assert actual_region_02.reports[test_faction_time_key] == test_region_report_02
