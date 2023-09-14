import pytest

from .example_without_meiga import NoSuchKey, TypeMismatch, string_from_key


@pytest.mark.unit
class TestExampleWithoutMeiga:
    dictionary = {"key1": "value", "key2": 2}

    def should_return_a_str(self):
        value = string_from_key(dictionary=self.dictionary, key="key1")
        assert isinstance(value, str)

    def should_raises_non_such_key_exception(self):
        with pytest.raises(NoSuchKey):
            _ = string_from_key(dictionary=self.dictionary, key="invalid_key")

    def should_raises_type_mismatch_exception(self):
        with pytest.raises(TypeMismatch):
            value = string_from_key(dictionary=self.dictionary, key="key2")
            assert not isinstance(value, str)
