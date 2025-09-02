<?php
include 'conexion.php';

$data = json_decode(file_get_contents('php://input'), true);

try {
    $pdo->beginTransaction();

    // Insertar venta
    $stmt = $pdo->prepare("INSERT INTO ventas (total, pago, cambio) VALUES (?, ?, ?)");
    $stmt->execute([$data['total'], $data['pago'], $data['cambio']]);
    $venta_id = $pdo->lastInsertId();

    // Insertar detalles
    foreach ($data['detalle'] as $item) {
        $stmt_prod = $pdo->prepare("SELECT id, precio FROM productos WHERE nombre = ?");
        $stmt_prod->execute([$item['nombre']]);
        $producto = $stmt_prod->fetch();

        if ($producto) {
            $stmt_det = $pdo->prepare("INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)");
            $stmt_det->execute([$venta_id, $producto['id'], $item['cantidad'], $producto['precio']]);
        }
    }

    $pdo->commit();
    echo json_encode(['status' => 'success']);
} catch (Exception $e) {
    $pdo->rollback();
    echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
}
?>