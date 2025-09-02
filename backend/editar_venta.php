<?php
include 'conexion.php';

$data = json_decode(file_get_contents('php://input'), true);
$id = $data['id'];

try {
    $stmt = $pdo->prepare("UPDATE ventas SET pago = ?, cambio = ? WHERE id = ?");
    $stmt->execute([$data['pago'], $data['cambio'], $id]);
    echo json_encode(['status' => 'success']);
} catch (Exception $e) {
    echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
}
?>