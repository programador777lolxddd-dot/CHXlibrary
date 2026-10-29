from datetime import date, datetime, timedelta

import pytest

import chrotrixurum as chx


def test_slugify_handles_accents_and_punctuation():
    assert chx.slugify("¡Hola Mundo Ñandú!") == "hola-mundo-nandu"


def test_case_conversions():
    assert chx.snake_case("HolaMundoCruel") == "hola_mundo_cruel"
    assert chx.camel_case("hola mundo_cruel") == "HolaMundoCruel"


def test_truncate_includes_suffix_in_limit():
    assert chx.truncate("Chrotrixurum eterno", 10) == "Chrotrixu…"
    assert chx.truncate("corto", 10) == "corto"
    assert chx.truncate("texto", 0) == ""
    with pytest.raises(ValueError):
        chx.truncate("texto", -1)


def test_palindrome_ignores_spaces_and_punctuation():
    assert chx.is_palindrome("Anita lava la tina")
    assert not chx.is_palindrome("Python")


def test_number_helpers():
    assert chx.clamp(15, 0, 10) == 10
    assert chx.clamp(5, 10, 0) == 5
    assert chx.lerp(0, 10, 0.5) == 5
    assert chx.is_prime(97)
    assert not chx.is_prime(1)
    assert list(chx.fibonacci(6)) == [0, 1, 1, 2, 3, 5]
    with pytest.raises(ValueError):
        list(chx.fibonacci(-1))


def test_percent():
    assert chx.percent(1, 4) == "25.0%"
    assert chx.percent(1, 0) == "0%"
    with pytest.raises(ValueError):
        chx.percent(1, 4, decimals=-1)


def test_dates():
    assert chx.days_between(date(2024, 1, 1), date(2024, 1, 10)) == 9
    assert chx.is_weekend(date(2024, 1, 6))
    assert not chx.is_weekend(date(2024, 1, 8))
    assert chx.humanize_delta(timedelta(hours=3)) == "dentro de 3 horas"
    assert chx.humanize_delta(timedelta(hours=-3)) == "hace 3 horas"
    assert chx.humanize_delta(timedelta(seconds=0)) == "ahora mismo"


def test_file_helpers(tmp_path):
    assert chx.human_size(1536) == "1.5 KB"
    with pytest.raises(ValueError):
        chx.human_size(-1)

    path = tmp_path / "nested" / "example.txt"
    chx.ensure_dir(path.parent)
    path.write_text("uno\ndos\n", encoding="utf-8")
    assert list(chx.read_lines_safe(path)) == ["uno", "dos"]
    assert chx.ensure_dir(path.parent) == path.parent


def test_creative_helpers_are_reproducible():
    assert chx.divine("pregunta", seed=42) == chx.divine("pregunta", seed=42)
    assert chx.sigil("texto", 8) == chx.sigil("texto", 8)
    assert len(chx.sigil("texto", 8)) == 8
    with pytest.raises(ValueError):
        chx.sigil("texto", -1)
    result = chx.palindrome_magic("Anita lava la tina")
    assert result["es_palindromo"] is True
    assert result["karma"] == "elevado"


def test_version_and_cli_entrypoint_exist():
    assert chx.__version__ == "0.1.0"
    assert callable(chx.main)
