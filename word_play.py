import sys
from collections import defaultdict


class WordPlay:

    def __init__(self, players_file):
        with open(players_file) as fobj:
            self.players = [name.strip() for name in fobj]

    def pop_name(self, source: list, exclude: str) -> list:
        target = list(source)
        target.remove(exclude)
        return target

    def names_with_match(self, target: str, player_names: list) -> list:
        return [name for name in player_names if target[0] in name]

    def match(self, target: str, player_names: list) -> list:
        self.total_iterations += 1
        matching_names = self.names_with_match(target, player_names)

        if matching_names:
            if target[1:]:
                for name in matching_names:

                    dt = self.match(target[1:], self.pop_name(player_names, name))

                    if dt:
                        dt.append((target[0], name))
                        return dt

            else:
                dt = list()
                dt.append((target[0], matching_names[0]))
                return dt

    def pretty_print(self, matched_names: list):
        dt2 = [(letter, name.index(letter), len(name), name) for letter, name in matched_names]
        max_index_len = max(dt2, key=lambda x: x[1])[1]
        for letter, index, lenn, name in dt2:
            name = name.rjust(max_index_len + lenn - index)
            name = name.replace(letter, "\033[95m{}\033[00m".format(letter.upper()), 1)
            print(name)

    def print_possibility(self, target_name: str) -> None:

        if len(target_name) > len(self.players):
            print('Not Possible')
            return False

        count_occurrence = defaultdict(int)
        for letter in target_name:
            count_occurrence[letter] += 1

        for letter in count_occurrence.keys():
            if count_occurrence[letter] > len(self.names_with_match(letter, self.players)):
                print('Not Possible')
                return False

        self.total_iterations = 0
        dt = self.match(target_name, self.players)
        print('Total Iterations: ', self.total_iterations )
        if dt:
            dt.reverse()
            self.pretty_print(dt)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        word_play = WordPlay('./players.txt')
        word_play.print_possibility(sys.argv[1].replace(' ', '').lower())
    else:
        print('Pass a name to match as an argument')
