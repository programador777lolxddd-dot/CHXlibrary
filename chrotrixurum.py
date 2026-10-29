#!/usr/bin/env python3
"""
Chrotrixurum — utilidades místicas y prácticas para Python.
Versión monolítica (un solo archivo).

Uso como librería:
    >>> import chrotrixurum as chx
    >>> chx.slugify("Hola Mundo Ñandú")
    'hola-mundo-nandu'

Uso como script (demo):
    $ python chrotrixurum.py
"""

from __future__ import annotations

import hashlib
import random
import re
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterator, Union

__version__ = "0.1.0"
__all__ = [
    # strings
    "slugify", "snake_case", "camel_case", "truncate", "is_palindrome",
    # numbers
    "clamp", "lerp", "is_prime", "fibonacci", "percent",
    # dates
    "humanize_delta", "days_between", "is_weekend",
    # files
    "human_size", "read_lines_safe", "ensure_dir",
    # arcana
    "divine", "sigil", "palindrome_magic",
    # metadatos
    "__version__",
]


# ─────────────────────────────────────────────────────────────────────
# strings
# ─────────────────────────────────────────────────────────────────────
def _strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def slugify(text: str) -> str:
    """Convierte texto en slug URL-friendly.

    >>> slugify("Hola Mundo Ñandú!")
    'hola-mundo-nandu'
    """
    text = _strip_accents(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def snake_case(text: str) -> str:
    """Convierte CamelCase o texto libre a snake_case.

    >>> snake_case("HolaMundoCruel")
    'hola_mundo_cruel'
    """
    text = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    return re.sub(r"[\s\-]+", "_", text).lower().strip("_")


def camel_case(text: str) -> str:
    """Convierte texto a CamelCase.

    >>> camel_case("hola mundo cruel")
    'HolaMundoCruel'
    """
    parts = re.split(r"[_\-\s]+", text.strip())
    return "".join(p.capitalize() for p in parts if p)


def truncate(text: str, length: int, suffix: str = "…") -> str:
    """Trunca un texto respetando un sufijo.

    >>> truncate("Chrotrixurum eterno", 10)
    'Chrotrixur…'
    """
    if length <= len(suffix):
        return suffix[:length]
    return text if len(text) <= length else text[: length - len(suffix)] + suffix


def is_palindrome(text: str, ignore_case: bool = True) -> bool:
    """True si el texto es palíndromo (ignora signos y espacios).

    >>> is_palindrome("Anita lava la tina")
    True
    """
    clean = re.sub(r"[^a-zA-Z0-9]", "", _strip_accents(text))
    if ignore_case:
        clean = clean.lower()
    return clean == clean[::-1]


# ─────────────────────────────────────────────────────────────────────
# numbers
# ─────────────────────────────────────────────────────────────────────
def clamp(value: float, lo: float, hi: float) -> float:
    """Limita *value* al rango [lo, hi].

    >>> clamp(15, 0, 10)
    10
    """
    if lo > hi:
        lo, hi = hi, lo
    return max(lo, min(hi, value))


def lerp(a: float, b: float, t: float) -> float:
    """Interpolación lineal entre *a* y *b* con factor *t* ∈ [0,1].

    >>> lerp(0, 10, 0.5)
    5.0
    """
    return a + (b - a) * clamp(t, 0.0, 1.0)


def is_prime(n: int) -> bool:
    """Determina si *n* es primo.

    >>> is_prime(97)
    True
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def fibonacci(n: int) -> Iterator[int]:
    """Generador con los primeros *n* números de Fibonacci.

    >>> list(fibonacci(6))
    [0, 1, 1, 2, 3, 5]
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def percent(part: float, whole: float, decimals: int = 1) -> str:
    """Porcentaje formateado de *part* sobre *whole*.

    >>> percent(1, 4)
    '25.0%'
    """
    if whole == 0:
        return "0%"
    return f"{part / whole * 100:.{decimals}f}%"


# ─────────────────────────────────────────────────────────────────────
# dates
# ─────────────────────────────────────────────────────────────────────
def humanize_delta(delta: timedelta) -> str:
    """Convierte un timedelta en frase legible.

    >>> humanize_delta(timedelta(hours=3, minutes=20))
    'hace 3 horas'
    """
    seconds = int(abs(delta.total_seconds()))
    future = delta.total_seconds() >= 0
    units = [
        ("año", 365 * 24 * 3600), ("mes", 30 * 24 * 3600),
        ("día", 24 * 3600), ("hora", 3600),
        ("minuto", 60), ("segundo", 1),
    ]
    for name, secs in units:
        if seconds >= secs:
            count = seconds // secs
            plural = "s" if count != 1 and name != "mes" else ""
            label = f"{count} {name}{plural}"
            return f"{'dentro de' if future else 'hace'} {label}"
    return "ahora mismo"


def days_between(a: date, b: date) -> int:
    """Días absolutos entre dos fechas.

    >>> days_between(date(2024, 1, 1), date(2024, 1, 10))
    9
    """
    return abs((b - a).days)


def is_weekend(d: Union[date, datetime, None] = None) -> bool:
    """True si la fecha cae en sábado o domingo.

    >>> is_weekend(date(2024, 1, 6))
    True
    """
    d = d or date.today()
    return d.weekday() >= 5


# ─────────────────────────────────────────────────────────────────────
# files
# ─────────────────────────────────────────────────────────────────────
def human_size(bytes_: int) -> str:
    """Bytes a cadena legible.

    >>> human_size(1536)
    '1.5 KB'
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(bytes_)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def read_lines_safe(path: Union[str, Path]) -> Iterator[str]:
    """Lee un archivo línea a línea sin cargarlo entero en memoria."""
    p = Path(path)
    with p.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            yield line.rstrip("\n")


def ensure_dir(path: Union[str, Path]) -> Path:
    """Crea el directorio si no existe y lo devuelve."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


# ─────────────────────────────────────────────────────────────────────
# arcana
# ─────────────────────────────────────────────────────────────────────
_SIGILS = "⛧⛥✧✦✩✶✷✸❂☽☾♆♇♄♅⛤"


def divine(question: str, seed: Union[int, None] = None) -> str:
    """Veredicto astral determinista (misma pregunta ⇒ misma respuesta).

    >>> divine("¿Aprobaré?", seed=42) == divine("¿Aprobaré?", seed=42)
    True
    """
    rng = random.Random(seed if seed is not None else question)
    respuestas = [
        "sí, sin duda.", "es posible.", "los astros guardan silencio.",
        "no cuentes con ello.", "sí, pero con esfuerzo.",
        "pregunta de nuevo más tarde.", "definitivamente no.",
        "las señales apuntan a que sí.",
    ]
    return f"Los astros susurran: {rng.choice(respuestas)}"


def sigil(text: str, length: int = 12) -> str:
    """Sigilo determinista a partir de un texto.

    >>> len(sigil("chrotrixurum", 8))
    8
    """
    digest = hashlib.sha256(text.encode()).digest()
    rng = random.Random(digest)
    return "".join(rng.choice(_SIGILS) for _ in range(length))


def palindrome_magic(text: str) -> dict:
    """Analiza el karma palindrómico de una frase."""
    clean = re.sub(r"[^a-zA-Z0-9]", "", _strip_accents(text)).lower()
    is_pal = clean == clean[::-1]
    return {
        "texto": text,
        "limpio": clean,
        "es_palindromo": is_pal,
        "longitud": len(clean),
        "karma": "elevado" if is_pal else "terrenal",
        "veredicto": (
            f"{sigil(text)} Los ecos se repiten. Karma elevado."
            if is_pal else
            f"{sigil(text)} Los ecos se dispersan. Karma terrenal."
        ),
    }


# ─────────────────────────────────────────────────────────────────────
# demo / CLI
# ─────────────────────────────────────────────────────────────────────
def _demo() -> None:
    print(f"🔮 Chrotrixurum v{__version__}\n")
    print("slugify :", slugify("Hola Mundo Ñandú!"))
    print("snake   :", snake_case("HolaMundoCruel"))
    print("camel   :", camel_case("hola mundo cruel"))
    print("truncate:", truncate("Chrotrixurum eterno", 10))
    print("palindr :", is_palindrome("Anita lava la tina"))
    print("clamp   :", clamp(15, 0, 10))
    print("lerp    :", lerp(0, 10, 0.5))
    print("primo97 :", is_prime(97))
    print("fib(6)  :", list(fibonacci(6)))
    print("percent :", percent(1, 4))
    print("size    :", human_size(1536))
    print("delta   :", humanize_delta(timedelta(hours=3, minutes=20)))
    print("weekend :", is_weekend(date(2024, 1, 6)))
    print("divine  :", divine("¿Aprobaré el examen?"))
    print("sigil   :", sigil("chrotrixurum"))
    print("magic   :", palindrome_magic("Anita lava la tina")["veredicto"])


if __name__ == "__main__":
    _demo()