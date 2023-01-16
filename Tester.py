from Compete import Compete


def main():
    competition = Compete(directory=None, json_file="testdata2.json")
    competition.random_bracket()
    competition.top(5)

if __name__ == '__main__':
    main()
