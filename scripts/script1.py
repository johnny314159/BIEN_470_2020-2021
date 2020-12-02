import sys

sequence_path = sys.argv[1]
print(sequence_path)
rawseq = open(sequence_path, 'r')
seq = rawseq.readlines()


def parse(sequence):
    seq_string = ''
    for each in range(len(sequence)):
        seq_string += sequence[each].replace('\n', '')


    length = len(seq_string)
    nucleotides = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
    for term in seq_string:
        nucleotides[term] += 1
    print('Sequence has ' + str(length) + ' nucleotides.')
    for term in nucleotides:
        print(str(term) + ': ' + str(nucleotides[term]))

    return ()


parse(seq)

