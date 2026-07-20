from src.file_filters import expected_test_file, is_production_file, is_test_path, prod_has_matching_test


def test_production_file_detection():
    assert is_production_file("models.py")
    assert not is_production_file("test_models.py")


def test_test_path_detection():
    assert is_test_path("tests/test_models.py")
    assert is_test_path("test_models.py")


def test_expected_test_file_mapping():
    assert expected_test_file("models.py") == "test_models.py"


def test_prod_has_matching_test():
    assert prod_has_matching_test("test_models.py", "models.py")
