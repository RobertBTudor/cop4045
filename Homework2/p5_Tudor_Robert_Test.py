import os
import tempfile
import unittest
import datetime

try:
    from .p5_Tudor_Robert import (
        read_observations,
        station_statistics,
        write_statistics,
    )
except ImportError:
    from p5_Tudor_Robert import (
        read_observations,
        station_statistics,
        write_statistics,
    )


class TestWeatherObservations(unittest.TestCase):
    """Test observation parsing, calculations, and output writing."""

    def make_csv(self, contents: str) -> str:
        """Create a temporary CSV file and remove it after the test."""
        file = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", delete=False
        )
        file.write(contents)
        file.close()
        self.addCleanup(lambda: os.unlink(file.name))
        return file.name

    def test_reads_several_stations(self) -> None:
        """Read and group observations from multiple stations."""
        filename = self.make_csv(
            "station,date,temperature\n"
            "Beta,2024-01-02,12\n"
            "Alpha,2024-01-01,8\n"
            "Beta,2024-01-01,10\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(
            observations,
            {
                "Alpha": [(datetime.datetime(2024, 1, 1), 8.0)],
                "Beta": [
                    (datetime.datetime(2024, 1, 1), 10.0),
                    (datetime.datetime(2024, 1, 2), 12.0),
                ],
            },
        )
        self.assertEqual(errors, [])

    def test_accepts_negative_temperatures(self) -> None:
        """Accept temperatures below zero within the valid range."""
        filename = self.make_csv(
            "North,2024-01-01,-12.5\n"
            "North,2024-01-02,-3\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(
            observations["North"],
            [
                (datetime.datetime(2024, 1, 1), -12.5),
                (datetime.datetime(2024, 1, 2), -3.0),
            ],
        )
        self.assertEqual(errors, [])

    def test_rejects_duplicate_station_date(self) -> None:
        """Reject a second observation for the same station and date."""
        filename = self.make_csv(
            "Alpha,2024-01-01,10\n"
            "Alpha,2024-01-01,12\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(
            observations, {"Alpha": [(datetime.datetime(2024, 1, 1), 10.0)]}
        )
        self.assertEqual(errors, [(2, "duplicate station and date")])

    def test_rejects_invalid_temperature_values(self) -> None:
        """Reject nonnumeric, nonfinite, and out-of-range temperatures."""
        filename = self.make_csv(
            "Alpha,2024-01-01,not-a-number\n"
            "Beta,2024-01-01,nan\n"
            "Gamma,2024-01-01,inf\n"
            "Delta,2024-01-01,-inf\n"
            "Epsilon,2024-01-01,-100.1\n"
            "Zeta,2024-01-01,150.1\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(observations, {})
        self.assertEqual(
            errors,
            [
                (1, "temperature must be numeric"),
                (2, "temperature must be between -100.0 and 150.0"),
                (3, "temperature must be between -100.0 and 150.0"),
                (4, "temperature must be between -100.0 and 150.0"),
                (5, "temperature must be between -100.0 and 150.0"),
                (6, "temperature must be between -100.0 and 150.0"),
            ],
        )

    def test_accepts_boundary_temperatures(self) -> None:
        """Accept exactly -100.0 and 150.0 degrees."""
        filename = self.make_csv(
            "Alpha,09:00:00 AM 04/20/2026,-100.0\n"
            "Beta,09:00:00 AM 04/20/2026,150.0\n"
        )

        observations, errors = read_observations(filename)

        expected_date = datetime.datetime(2026, 4, 20, 9, 0)
        self.assertEqual(observations["Alpha"][0][0], expected_date)
        self.assertEqual(observations["Beta"][0][0], expected_date)
        self.assertEqual(errors, [])

    def test_calculates_station_statistics(self) -> None:
        """Calculate minimum, maximum, and mean temperatures."""
        observations = {
            "Alpha": [
                ("2024-01-01", -2.0),
                ("2024-01-02", 4.0),
                ("2024-01-03", 1.0),
            ],
            "Beta": [("2024-01-01", 7.5)],
        }

        self.assertEqual(
            station_statistics(observations),
            {"Alpha": (-2.0, 4.0, 1.0), "Beta": (7.5, 7.5, 7.5)},
        )

    def test_writes_sorted_stations_and_one_decimal_values(self) -> None:
        """Write stations in order with one decimal place per value."""
        filename = self.make_csv("")

        write_statistics(
            filename,
            {
                "Zoo": (2, 10, 6),
                "Alpha": (-1.25, 3, 0),
                "Beta": (4.44, 4.46, 4.45),
            },
        )

        with open(filename, "r", encoding="utf-8", newline="") as file:
            output = file.read()

        self.assertEqual(
            output,
            "Alpha,-1.2,3.0,0.0\n"
            "Beta,4.4,4.5,4.5\n"
            "Zoo,2.0,10.0,6.0\n",
        )

    def test_missing_input_file_raises_file_not_found(self) -> None:
        """Raise FileNotFoundError when the input file is absent."""
        missing_file = os.path.join(tempfile.gettempdir(), "does-not-exist.csv")

        with self.assertRaises(FileNotFoundError):
            read_observations(missing_file)


if __name__ == "__main__":
    unittest.main()
