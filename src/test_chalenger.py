# Copyright (c) 2024 Renan Evaristo
# ruff: noqa: S101

import pytest
from _pytest.monkeypatch import MonkeyPatch
from unittest.mock import patch, MagicMock
from src.chalenger import key_validation, transfer_data_to_csv, validate_connection_get_response


def test_key_validation_success(monkeypatch: MonkeyPatch) -> None:
    """Testa o carregamento bem-sucedido da chave de API."""
    monkeypatch.setenv("RGAPI_KEY", "chave_de_teste_123")
    resultado = key_validation()
    assert resultado == "chave_de_teste_123"


def test_key_validation_failure() -> None:
    """Testa se o programa encerra quando a chave de API está ausente."""
    with patch("os.getenv", return_value=None), pytest.raises(SystemExit) as e:
        key_validation()
    assert e.value.code == 1
