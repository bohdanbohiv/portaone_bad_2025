from collections.abc import Collection, Iterable
from copy import copy
from sys import argv


def main():
    if len(argv) < 2:
        print('Usage: python main.py <filename>')
        return
    with open(argv[1], 'r') as source:
        numbers = PrefixMap(source)

    longest_sequences = LongestSequences()
    for num in numbers:
        longest_sequences.adds(find_longest_sequences(numbers, num, []))

    for sequence in longest_sequences:
        print_sequence(sequence)


class PrefixMap(tuple):
    def __new__(cls, numbers: Iterable[str]):
        return super().__new__(cls, (list() for _ in range(10 ** 2)))

    def __init__(self, numbers: Iterable[str]):
        super().__init__()
        for num in numbers:
            num = num.strip()
            self[int(num[:2])].append(num)

    def remove(self, number: str) -> None:
        self[int(number[:2])].remove(number)

    def __copy__(self):
        cp = PrefixMap([])
        for i in range(10 ** 2):
            cp[i].extend(self[i])
        return cp

    def __iter__(self) -> Iterator[str]:
        for l in super().__iter__():
            for n in l:
                yield n


class LongestSequences(list):
    def __init__(self):
        super().__init__()
        self.append([])

    def add(self, sequence: list) -> None:
        if len(sequence) > len(self[0]):
            self.clear()
            self.append(sequence)
        elif len(sequence) == len(self[0]):
            self.append(sequence)

    def adds(self, sequences: Collection[list]) -> None:
        assert len(set(map(len, sequences))) <= 1
        seq_i = iter(sequences)
        if sequences:
            seq = next(seq_i)
            if len(seq) < len(self[0]):
                return
            self.add(seq)
        self.extend(seq_i)


def find_longest_sequences(numbers: PrefixMap, next_n: str, seq: list
                           ) -> list[list[str]]:
    numbers = copy(numbers)
    seq = copy(seq)
    seq.append(next_n)
    numbers.remove(next_n)
    while numbers[int(seq[-1][-2:])]:
        if len(numbers[int(seq[-1][-2:])]) > 1:
            longest_sequences = LongestSequences()
            for num in numbers[int(seq[-1][-2:])]:
                longest_sequences.adds(
                    find_longest_sequences(numbers, num, seq))
            return longest_sequences
        next_n = numbers[int(seq[-1][-2:])][0]
        seq.append(next_n)
        numbers.remove(next_n)
    return [seq]


def print_sequence(sequence: list[str]) -> None:
    print(sequence[0][:2], end='')
    for num in sequence:
        print(num[2:], end='')
    print()


if __name__ == '__main__':
    main()
