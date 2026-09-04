import json
import sqlite3
from pathlib import Path
from typing import Any

from .transform import normalize_products


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def load_json(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    return data if isinstance(data, list) else [data]


def load_database(json_paths: list[Path], database_path: Path) -> int:
    raw_products = [item for path in json_paths for item in load_json(path)]
    products = normalize_products(raw_products)
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        source_urls = {
            "Books to Scrape": "https://books.toscrape.com/",
            "Web Scraper Test Sites": "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
        }
        for source_name, source_url in source_urls.items():
            connection.execute(
                "INSERT OR IGNORE INTO fuentes (nombre, url) VALUES (?, ?)",
                (source_name, source_url),
            )

        source_ids = {
            name: source_id
            for name, source_id in connection.execute(
                "SELECT nombre, id_fuente FROM fuentes"
            )
        }
        for product in products:
            category_id = None
            if product["tipo"] == "libro" and product["categoria"]:
                connection.execute(
                    "INSERT OR IGNORE INTO categorias (nombre) VALUES (?)",
                    (product["categoria"],),
                )
                category_id = connection.execute(
                    "SELECT id_categoria FROM categorias WHERE nombre = ?",
                    (product["categoria"],),
                ).fetchone()[0]

            connection.execute(
                """INSERT INTO productos
                (id_fuente, tipo, nombre, precio, calificacion, url)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id_fuente, url) DO UPDATE SET
                    tipo = excluded.tipo,
                    nombre = excluded.nombre,
                    precio = excluded.precio,
                    calificacion = excluded.calificacion""",
                (
                    source_ids[product["fuente"]], product["tipo"], product["nombre"],
                    product["precio"], product["calificacion"], product["url"],
                ),
            )
            product_id = connection.execute(
                "SELECT id_producto FROM productos WHERE id_fuente = ? AND url = ?",
                (source_ids[product["fuente"]], product["url"]),
            ).fetchone()[0]
            if product["tipo"] == "libro":
                connection.execute(
                    """INSERT INTO libros
                    (id_producto, id_categoria, disponibilidad, stock_quantity, descripcion)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(id_producto) DO UPDATE SET
                        id_categoria = excluded.id_categoria,
                        disponibilidad = excluded.disponibilidad,
                        stock_quantity = excluded.stock_quantity,
                        descripcion = excluded.descripcion""",
                    (product_id, category_id, product["disponibilidad"], product["stock_quantity"], product["descripcion"]),
                )
            else:
                connection.execute(
                    """INSERT INTO tecnologia (id_producto, descripcion)
                    VALUES (?, ?)
                    ON CONFLICT(id_producto) DO UPDATE SET descripcion = excluded.descripcion""",
                    (product_id, product["descripcion"]),
                )
    return len(products)
