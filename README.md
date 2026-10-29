# CHXLibrary

**CHXLibrary** es una pequeña colección de utilidades para Python, en español y sin dependencias externas de ejecución. Incluye funciones para trabajar con texto, números, fechas, archivos y herramientas creativas.

- **Distribución en PyPI:** `chxlibrary`
- **Módulo de importación:** `chrotrixurum`
- **Versión actual del proyecto:** `0.1.0`
- **Python:** 3.8 o superior
- **Licencia:** Apache-2.0

## Instalación

Cuando la publicación esté disponible en PyPI:

```bash
python -m pip install chxlibrary
```

Para desarrollar desde este repositorio:

```bash
git clone https://github.com/programador777lolxddd-dot/CHXlibrary.git
cd CHXlibrary
python -m pip install -e ".[dev]"
```

## Inicio rápido

```python
import chrotrixurum as chx

print(chx.slugify("Hola Mundo Ñandú!"))  # hola-mundo-nandu
print(chx.snake_case("HolaMundoCruel"))  # hola_mundo_cruel
print(chx.clamp(15, 0, 10))              # 10
print(chx.is_prime(97))                  # True
print(list(chx.fibonacci(6)))            # [0, 1, 1, 2, 3, 5]
print(chx.human_size(1536))              # 1.5 KB
print(chx.is_weekend())                  # True o False según la fecha actual
```

## Funciones disponibles

### Texto
- `slugify(text)`: convierte texto en un slug para URLs y elimina acentos.
- `snake_case(text)`: convierte texto a `snake_case`.
- `camel_case(text)`: convierte texto a `CamelCase`.
- `truncate(text, length, suffix="…")`: limita la longitud de un texto.
- `is_palindrome(text, ignore_case=True)`: comprueba si un texto es palíndromo.

### Números
- `clamp(value, lo, hi)`: limita un valor a un rango.
- `lerp(a, b, t)`: interpolación lineal con `t` limitado entre 0 y 1.
- `is_prime(n)`: comprueba si un entero es primo.
- `fibonacci(n)`: genera los primeros `n` números de Fibonacci.
- `percent(part, whole, decimals=1)`: devuelve un porcentaje formateado.

### Fechas y tiempo
- `humanize_delta(delta)`: expresa una diferencia temporal en español.
- `days_between(a, b)`: calcula los días absolutos entre dos fechas.
- `is_weekend(d=None)`: comprueba si una fecha es sábado o domingo.

### Archivos
- `human_size(bytes_)`: convierte bytes a una unidad legible.
- `read_lines_safe(path)`: lee un archivo UTF-8 línea por línea.
- `ensure_dir(path)`: crea un directorio y sus padres si hacen falta.

### Herramientas creativas
- `divine(question, seed=None)`: genera una respuesta aleatoria reproducible con semilla.
- `sigil(text, length=12)`: genera un símbolo textual reproducible.
- `palindrome_magic(text)`: devuelve un análisis lúdico de una frase.

## Ejecutar la demostración

```bash
python -m chrotrixurum
```

También puedes usar el comando instalado:

```bash
chrotrixurum
```

## Pruebas

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## Licencia

Este proyecto se distribuye bajo la licencia **Apache License 2.0**. Consulta el archivo [LICENSE](LICENSE) para ver el texto completo.

## Autor y contribuciones

Creado por [programador777lolxddd-dot](https://github.com/programador777lolxddd-dot). Las sugerencias y reportes de errores se pueden enviar en [Issues](https://github.com/programador777lolxddd-dot/CHXlibrary/issues).
