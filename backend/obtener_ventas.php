<?php
include 'conexion.php';

$stmt = $pdo->query("
    SELECT v.id, v.fecha, v.total, v.pago, v.cambio,
           GROUP_CONCAT(CONCAT(p.nombre, ' x', dv.cantidad) SEPARATOR ', ') AS productos
    FROM ventas v
    LEFT JOIN detalle_venta dv ON v.id = dv.venta_id
    LEFT JOIN productos p ON dv.producto_id = p.id
    GROUP BY v.id
    ORDER BY v.fecha DESC
");
$ventas = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo json_encode($ventas);
