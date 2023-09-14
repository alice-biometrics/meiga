import pytest

from .example_with_meiga import NoSuchKey, TypeMismatch, string_from_key


@pytest.mark.unit
class TestExampleWithMeiga:
    dictionary = {"key1": "value", "key2": 2}

    def should_success(self):
        result = string_from_key(dictionary=self.dictionary, key="key1")
        result.assert_success(value_is_instance_of=str)

    def should_fail_when_key_does_not_exist(self):
        result = string_from_key(dictionary=self.dictionary, key="invalid_key")
        result.assert_failure(value_is_instance_of=NoSuchKey)

    def should_fail_when_type_mismatch(self):
        result = string_from_key(dictionary=self.dictionary, key="key2")
        result.assert_failure(value_is_instance_of=TypeMismatch)
