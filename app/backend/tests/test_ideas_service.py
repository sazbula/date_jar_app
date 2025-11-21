from app.backend.services import ideas_service


def test_validate_categories_success():
    ideas_service.validate_categories(["home"])


def test_validate_categories_empty():
    try:
        ideas_service.validate_categories([])
        assert False, "Should raise"
    except Exception:
        assert True


def test_validate_categories_too_many():
    try:
        ideas_service.validate_categories(["a", "b", "c", "d"])
        assert False
    except Exception:
        assert True


def test_validate_categories_invalid():
    try:
        ideas_service.validate_categories(["invalid"])
        assert False
    except Exception:
        assert True
