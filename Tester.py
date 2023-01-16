from Compete import Compete


def main():
    competition = Compete(character="Chy")
    competition.random_bracket()
    competition.top(100)


if __name__ == '__main__':
    main()
