import sys

seq = sys.argv[1]


def parse(sequence):
    length = len(sequence)
    nucleotides = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
    for term in sequence:
        nucleotides[term] += 1
    print('Sequence has ' + str(length) + ' nucleotides.')
    for term in nucleotides:
        print(str(term) + ': ' + str(nucleotides[term]))

    return ()


parse(seq)
