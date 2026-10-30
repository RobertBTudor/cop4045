"""Unit tests for find_large_files() and Entry.absolute_path() in p6_Tudor_Robert."""

import unittest

from p6_Tudor_Robert import File, Folder, find_large_files


class TestFindLargeFiles(unittest.TestCase):
    """Tests for the find_large_files() function."""

    def test_single_file_above_threshold(self) -> None:
        """A file larger than the threshold is returned in a list."""
        file = File("big.txt", 500)
        self.assertEqual(find_large_files(file, 100), [file])

    def test_single_file_below_threshold(self) -> None:
        """A file smaller than the threshold returns an empty list."""
        file = File("small.txt", 50)
        self.assertEqual(find_large_files(file, 100), [])

    def test_single_file_at_threshold(self) -> None:
        """A file exactly at the threshold is included."""
        file = File("exact.txt", 100)
        self.assertEqual(find_large_files(file, 100), [file])

    def test_empty_folder(self) -> None:
        """An empty folder contains no files, so the result is empty."""
        self.assertEqual(find_large_files(Folder("empty"), 0), [])

    def test_nested_folders(self) -> None:
        """Matching files are found at every level, in tree order."""
        root = Folder("root")
        sub = Folder("sub")
        deep = Folder("deep")
        a = File("a.txt", 300)
        b = File("b.txt", 50)
        c = File("c.txt", 200)
        d = File("d.txt", 1000)
        root.add(a)
        root.add(sub)
        sub.add(b)
        sub.add(deep)
        deep.add(c)
        deep.add(d)

        self.assertEqual(find_large_files(root, 200), [a, c, d])
        self.assertEqual(find_large_files(root, 0), [a, b, c, d])
        self.assertEqual(find_large_files(root, 5000), [])


class TestAbsolutePath(unittest.TestCase):
    """Tests for the Entry.absolute_path() method."""

    def test_root_alone(self) -> None:
        """The root's path contains only the root itself."""
        root = Folder("root")
        self.assertEqual(root.absolute_path(), [root])

    def test_deeply_nested_file(self) -> None:
        """A nested file's path runs from the file up to the root, in order."""
        root = Folder("root")
        level1 = Folder("level1")
        level2 = Folder("level2")
        level3 = Folder("level3")
        file = File("deep.txt", 10)
        root.add(level1)
        level1.add(level2)
        level2.add(level3)
        level3.add(file)

        path = file.absolute_path()
        expected = [file, level3, level2, level1, root]
        self.assertEqual(len(path), len(expected))
        for actual, wanted in zip(path, expected):
            self.assertIs(actual, wanted)


if __name__ == "__main__":
    unittest.main()
