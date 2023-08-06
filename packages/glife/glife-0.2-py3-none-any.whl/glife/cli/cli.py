import os

from .arguments import parse
from ..colony.colony import Colony
from ..colony.exception.colony_exception import ColonyException
from ..gol.arguments import Arguments as GolArguments
from .start_field.only_string import input_field as field_from_string
from .start_field.string_with_width import input_field as field_from_string_with_width
from .start_field.from_file import input_field as field_from_file
from ..gol.factory import Factory
from ..gol.field import Field


def create_gol_arguments(args: object) -> GolArguments:
    if args.file_start_generation:
        field = field_from_file(args.file_start_generation, args.file_false, args.file_true)
    elif (args.width > 0):
        field = field_from_string_with_width(args.start_generation, args.width)
    elif args.start_generation != '':
        field = field_from_string(args.start_generation)
    else:
        print("Can't determine the start generation - please use --help to find how to use this app")
        exit(1)

    width: int = field.width()
    start_generation: str = field.__str__()

    return GolArguments(start_generation, width)


def show_generation(generation_number: int, generation: Field) -> None:
    print(f" >> gen: {generation_number}")
    for point in generation:
        value = generation.state_point(point)
        if value:
            # char = chr(9634)
            # char = ' ' + chr(9632)
            char = 'O '
        else:
            # char = chr(1468) + ' '
            char = '. '
        if point.x == generation.geometry().x - 1:
            print(char)
        else:
            print(char, end='')


def run():

    args = parse()

    gol_arguments = create_gol_arguments(args)
    gol = Factory.create_from_arguments(gol_arguments)
    colony = Colony(gol)

    try:
        for i in range(0, args.generations + 1):

            if args.clear:
                os.system('clear')

            if args.quiet:
                print('.', end='')
            else:
                show_generation(i, colony.field())

            if args.interactive:
                input("Press Enter to continue...")

            if i < args.generations:
                    colony.next_generation()

    except ColonyException as exception:
        print()
        print(exception.message)
        print(f"generation: {i}")


if __name__ == '__main__':
    run()
