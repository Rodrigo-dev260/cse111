"""Automated tests for the Inventory Control System (CSE 111 W07)."""
import csv
from datetime import datetime, timedelta
from unittest.mock import patch
import pytest
import inventory_control as storage


@pytest.fixture(autouse=True)
def isolated_inventory(tmp_path, monkeypatch):
    """Prevent tests from changing the actual inventory file."""
    monkeypatch.setattr(storage, 'DATA_FILE', tmp_path / 'inventory.csv')
    monkeypatch.setattr(storage, 'inventory', [])


def product(name='Rice', category='Shelf-Stable', quantity=10, expiration_date='31/12/2099'):
    return {'name': name, 'category': category, 'quantity': quantity, 'expiration_date': expiration_date}


def run_with_inputs(function, answers):
    """Run an interactive function with simulated user answers."""
    with patch('builtins.input', side_effect=answers):
        function()


def test_validate_date_accepts_valid_dates():
    assert storage.validate_date('01/01/2026') is True
    assert storage.validate_date('29/02/2024') is True


def test_validate_date_rejects_invalid_dates():
    assert storage.validate_date('31/02/2026') is False
    assert storage.validate_date('29/02/2025') is False


def test_load_inventory_when_file_is_missing():
    storage.inventory.append(product())
    storage.load_inventory()
    assert storage.inventory == []
    storage.inventory.append(product('Beans'))
    storage.load_inventory()
    assert storage.inventory == []


def test_save_and_load_inventory():
    storage.inventory.append(product())
    storage.save_inventory()
    storage.inventory.clear()
    storage.load_inventory()
    assert storage.inventory == [product()]
    storage.inventory.append(product('Beans'))
    storage.save_inventory()
    storage.inventory.clear()
    storage.load_inventory()
    assert storage.inventory == [product(), product('Beans')]


def test_save_inventory_writes_english_headers():
    storage.inventory.append(product())
    storage.save_inventory()
    with storage.DATA_FILE.open(newline='', encoding='utf-8') as file:
        rows = csv.DictReader(file)
        assert rows.fieldnames == ['name', 'category', 'quantity', 'expiration_date']
    storage.inventory.append(product('Beans'))
    storage.save_inventory()
    with storage.DATA_FILE.open(newline='', encoding='utf-8') as file:
        rows = list(csv.DictReader(file))
        assert len(rows) == 2


def test_choose_category():
    with patch('builtins.input', return_value='1'):
        assert storage.choose_category() == 'Shelf-Stable'
    with patch('builtins.input', return_value='2'):
        assert storage.choose_category() == 'Frozen'


def test_register_product():
    run_with_inputs(storage.register_product, ['Beans', '1', '8', '20/10/2099'])
    assert storage.inventory == [product('Beans', quantity=8, expiration_date='20/10/2099')]
    run_with_inputs(storage.register_product, ['Chicken', '2', '6', '21/10/2099'])
    assert len(storage.inventory) == 2


def test_register_product_rejects_invalid_data():
    run_with_inputs(storage.register_product, ['Beans', '1', '-1', '20/10/2099'])
    assert storage.inventory == []
    run_with_inputs(storage.register_product, ['Beans', '1', '5', '31/02/2026'])
    assert storage.inventory == []


def test_list_inventory_empty(capsys):
    storage.list_inventory()
    assert 'No products registered' in capsys.readouterr().out
    storage.list_inventory()
    assert 'No products registered' in capsys.readouterr().out


def test_list_inventory_displays_products(capsys):
    storage.inventory.append(product())
    storage.list_inventory()
    assert 'Rice' in capsys.readouterr().out
    storage.inventory.append(product('Beans'))
    storage.list_inventory()
    assert 'Beans' in capsys.readouterr().out


def test_record_stock_in_increases_quantity():
    storage.inventory.append(product())
    run_with_inputs(storage.record_stock_in, ['1', '5'])
    assert storage.inventory[0]['quantity'] == 15
    run_with_inputs(storage.record_stock_in, ['1', '2'])
    assert storage.inventory[0]['quantity'] == 17


def test_record_stock_in_rejects_negative_quantity():
    storage.inventory.append(product())
    run_with_inputs(storage.record_stock_in, ['1', '-2'])
    assert storage.inventory[0]['quantity'] == 10
    run_with_inputs(storage.record_stock_in, ['1', '0'])
    assert storage.inventory[0]['quantity'] == 10


def test_record_stock_out_decreases_quantity():
    storage.inventory.append(product())
    run_with_inputs(storage.record_stock_out, ['1', '4'])
    assert storage.inventory[0]['quantity'] == 6
    run_with_inputs(storage.record_stock_out, ['1', '2'])
    assert storage.inventory[0]['quantity'] == 4


def test_record_stock_out_rejects_invalid_quantity():
    storage.inventory.append(product())
    run_with_inputs(storage.record_stock_out, ['1', '11'])
    assert storage.inventory[0]['quantity'] == 10
    run_with_inputs(storage.record_stock_out, ['1', '-3'])
    assert storage.inventory[0]['quantity'] == 10


def test_stock_operations_reject_invalid_product_number(capsys):
    storage.inventory.append(product())
    run_with_inputs(storage.record_stock_in, ['2'])
    assert 'Invalid product' in capsys.readouterr().out
    run_with_inputs(storage.record_stock_out, ['2'])
    assert 'Invalid product' in capsys.readouterr().out


def test_check_alerts_low_stock(capsys):
    storage.inventory.append(product(quantity=3))
    storage.check_alerts()
    assert 'Low stock: Rice' in capsys.readouterr().out
    storage.inventory[0]['quantity'] = 4
    storage.check_alerts()
    assert 'Low stock: Rice' in capsys.readouterr().out


def test_check_alerts_expired_product(capsys):
    yesterday = (datetime.today() - timedelta(days=2)).strftime('%d/%m/%Y')
    storage.inventory.append(product(expiration_date=yesterday))
    storage.check_alerts()
    assert 'EXPIRED' in capsys.readouterr().out
    storage.inventory.append(product('Beans', expiration_date=yesterday))
    storage.check_alerts()
    assert 'Beans' in capsys.readouterr().out


def test_check_alerts_no_alerts(capsys):
    storage.inventory.append(product())
    storage.check_alerts()
    assert 'No alerts at this time' in capsys.readouterr().out
    storage.inventory.append(product('Beans'))
    storage.check_alerts()
    assert 'No alerts at this time' in capsys.readouterr().out


def test_report_by_category_filters_products(capsys):
    storage.inventory.extend([product(), product('Chicken', 'Frozen', 6)])
    run_with_inputs(storage.report_by_category, ['2'])
    assert 'Chicken' in capsys.readouterr().out
    run_with_inputs(storage.report_by_category, ['1'])
    assert 'Rice | Qty' in capsys.readouterr().out


def test_main_menu_exits(capsys):
    run_with_inputs(storage.main_menu, ['7'])
    assert 'Closing the system. Goodbye!' in capsys.readouterr().out
    run_with_inputs(storage.main_menu, ['7'])
    assert 'Closing the system. Goodbye!' in capsys.readouterr().out
