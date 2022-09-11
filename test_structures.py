import pytest

from abc import ABC, abstractclassmethod
from decimal import Decimal


class StructureTest(ABC):

    structure: type = None

    @pytest.mark.skip()
    @pytest.mark.filterwarnings()
    @abstractclassmethod
    def test_convert_valid(cls, value):
        assert isinstance(cls.structure(value), cls.structure)

    @pytest.mark.skip()
    @pytest.mark.filterwarnings()
    @abstractclassmethod
    def test_convert_not_valid(cls, value):
        with pytest.raises((ValueError, TypeError)):
            assert isinstance(cls.structure(value), cls.structure)


class TestInt(StructureTest):

    structure: int = int

    @pytest.mark.parametrize('value', ['123', 1, 1.223, Decimal(123)])
    def test_convert_valid(cls, value):
        super().test_convert_valid(value)

    @pytest.mark.parametrize(
        'value',
        ['test', [1, 'test'], {'test_key': 'test_value'}],
    )
    def test_convert_not_valid(self, value):
        super().test_convert_not_valid(value)


class TestFloat(TestInt):

    structure: float = float


class TestStr(StructureTest):

    structure: str = str

    @pytest.mark.parametrize('value', ['test', '123', 1, 1.2])
    def test_convert_valid(cls, value):
        super().test_convert_valid(value)

    def test_immutable(self):
        def assign_string(test_string: str, insert_value: str):
            test_string[0] = insert_value
            return test_string
        try:
            assert assign_string('test_string', 'a')
        except TypeError:
            pass
