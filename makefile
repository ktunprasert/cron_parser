.PHONY: build run test

# Build the Docker image
build:
	docker-compose build

# Run the tests in the Docker container
test:
	docker-compose run cron python -m pytest

# Run the Python script in the Docker container
run:
	docker-compose run cron python cron_parser.py "$(filter-out $@,$(MAKECMDGOALS))"

