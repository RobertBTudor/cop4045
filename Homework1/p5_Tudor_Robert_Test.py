import unittest

from p5_Tudor_Robert import caesar_cipher, caesar_decipher, letter_frequency


class TestCaesarCipher(unittest.TestCase):

    def test_cipher(self):
        # Test that letters are shifted correctly
        self.assertEqual(caesar_cipher("Hello", 3), "Khoor")

    def test_cipher_with_spaces(self):
        # Test that spaces are preserved
        self.assertEqual(caesar_cipher("Hello World", 3), "Khoor Zruog")

    def test_cipher_preserves_case(self):
        # Test that uppercase and lowercase letters are preserved
        self.assertEqual(caesar_cipher("AbC", 2), "CdE")

    def test_cipher_wraps_around(self):
        # Test that letters wrap around from Z back to A
        self.assertEqual(caesar_cipher("XYZ", 3), "ABC")

    def test_decipher(self):
        # Test that an encrypted message can be decrypted
        self.assertEqual(caesar_decipher("Khoor", 3), "Hello")

    def test_frequency(self):
        # Test the number of times each letter appears
        frequency = letter_frequency("Hello")

        self.assertEqual(frequency[ord('e') - ord('a')], 1)
        self.assertEqual(frequency[ord('h') - ord('a')], 1)
        self.assertEqual(frequency[ord('l') - ord('a')], 2)
        self.assertEqual(frequency[ord('o') - ord('a')], 1)

    def test_frequency_ignores_case(self):
        # Test that uppercase and lowercase letters are counted together
        frequency = letter_frequency("AaAa")

        self.assertEqual(frequency[0], 4)

    def test_frequency_ignores_non_letters(self):
        # Test that spaces and punctuation are not counted
        frequency = letter_frequency("Hello, World!")

        total = sum(frequency)

        self.assertEqual(total, 10)


# Run all tests
if __name__ == "__main__":
    unittest.main()