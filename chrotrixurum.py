#!/usr/bin/env python3
"""
CHXLibrary — utilidades prácticas para Python.

Uso como librería:
    >>> import chrotrixurum as chx
    >>> chx.slugify("Hola Mundo Ñandú")
    'hola-mundo-nandu'

Uso como script:
    $ python -m chrotrixurum
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
    "slugify", "snake_case", "camel_case", "truncate", "is_palindrome",
    "clamp", "lerp", "is_prime", "fibonacci", "percent",
    "humanize_delta", "days_between", "is_weekend",
    "human_size", "read_lines_safe", "ensure_dir",
    "divine", "sigil", "palindrome_magic", "main", "__version__",
]


# ---------------------------------------------------------------------
# Strings
# ---------------------------------------------------------------------
def _strip_accents(text: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )


def slugify(text: str) -> str:
    """Convierte texto en un slug apto para URLs."""
    text = _strip_accents(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def snake_case(text: str) -> str:
    """Convierte CamelCase o texto libre a snake_case."""
    text = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    return re.sub(r"[\s\-]+", "_", text).lower().strip("_")


def camel_case(text: str) -> str:
    """Convierte texto separado por espacios, guiones o guiones bajos a CamelCase."""
    parts = re.split(r"[_\-\s]+", text.strip())
    return "".join(part.capitalize() for part in parts if part)


def truncate(text: str, length: int, suffix: str = "…") -> str:
    """Limita un texto a *length* caracteres, incluyendo el sufijo."""
    if length < 0:
        raise ValueError("length no puede ser negativo")
    if length == 0:
        return ""
    if len(text) <= length:
        return text
    if length <= len(suffix):
        return suffix[:length]
    return text[: length - len(suffix)] + suffix


def is_palindrome(text: str, ignore_case: bool = True) -> bool:
    """Comprueba si un texto es palíndromo, ignorando espacios y signos."""
    clean = re.sub(r"[^a-zA-Z0-9]", "", _strip_accents(text))
    if ignore_case:
        clean = clean.lower()
    return clean == clean[::-1]


# ---------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------
def clamp(value: float, lo: float, hi: float) -> float:
    """Limita *value* al rango [lo, hi]. Si el rango está invertido, lo corrige."""
    if lo > hi:
        lo, hi = hi, lo
    return max(lo, min(hi, value))


def lerp(a: float, b: float, t: float) -> float:
    """Interpola linealmente entre *a* y *b*, limitando *t* al rango [0, 1]."""
    return a + (b - a) * clamp(t, 0.0, 1.0)


def is_prime(n: int) -> bool:
    """Devuelve True si *n* es un número primo."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    divisor = 5
    while divisor * divisor <= n:
        if n % divisor == 0 or n % (divisor + 2) == 0:
            return False
        divisor += 6
    return True


def fibonacci(n: int) -> Iterator[int]:
    """Genera los primeros *n* números de Fibonacci."""
    if n < 0:
        raise ValueError("n no puede ser negativo")
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def percent(part: float, whole: float, decimals: int = 1) -> str:
    """Devuelve *part* como porcentaje de *whole*, formateado como texto."""
    if decimals < 0:
        raise ValueError("decimals no puede ser negativo")
    if whole == 0:
        return "0%"
    return f"{part / whole * 100:.{decimals}f}%"


# ---------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------
def humanize_delta(delta: timedelta) -> str:
    """Convierte una diferencia temporal en una frase en español.

    Una diferencia positiva se interpreta como tiempo futuro; una negativa,
    como tiempo pasado.
    """
    total_seconds = delta.total_seconds()
    seconds = int(abs(total_seconds))
    future = total_seconds >= 0
    units = [
        ("año", 365 * 24 * 3600), ("mes", 30 * 24 * 3600),
        ("día", 24 * 3600), ("hora", 3600), ("minuto", 60),
        ("segundo", 1),
    ]
    for name, unit_seconds in units:
        if seconds >= unit_seconds:
            count = seconds // unit_seconds
            plural = "s" if count != 1 else ""
            label = f"{count} {name}{plural}"
            return f"{'dentro de' if future else 'hace'} {label}"
    return "ahora mismo"


def days_between(a: date, b: date) -> int:
    """Devuelve el número absoluto de días entre dos fechas."""
    return abs((b - a).days)


def is_weekend(d: Union[date, datetime, None] = None) -> bool:
    """Comprueba si una fecha es sábado o domingo; por defecto usa hoy."""
    d = d or date.today()
    return d.weekday() >= 5


# ---------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------
def human_size(bytes_: int) -> str:
    """Convierte una cantidad de bytes a una unidad legible."""
    if bytes_ < 0:
        raise ValueError("bytes_ no puede ser negativo")
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(bytes_)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def read_lines_safe(path: Union[str, Path]) -> Iterator[str]:
    """Lee un archivo UTF-8 línea por línea, reemplazando bytes inválidos."""
    with Path(path).open("r", encoding="utf-8", errors="replace") as file:
        for line in file:
            yield line.rstrip("\r\n")


def ensure_dir(path: Union[str, Path]) -> Path:
    """Crea un directorio y sus padres si no existen, y devuelve su ruta."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


# ---------------------------------------------------------------------
# Creative utilities
# ---------------------------------------------------------------------
_SIGILS = "⛧⛥✧✦✩✶✷✸❂☽☾♆♇♄♅⛤"


def divine(question: str, seed: Union[int, None] = None) -> str:
    """Genera una respuesta creativa; con la misma semilla es reproducible."""
    rng = random.Random(seed if seed is not None else question)
    answers = [
        "sí, sin duda.", "es posible.", "los astros guardan silencio.",
        "no cuentes con ello.", "sí, pero con esfuerzo.",
        "pregunta de nuevo más tarde.", "definitivamente no.",
        "las señales apuntan a que sí.",
    ]
    return f"Los astros susurran: {rng.choice(answers)}"


def sigil(text: str, length: int = 12) -> str:
    """Genera un sigilo reproducible a partir de un texto."""
    if length < 0:
        raise ValueError("length no puede ser negativo")
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    rng = random.Random(digest)
    return "".join(rng.choice(_SIGILS) for _ in range(length))


def palindrome_magic(text: str) -> dict:
    """Devuelve un análisis lúdico de una frase y su posible palíndromo."""
    clean = re.sub(r"[^a-zA-Z0-9]", "", _strip_accents(text)).lower()
    is_pal = clean == clean[::-1]
    if is_pal:
        verdict = f"{sigil(text)} Los ecos se repiten. Karma elevado."
    else:
        verdict = f"{sigil(text)} Los ecos se dispersan. Karma terrenal."
    return {
        "texto": text,
        "limpio": clean,
        "es_palindromo": is_pal,
        "longitud": len(clean),
        "karma": "elevado" if is_pal else "terrenal",
        "veredicto": verdict,
    }


def main() -> None:
    """Ejecuta una demostración breve de las funciones principales."""
    print(f"CHXLibrary v{__version__}\n")
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
    print("sigil   :", sigil("chxlibrary"))


if __name__ == "__main__":
    main()
