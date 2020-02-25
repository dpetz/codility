#https://coderpad.io/WP3PHTC6

class Datasource(object):
    def __init__(self,numbers):
        self.numbers = numbers

    def map(self,mapper):
        numbers = [mapper(n) for n in self.numbers]
        return Datasource(numbers)

    def collect(self):
        return self.numbers.copy()


def test_collect_with_a_single_map():
    d = Datasource([1,2,3]).map(lambda x: x*2)

    assert d.collect() == [2,4,6]

def test_collect_with_two_maps():
    initial = Datasource([1,2,3])

    first = initial.map(lambda x: x*2)

    second = first.map(lambda x: x*3)

    assert initial.collect() == [1,2,3]
    assert first.collect() == [2,4,6]
    assert second.collect() == [6,12,18]

test_collect_with_a_single_map()
test_collect_with_two_maps()
print("All tests passed!")