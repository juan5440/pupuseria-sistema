<?php
// Habilitar errores (solo para desarrollo)
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include 'conexion.php';

// Obtener el ID de la venta desde la URL
$id = $_GET['id'] ?? null;

if (!$id || !is_numeric($id)) {
    http_response_code(400);
    echo json_encode(['error' => 'ID de venta inválido']);
    exit;
}

try {
    // Obtener datos de la venta
    $stmt_venta = $pdo->prepare("SELECT total, pago, cambio FROM ventas WHERE id = ?");
    $stmt_venta->execute([$id]);
    $venta = $stmt_venta->fetch(PDO::FETCH_ASSOC);

    if (!$venta) {
        http_response_code(404);
        echo json_encode(['error' => 'Venta no encontrada']);
        exit;
    }

    // Obtener productos de la venta
    $stmt_productos = $pdo->prepare("
        SELECT p.nombre, dv.cantidad, dv.precio_unitario AS precio
        FROM detalle_venta dv
        JOIN productos p ON dv.producto_id = p.id
        WHERE dv.venta_id = ?
    ");
    $stmt_productos->execute([$id]);
    $productos = $stmt_productos->fetchAll(PDO::FETCH_ASSOC);

    // Combinar todo en una respuesta
    $respuesta = [
        'total' => $venta['total'],
        'pago' => $venta['pago'],
        'cambio' => $venta['cambio'],
        'productos' => $productos
    ];

    // Devolver como JSON
    header('Content-Type: application/json');
    echo json_encode($respuesta);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Error al obtener los datos: ' . $e->getMessage()]);
}
?>