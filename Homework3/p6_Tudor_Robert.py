"""Model a storage system of files and folders and estimate storage size."""

from __future__ import annotations


class Entry:
    """Base class for any item stored on the storage system.

    Attributes:
        name: The entry's name.
        _parent: The folder that contains this entry, or None for the root.
    """

    def __init__(self, name: str) -> None:
        """Create an entry with the given name and no parent.

        Args:
            name: The entry's name.
        """
        self.name = name
        self._parent: Entry | None = None

    def parent(self) -> Entry | None:
        """Return the entry that contains this one, or None if it is the root."""
        return self._parent

    def size(self) -> int:
        """Return the storage size of this entry in bytes.

        Subclasses must override this method.

        Raises:
            NotImplementedError: Always, since a plain Entry has no size.
        """
        raise NotImplementedError("Subclasses of Entry must implement size()")

    def absolute_path(self) -> list[Entry]:
        """Return the path from this entry up to the root, computed recursively.

        Returns:
            A list of Entry objects starting with this entry, then its parent,
            and so on, ending with the root entry (whose parent is None).
        """
        parent = self.parent()
        if parent is None:
            return [self]
        return [self] + parent.absolute_path()

    def __repr__(self) -> str:
        """Return a readable representation showing the class and name."""
        return f"{type(self).__name__}({self.name!r})"


class File(Entry):
    """A file that uses a fixed number of bytes.

    Attributes:
        bytes_used: The nonnegative number of bytes the file uses.
    """

    def __init__(self, name: str, bytes_used: int) -> None:
        """Create a file with the given name and size.

        Args:
            name: The file's name.
            bytes_used: The number of bytes the file uses.

        Raises:
            ValueError: If bytes_used is negative.
        """
        super().__init__(name)
        if bytes_used < 0:
            raise ValueError("bytes_used must be nonnegative")
        self.bytes_used = bytes_used

    def size(self) -> int:
        """Return the number of bytes this file uses."""
        return self.bytes_used


class Folder(Entry):
    """A folder that holds files and other folders.

    Attributes:
        _children: The entries stored directly in this folder.
    """

    def __init__(self, name: str) -> None:
        """Create an empty folder with the given name.

        Args:
            name: The folder's name.
        """
        super().__init__(name)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add entry to this folder and make this folder its parent.

        The entry should not already belong to another folder.

        Args:
            entry: The file or folder to add.
        """
        entry._parent = self
        self._children.append(entry)

    def children(self) -> tuple[Entry, ...]:
        """Return a tuple with all the children in this folder."""
        return tuple(self._children)

    def size(self) -> int:
        """Return the total size of all children, including nested folders."""
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Recursively find all files at least minimum_size bytes, starting from entry.

    If entry is a File, return a list containing just that file when its size
    is at least minimum_size, otherwise an empty list. If entry is a Folder,
    search each child in order (including nested folders) and return all
    matching files combined into one list. An empty folder, or any other kind
    of Entry, returns an empty list.

    Args:
        entry: The file or folder to start searching from.
        minimum_size: The smallest size in bytes a file can have to be included.

    Returns:
        A list of the matching File objects, in the order they appear in the tree.
    """
    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []
    if isinstance(entry, Folder):
        large_files: list[File] = []
        for child in entry.children():
            large_files += find_large_files(child, minimum_size)
        return large_files
    return []


def print_tree(entry: Entry, indent: int = 0) -> None:
    """Print entry and everything under it, with the size each one adds up to.

    Args:
        entry: The file or folder to print.
        indent: How many levels deep entry is, used to indent the output.
    """
    label = f"{entry.name}/" if isinstance(entry, Folder) else entry.name
    print(f"{'    ' * indent}{label:<{30 - 4 * indent}} {entry.size():>9,} bytes")
    if isinstance(entry, Folder):
        for child in entry.children():
            print_tree(child, indent + 1)


def main() -> None:
    """Build a sample storage tree and demonstrate size(), find_large_files() and absolute_path()."""
    # Part f: build a tree four folders deep, with files at every level.
    university = Folder("university")
    computer_science = Folder("computer_science")
    mathematics = Folder("mathematics")
    cop4045 = Folder("cop4045")
    homework3 = Folder("homework3")

    readme = File("readme.txt", 2_000)
    handbook = File("handbook.pdf", 150_000)
    calendar = File("calendar.txt", 30_000)
    syllabus = File("syllabus.pdf", 80_000)
    p6 = File("p6.py", 4_000)
    dataset = File("dataset.csv", 500_000)

    university.add(readme)
    university.add(computer_science)
    university.add(mathematics)
    computer_science.add(handbook)
    computer_science.add(cop4045)
    mathematics.add(calendar)
    cop4045.add(syllabus)
    cop4045.add(homework3)
    homework3.add(p6)
    homework3.add(dataset)

    print("Part f: size()")
    print(f"university.size() = {university.size():,} bytes")
    print()
    print("What each file and folder adds up to:")
    print_tree(university)
    all_files = find_large_files(university, 0)
    print(f"Sum of all {len(all_files)} file sizes = {sum(f.size() for f in all_files):,} bytes")
    print()

    print("Part f: find_large_files()")
    for threshold in (50_000, 200_000):
        found = find_large_files(university, threshold)
        print(f"Files of at least {threshold:,} bytes: {found}")
    print()

    # Part g: show the path from the deepest file up to the root.
    print("Part g: absolute_path()")
    path = dataset.absolute_path()
    print(f"dataset.absolute_path() = {path}")
    print(" -> ".join(entry.name for entry in path))
    print("z23818028")


if __name__ == "__main__":
    main()
