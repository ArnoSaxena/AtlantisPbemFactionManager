from month import Month


def test_get_enum_from_string():
    test_month = 'August'
    actual = Month[test_month]

    assert actual == Month.August


def test_get_report_time():
    test_report_lines = [
        "",
        " ",
        ";Treasury:",
        ";",
        "",
        ";Item                                      Rank  Max        Total",
        ";=====================================================================",
        ";37 leaders [LEAD]                         21    189        2189",
        ";89 wood elves [WELF]                      13    796        5643",
        "",
        " ",
        "Atlantis Report For:",
        "Nekojin Empire (4) (Martial 2, Magic 3)",
        "January, Year 3"
        "",
        "Atlantis Engine Version: 5.2.4 (beta)",
        "NewOrigins, Version: 3.0.0 (beta)",
        "",
        "Faction Status:",
        "Regions: 14 (25)"
    ]

    actual_month, actual_year = Month.get_report_time(test_report_lines)

    assert actual_month == Month.January
    assert actual_year == 3


def test_get_time_key():
    assert Month.get_time_key(Month.January, 1) == "1_1"
    assert Month.get_time_key(Month.February, 3) == "2_3"
    assert Month.get_time_key(Month.March, 7) == "3_7"
    assert Month.get_time_key(Month.April, 11) == "4_11"
    assert Month.get_time_key(Month.May, 17) == "5_17"
    assert Month.get_time_key(Month.June, 21) == "6_21"
    assert Month.get_time_key(Month.July, 8) == "7_8"
    assert Month.get_time_key(Month.August, 5) == "8_5"
    assert Month.get_time_key(Month.September, 6) == "9_6"
    assert Month.get_time_key(Month.October, 2) == "10_2"
    assert Month.get_time_key(Month.November, 9) == "11_9"
    assert Month.get_time_key(Month.December, 12) == "12_12"


def test_left_time_key_larger_left():
    assert Month.left_time_key_younger("3_12", "10_9") is True
    assert Month.left_time_key_younger("12_10", "3_10") is True
    assert Month.left_time_key_younger("12_12", "3_15") is not True
    assert Month.left_time_key_younger("6_8", "7_8") is not True
    assert Month.left_time_key_younger("6_8", "6_8") is not True
    assert Month.left_time_key_younger("6_8", None) is True
    assert Month.left_time_key_younger(None, "6_8") is not True
    assert Month.left_time_key_younger(None, None) is not True


def test_get_month_and_year():
    actual_month, actual_year = Month.get_month_and_year("3_12")

    assert actual_month == Month.March
    assert actual_year == 12
