from simple_value_object import ValueObject, invariant


class Arguments(ValueObject):

    start_generation: str = ''
    width: int = 0

    def __init__(self, start_generation, width=0):
        pass

    @invariant
    def start_generation_is_str(self, instance):
        return type(instance.start_generation) == str

    @invariant
    def width_is_int(self, instance):
        return type(instance.width) == int
