from src.models import Parameters, Transfer
from src.manager import Manager


def _transfer(amount: float) -> Transfer:
    return Transfer(amount_pln=amount, date='2025-01-10', settlement_year=2025, settlement_month=1, tenant='tenant-1')


def test_manager_has_transfer_limits():
    manager = Manager(Parameters())

    assert isinstance(manager.min_transfer_pln, (int, float))
    assert isinstance(manager.max_transfer_pln, (int, float))
    assert manager.min_transfer_pln < manager.max_transfer_pln


def test_default_data_has_no_invalid_transfers():
    manager = Manager(Parameters())

    assert manager.validate_transfers() == []


def test_transfers_outside_limits_are_reported():
    manager = Manager(Parameters())
    manager.min_transfer_pln = 100.0
    manager.max_transfer_pln = 5000.0

    too_small = _transfer(50.0)
    at_min = _transfer(100.0)
    normal = _transfer(2500.0)
    at_max = _transfer(5000.0)
    too_large = _transfer(6000.0)
    manager.transfers = [too_small, at_min, normal, at_max, too_large]

    invalid = manager.validate_transfers()

    assert len(invalid) == 2
    assert too_small in invalid
    assert too_large in invalid


def test_negative_transfer_is_invalid_when_min_is_zero():
    manager = Manager(Parameters())
    manager.min_transfer_pln = 0.0
    manager.max_transfer_pln = 10000.0

    negative = _transfer(-10.0)
    manager.transfers = [negative, _transfer(1500.0)]

    assert manager.validate_transfers() == [negative]


def test_no_transfers_means_no_errors():
    manager = Manager(Parameters())
    manager.transfers = []

    assert manager.validate_transfers() == []