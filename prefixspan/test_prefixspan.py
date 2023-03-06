import os
import unittest
from prefixspan import PrefixSpan, data_from_file


class PrefixSpanTest(unittest.TestCase):

    def test_subsets_should_return_empty_subsets_if_input_empty_set(self):
        sequences = []
        model = PrefixSpan.train(sequences, minSupport=0.3, maxPatternLength=5)
        result = model.freqSequences().collect()

        self.assertEqual(result, [])

    def test_subsets_should_return_non_empty_subsets(self):
        sequences = [[[1]], [[2]]]
        model = PrefixSpan.train(sequences, minSupport=0.3, maxPatternLength=5)
        result = model.freqSequences().collect()

        self.assertEqual((result[0].sequence, result[0].freq), ([[1]], 1))
        self.assertEqual((result[1].sequence, result[1].freq), ([[2]], 1))

    def test_subsets_should_return_some_subsets(self):
        sequences = [
            [[1, 5], [2], [3], [4]],
            [[1], [3], [4], [3, 5]],
            [[1], [2], [3], [4]],
            [[1], [3], [5]],
            [[4], [5]]
        ]
        model = PrefixSpan.train(sequences, minSupport=0.3, maxPatternLength=5)
        result = model.freqSequences().collect()

        self.assertEqual((result[0].sequence, result[0].freq), ([[2]], 2))
        self.assertEqual((result[1].sequence, result[1].freq), ([[2], [3]], 2))
        self.assertEqual((result[2].sequence, result[2].freq), ([[2], [3], [4]], 2))
        self.assertEqual((result[3].sequence, result[3].freq), ([[2], [4]], 2))
        self.assertEqual((result[4].sequence, result[4].freq), ([[1]], 4))
        self.assertEqual((result[5].sequence, result[5].freq), ([[1], [2]], 2))
        self.assertEqual((result[6].sequence, result[6].freq), ([[1], [2], [3]], 2))
        self.assertEqual((result[7].sequence, result[7].freq), ([[1], [2], [3], [4]], 2))
        self.assertEqual((result[8].sequence, result[8].freq), ([[1], [2], [4]], 2))
        self.assertEqual((result[9].sequence, result[9].freq), ([[1], [5]], 2))
        self.assertEqual((result[10].sequence, result[10].freq), ([[1], [4]], 3))
        self.assertEqual((result[11].sequence, result[11].freq), ([[1], [3]], 4))
        self.assertEqual((result[12].sequence, result[12].freq), ([[1], [3], [5]], 2))
        self.assertEqual((result[13].sequence, result[13].freq), ([[1], [3], [4]], 3))
        self.assertEqual((result[14].sequence, result[14].freq), ([[5]], 4))
        self.assertEqual((result[15].sequence, result[15].freq), ([[3]], 4))
        self.assertEqual((result[16].sequence, result[16].freq), ([[3], [5]], 2))
        self.assertEqual((result[17].sequence, result[17].freq), ([[3], [4]], 3))
        self.assertEqual((result[18].sequence, result[18].freq), ([[4]], 4))
        self.assertEqual((result[19].sequence, result[19].freq), ([[4], [5]], 2))

    def test_read_data_from_file(self):
        data = "         1         11          1        11          5       145          2       4103         3       8715         4\n" +\
               "         2         66          1        90          3       109          4       203          3       203          5\n" +\
               "         3        128          1       139          2       157          3       189          4\n" +\
               "         4        162          1       169          3       176          5       176\n" +\
               "         5        188          4       194          5       211"
        os.system(f'echo \'{data}\' > test.dat')
        result = data_from_file('test.dat')

        expected = [
            [[1, 5], [2], [3], [4]],
            [[1], [3], [4], [3, 5]],
            [[1], [2], [3], [4]],
            [[1], [3], [5]],
            [[4], [5]]
        ]
        self.assertEqual(result, expected)

        os.system('rm test.dat')


if __name__ == '__main__':
    unittest.main()
