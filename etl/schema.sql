PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS fuentes (
    id_fuente INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    url TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY,
    id_fuente INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('libro', 'tecnologia')),
    nombre TEXT NOT NULL,
    precio REAL CHECK (precio IS NULL OR precio >= 0),
    calificacion REAL CHECK (calificacion IS NULL OR calificacion BETWEEN 1 AND 5),
    url TEXT NOT NULL,
    UNIQUE (id_fuente, url),
    FOREIGN KEY (id_fuente) REFERENCES fuentes(id_fuente)
);

CREATE TABLE IF NOT EXISTS tecnologia (
    id_producto INTEGER PRIMARY KEY,
    descripcion TEXT,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS libros (
    id_producto INTEGER PRIMARY KEY,
    id_categoria INTEGER,
    disponibilidad TEXT,
    stock_quantity INTEGER CHECK (stock_quantity IS NULL OR stock_quantity >= 0),
    descripcion TEXT,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE INDEX IF NOT EXISTS idx_productos_tipo ON productos(tipo);
CREATE INDEX IF NOT EXISTS idx_productos_fuente ON productos(id_fuente);
CREATE INDEX IF NOT EXISTS idx_libros_categoria ON libros(id_categoria);
