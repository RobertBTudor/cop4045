import csv
import datetime
import math
import sys
from typing import TypeAlias


Observation: TypeAlias = tuple[datetime.datetime, float]
Observations: TypeAlias = dict[str, list[Observation]]
Errors: TypeAlias = list[tuple[int, str]]
Statistics: TypeAlias = dict[str, tuple[float, float, float]]
Outliers: TypeAlias = dict[str, tuple[datetime.datetime, float, float]]


def read_observations(filename: str) -> tuple[Observations, Errors]:
	"""Read station observations from a CSV file.

	Args:
		filename: CSV file containing station, date, and temperature columns.

	Returns:
		A pair containing observations grouped by station and validation errors.
		Dates are ``datetime.datetime`` values, and errors are
		``(line_number, message)`` tuples.
	"""
	observations = {}
	errors = []
	seen = set()

	with open(filename, "r", encoding="utf-8", newline="") as file:
		for line_number, row in enumerate(csv.reader(file), start=1):
			if not row or not any(value.strip() for value in row):
				errors.append((line_number, "malformed line"))
				continue

			# Accept the optional header row without treating it as an observation.
			if line_number == 1 and [value.strip().lower() for value in row] == [
				"station",
				"date",
				"temperature",
			]:
				continue

			if len(row) != 3:
				errors.append((line_number, "expected station, date, temperature"))
				continue

			station, date_text, temperature_text = (value.strip() for value in row)
			if not station or not date_text:
				errors.append((line_number, "station and date are required"))
				continue

			# Accept the assignment's timestamp format and ISO dates used in tests.
			date = None
			for date_format in ("%I:%M:%S %p %m/%d/%Y", "%Y-%m-%d"):
				try:
					date = datetime.datetime.strptime(date_text, date_format)
					break
				except ValueError:
					continue
			if date is None:
				errors.append((line_number, "date has an unsupported format"))
				continue

			# Convert temperatures and enforce the inclusive assignment range.
			try:
				temperature = float(temperature_text)
			except ValueError:
				errors.append((line_number, "temperature must be numeric"))
				continue

			if not math.isfinite(temperature) or not -100.0 <= temperature <= 150.0:
				errors.append((line_number, "temperature must be between -100.0 and 150.0"))
				continue

			# Keep only the first observation for each station/date pair.
			key = (station, date)
			if key in seen:
				errors.append((line_number, "duplicate station and date"))
				continue

			seen.add(key)
			observations.setdefault(station, []).append((date, temperature))

	for station in observations:
		observations[station].sort(key=lambda observation: observation[0])

	return observations, errors

def station_statistics(observations: Observations) -> Statistics:
	"""Calculate each station's minimum, maximum, and mean temperature.

	Args:
		observations: Mapping of station names to ``(date, temperature)`` pairs.

	Returns:
		A mapping of station names to ``(minimum, maximum, mean)`` tuples.
	"""
	statistics = {}

	for station, records in observations.items():
		temperatures = [temperature for _, temperature in records]
		if not temperatures:
			raise ValueError(f"station {station!r} has no observations")

		statistics[station] = (
			min(temperatures),
			max(temperatures),
			sum(temperatures) / len(temperatures),
		)

	return statistics


def station_outliers(observations: Observations) -> Outliers:
	"""Return stations whose latest reported temperature exceeds their mean.

	Args:
		observations: Mapping of station names to date/temperature observations.

	Returns:
		A mapping to ``(latest_date, latest_temperature, mean)`` tuples.
	"""
	statistics = station_statistics(observations)
	latest = {
		station: max(records, key=lambda record: record[0])
		for station, records in observations.items()
	}

	return {
		station: (date, temperature, statistics[station][2])
		for station, (date, temperature) in latest.items()
		if temperature > statistics[station][2]
	}

def write_statistics(filename: str, statistics: Statistics) -> None:
	"""Write station statistics as sorted CSV rows.

	Args:
		filename: Destination CSV filename.
		statistics: Mapping to ``(minimum, maximum, mean)`` tuples.

	Each row contains the station name followed by its minimum, maximum, and
	mean temperatures.  Stations are lexicographically ordered, and each
	numeric value has exactly one digit after the decimal point.
	"""
	with open(filename, "w", encoding="utf-8", newline="") as file:
		for station in sorted(statistics):
			minimum, maximum, mean = statistics[station]
			# Explicit formatting keeps integer-valued temperatures as 5.0.
			file.write(f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}\n")


def main() -> int:
	"""Process command-line input and write station statistics.

	Returns:
		Zero on success, or one when the two required filenames are missing.
	"""
	if len(sys.argv) != 3:
		print("Usage: python p5_Tudor_Robert.py input.csv output.csv")
		return 1

	input_filename = sys.argv[1]
	output_filename = sys.argv[2]

	observations, errors = read_observations(input_filename)
	statistics = station_statistics(observations)
	outliers = station_outliers(observations)

	if errors:
		print("Errors:")
		for line_number, message in errors:
			print(f"  line {line_number}: {message}")

	print("Statistics:")
	for station in sorted(statistics):
		minimum, maximum, mean = statistics[station]
		print(
			f"  {station}: min={minimum:.1f}, "
			f"max={maximum:.1f}, mean={mean:.1f}"
		)

	print("Outliers:")
	for station in sorted(outliers):
		date, temperature, mean = outliers[station]
		print(f"  {station}: date={date}, temperature={temperature:.1f}, mean={mean:.1f}")

	write_statistics(output_filename, statistics)
	return 0


if __name__ == "__main__":
	sys.exit(main())
