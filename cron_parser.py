import enum
from typing import Dict, List
import sys


class CronField(enum.Enum):
    MINUTE = (0, 59)
    HOUR = (0, 23)
    DAY = (1, 31)
    MONTH = (1, 12)
    WEEKDAY = (0, 6)

    def getLabel(self) -> str:
        match (self):
            case self.MINUTE:
                return "minute"
            case self.HOUR:
                return "hour"
            case self.DAY:
                return "day of month"
            case self.MONTH:
                return "month"
            case self.WEEKDAY:
                return "day of week"
            case _:
                return ""


def parse_field(expr: str, field: CronField) -> List[int]:
    field_min, field_max = field.value
    values = set()

    weekday_to_int = {
        "Mon": 0,
        "Tue": 1,
        "Wed": 2,
        "Thu": 3,
        "Fri": 4,
        "Sat": 5,
        "Sun": 6,
    }

    if expr == "*":
        return list(range(field_min, field_max + 1))

    for part in expr.split(","):
        if field == CronField.WEEKDAY and part in weekday_to_int:
            part = str(weekday_to_int[part])

        if part == "*":
            values = values.union(range(field_min, field_max + 1))
            break

        if "-" in part:
            suffix = 1
            if "/" in part:
                part, suffix = part.split("/")

            start, end = part.split("-")

            start = weekday_to_int.get(start, int(start))
            end = weekday_to_int.get(end, int(end))

            if start < field_min or start > field_max:
                raise ValueError(f"Value out of range for {field.name}: {part}")

            if end < start:
                for i in range(start, end + field_max + 2):
                    values.add(i % (field_max + 1))
            else:
                values = values.union(range(start, end + 1, int(suffix)))

        elif "/" in part:
            start, step = part.split("/")
            if start == "*":
                values = values.union(range(field_min, field_max + 1, int(step)))
            else:
                values = values.union(range(int(start), field_max + 1, int(step)))
        else:
            val = int(part)
            if val < field_min or val > field_max:
                raise ValueError(f"Value out of range for {field.name}: {val}")

            values.add(val)

    return sorted(values)


def parse_cron(cron: str) -> None:
    parts = cron.split()
    if len(parts) < 6:
        raise ValueError(f"Invalid CRON expression expected minimum length 6: {parts}")

    fields = {
        field: parse_field(expr, field) for field, expr in zip(CronField, parts[:5])
    }

    cmd = parts[5:]
    cmd_split = []
    for c in cmd:
        for s in c.split("/"):
            if s == "":
                continue
            cmd_split.append(s)
    print_fields(fields, cmd_split)


def print_fields(fields: Dict[CronField, List[int]], cmd: List[str] = []) -> None:
    for field, values in fields.items():
        print(f"{field.getLabel():14} {' '.join(map(str, values))}")

    [first, *cmd] = cmd
    print(f"{'command':14} {first}")
    for c in cmd:
        print(f"{' ':14} {c}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cron_parser.py <cron expression>")
        sys.exit(1)

    parse_cron(sys.argv[1])
