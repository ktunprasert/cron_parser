import pytest
from cron_parser import CronField, parse_field, parse_cron


def test_getLabel():
    assert CronField.MINUTE.getLabel() == "minute"
    assert CronField.HOUR.getLabel() == "hour"
    assert CronField.DAY.getLabel() == "day of month"
    assert CronField.MONTH.getLabel() == "month"
    assert CronField.WEEKDAY.getLabel() == "day of week"


def test_parse_field():
    assert parse_field("*", CronField.MINUTE) == list(range(0, 60))
    assert parse_field("*/15", CronField.MINUTE) == list(range(0, 60, 15))
    assert parse_field("1-5", CronField.DAY) == [1, 2, 3, 4, 5]
    assert parse_field("10", CronField.HOUR) == [10]
    with pytest.raises(ValueError):
        parse_field("61", CronField.MINUTE)
        parse_field("24", CronField.HOUR)
        parse_field("32", CronField.DAY)
        parse_field("13", CronField.MONTH)
        parse_field("10", CronField.WEEKDAY)

    assert parse_field("1-5,6-9", CronField.DAY) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert parse_field("1-5,*/15", CronField.DAY) == [1, 2, 3, 4, 5, 16, 31]
    assert parse_field("1-5,2-3", CronField.DAY) == [1, 2, 3, 4, 5]


def test_parse_cron(capsys):
    with pytest.raises(ValueError):
        parse_cron("* * *")
    with pytest.raises(ValueError):
        parse_cron("* * * * *")
    with pytest.raises(ValueError):
        parse_cron("61 * * * * some_command")

    parse_cron("*/15 0 1,15 * 1-5 /usr/bin/find stuff")
    captured = capsys.readouterr()
    assert captured.out == (
        f"{'minute':14} 0 15 30 45\n"
        + f"{'hour':14} 0\n"
        + f"{'day of month':14} 1 15\n"
        + f"{'month':14} 1 2 3 4 5 6 7 8 9 10 11 12\n"
        + f"{'day of week':14} 1 2 3 4 5\n"
        + f"{'command':14} /usr/bin/find stuff\n"
    )
