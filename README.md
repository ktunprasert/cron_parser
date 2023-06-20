# Cron Expression Parser

This project is a command line utility written in Python that parses CRON expressions and prints the schedule details in a human-friendly format.

## Prerequisites

- Python 3.10+
- Docker
- Docker Compose
- Make

## Getting Started

Then build the Docker image with:

```bash
make build
```

You can then run the utility with a cron expression as follows:

```bash
make run "* * * * * /usr/bin/find"
```

This will parse the cron expression and print the schedule.

To run the unit tests, use:

```bash
make test
```

## Example

Here's an example of the output when you run the utility with the cron expression `*/15 0 1,15 * 1-5 /usr/bin/find`:

```
minute       0 15 30 45
hour         0
day of month 1 15
month        1 2 3 4 5 6 7 8 9 10 11 12
day of week  1 2 3 4 5
command      /usr/bin/find
```

This indicates that the command `/usr/bin/find` will be executed every 15 minutes, at hour 0, on the 1st and 15th day of the month, every month, from Monday to Friday.
