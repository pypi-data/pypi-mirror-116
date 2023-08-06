import argparse


class Arguments:
    width: int = 0
    height: int = 0
    start_generation: str = ''
    file_start_generation: str = ''
    file_false: str = '0'
    file_true: str = '1'
    generations: int = 1
    interactive: bool = False
    clear: bool = False
    quiet: bool = False


def parse() -> object:
    parser = argparse.ArgumentParser(
        epilog='2021 Łukasz Bacik <mail@luka.sh> https://github.com/lbacik/glife'
    )

    parser.add_argument('-s', '--start-generation', nargs='?', default=Arguments.start_generation)
    parser.add_argument('-f', '--file-start-generation', nargs='?', default=Arguments.file_start_generation)
    parser.add_argument('--file-false', nargs='?', default=Arguments.file_false)
    parser.add_argument('--file-true', nargs='?', default=Arguments.file_true)
    parser.add_argument('-w', '--width', nargs='?', default=Arguments.width, type=int)
    parser.add_argument('-g', '--generations', nargs='?', default=Arguments.generations, type=int)
    parser.add_argument('-i', '--interactive', action='store_const', const=True)
    parser.add_argument('-c', '--clear', action='store_const', const=True)
    parser.add_argument('-q', '--quiet', action='store_const', const=True)

    return parser.parse_args(namespace=Arguments)
