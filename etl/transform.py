import re
from typing import Any


RATINGS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
}


def clean_text(value: Any) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(str(value).split())
    return cleaned or None


def parse_price(value: Any) -> float | None:
    cleaned = clean_text(value)
    if not cleaned:
        return None
    number = re.search(r"\d+(?:[.,]\d+)?", cleaned.replace(",", "."))
    return float(number.group()) if number else None


def parse_rating(value: Any) -> int | None:
    cleaned = clean_text(value)
    if not cleaned:
        return None
    if cleaned.lower() in RATINGS:
        return RATINGS[cleaned.lower()]
    number = re.search(r"\d+(?:[.,]\d+)?", cleaned)
    return int(float(number.group().replace(",", "."))) if number else None


def parse_stock(value: Any) -> tuple[str | None, int | None]:
    cleaned = clean_text(value)
    if not cleaned:
        return None, None
    available = re.search(r"(\d+)\s+available", cleaned, flags=re.IGNORECASE)
    return "in_stock" if "in stock" in cleaned.lower() else cleaned, int(available.group(1)) if available else None


def normalize_product(raw: dict[str, Any]) -> dict[str, Any]:
    availability, stock_quantity = parse_stock(raw.get("disponibilidad"))
    product = {
        "fuente": clean_text(raw.get("fuente")),
        "tipo": clean_text(raw.get("tipo")),
        "nombre": clean_text(raw.get("nombre")),
        "precio": parse_price(raw.get("precio")),
        "calificacion": parse_rating(raw.get("calificacion")),
        "url": clean_text(raw.get("url")),
        "categoria": clean_text(raw.get("categoria")),
        "disponibilidad": availability,
        "stock_quantity": stock_quantity,
        "descripcion": clean_text(raw.get("descripcion")),
    }
    if not product["nombre"] or not product["url"] or not product["tipo"] or not product["fuente"]:
        raise ValueError("El producto requiere fuente, tipo, nombre y URL")
    if product["precio"] is not None and product["precio"] < 0:
        raise ValueError("El precio no puede ser negativo")
    if product["calificacion"] is not None and not 1 <= product["calificacion"] <= 5:
        raise ValueError("La calificacion debe estar entre 1 y 5")
    return product


def normalize_products(raw_products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    seen = set()
    for raw in raw_products:
        product = normalize_product(raw)
        key = (product["fuente"], product["url"])
        if key not in seen:
            seen.add(key)
            normalized.append(product)
    return normalized
