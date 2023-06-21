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

    if expr == "*":
        return list(range(field_min, field_max + 1))

    for part in expr.split(","):
        if part == "*":
            values = values.union(range(field_min, field_max + 1))
            break

        if "-" in part:
            start, end = map(int, part.split("-"))
            if start < field_min or start > field_max:
                raise ValueError(f"Value out of range for {field.name}: {part}")

            values = values.union(range(start, end + 1))
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
    print_fields(fields, " ".join(cmd))


def print_fields(fields: Dict[CronField, List[int]], cmd: str = "") -> None:
    for field, values in fields.items():
        print(f"{field.getLabel():14} {' '.join(map(str, values))}")

    print(f"{'command':14} {cmd}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cron_parser.py <cron expression>")
        sys.exit(1)

    parse_cron(sys.argv[1])
