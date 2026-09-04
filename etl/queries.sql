-- 1. Producto junto con la fuente
SELECT p.id_producto, p.nombre, p.tipo, p.precio, f.nombre AS fuente
FROM productos AS p
JOIN fuentes AS f ON f.id_fuente = p.id_fuente
ORDER BY p.tipo, p.nombre;

-- 2. Informacion relacionada con categorias
SELECT p.nombre AS producto, c.nombre AS categoria, l.disponibilidad, l.stock_quantity
FROM libros AS l
JOIN productos AS p ON p.id_producto = l.id_producto
LEFT JOIN categorias AS c ON c.id_categoria = l.id_categoria
ORDER BY c.nombre, p.nombre;

-- 3. Cuantos productos existen de cada tipo
SELECT tipo, COUNT(*) AS cantidad
FROM productos
GROUP BY tipo
ORDER BY tipo;

-- 4. Producto mas costoso
SELECT p.nombre, p.precio, f.nombre AS fuente
FROM productos AS p
JOIN fuentes AS f ON f.id_fuente = p.id_fuente
WHERE p.precio = (SELECT MAX(precio) FROM productos);

-- 5. Producto mas economico
SELECT p.nombre, p.precio, f.nombre AS fuente
FROM productos AS p
JOIN fuentes AS f ON f.id_fuente = p.id_fuente
WHERE p.precio = (SELECT MIN(precio) FROM productos WHERE precio IS NOT NULL);

-- 6. Precio promedio
SELECT ROUND(AVG(precio), 2) AS precio_promedio
FROM productos;

-- 7. Calificacion promedio
SELECT ROUND(AVG(calificacion), 2) AS calificacion_promedio
FROM productos;

-- 8. Fuente que proporciona mas productos
SELECT f.nombre AS fuente, COUNT(*) AS cantidad
FROM productos AS p
JOIN fuentes AS f ON f.id_fuente = p.id_fuente
GROUP BY f.id_fuente, f.nombre
ORDER BY cantidad DESC
LIMIT 1;
