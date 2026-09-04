import argparse
import json
from pathlib import Path

from scrapy.crawler import CrawlerProcess

from .database import load_database
from .spiders import BooksSpider, LaptopsSpider


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "etl_output"
DATABASE_PATH = ROOT / "etl.db"


def extract() -> list[Path]:
    OUTPUT_DIR.mkdir(exist_ok=True)
    process = CrawlerProcess(
        settings={
            "BOT_NAME": "etl_scraper",
            "ROBOTSTXT_OBEY": True,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
            "DOWNLOAD_DELAY": 0.25,
            "USER_AGENT": "scrapy-etl-laboratory/1.0",
            "FEEDS": {
                str(OUTPUT_DIR / "%(name)s.json"): {
                    "format": "json",
                    "encoding": "utf8",
                    "overwrite": True,
                }
            },
            "LOG_LEVEL": "INFO",
        }
    )
    process.crawl(BooksSpider)
    process.crawl(LaptopsSpider)
    process.start()
    return [OUTPUT_DIR / "books_etl.json", OUTPUT_DIR / "laptops_etl.json"]


def print_queries() -> None:
    import sqlite3

    query_path = Path(__file__).with_name("queries.sql")
    queries = [part.strip() for part in query_path.read_text(encoding="utf-8").split(";") if part.strip()]
    with sqlite3.connect(DATABASE_PATH) as connection:
        for index, query in enumerate(queries, start=1):
            clean_query = "\n".join(line for line in query.splitlines() if not line.strip().startswith("--"))
            rows = connection.execute(clean_query).fetchall()
            print(f"\nConsulta {index}")
            for row in rows[:10]:
                print(row)
            if len(rows) > 10:
                print(f"... ({len(rows)} filas en total)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta el ETL de libros y tecnologia")
    parser.add_argument("--skip-extract", action="store_true", help="Usa los JSON existentes")
    args = parser.parse_args()

    json_paths = [
        OUTPUT_DIR / "books_etl.json",
        OUTPUT_DIR / "laptops_etl.json",
    ] if args.skip_extract else extract()
    missing = [str(path) for path in json_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Faltan archivos de extraccion: {', '.join(missing)}")
    total = load_database(json_paths, DATABASE_PATH)
    print(f"Productos normalizados y cargados: {total}")
    print(f"Base SQLite: {DATABASE_PATH}")
    print_queries()


if __name__ == "__main__":
    main()
