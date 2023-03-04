PrefixSpan Algorithm
==========================================

Environment
-----

- Ubuntu 22.04
- Python 3.10.6

Usage
-----

To run the program with *minSupport* = 0.3 and *maxPatternLength* = 5

    python3 prefixspan.py -f seqdata.dat -s 0.3 -l 5

Test
-----

To run the unittest

    cd prefixspan
    python3 -m unittest test_prefixspan.py
