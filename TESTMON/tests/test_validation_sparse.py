def test_validation_segment_sparse_only():
    from commerce_platform.validation.segment_000 import ValidationService0
    svc = ValidationService0("tenant-sparse")
    assert svc.health_check() is True
