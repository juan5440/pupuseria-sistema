<?php
include 'conexion.php';

$id = $_POST['id'] ?? null;
$nombre = trim($_POST['nombre'] ?? '');
$precio = $_POST['precio'] ?? null;

if (!$id || !$nombre || !$precio || !is_numeric($precio)) {
    echo json_encode(['status' => 'error', 'message' => 'Datos inválidos']);
    exit;
}

try {
    $stmt = $pdo->prepare("UPDATE productos SET nombre = ?, precio = ? WHERE id = ?");
    $stmt->execute([$nombre, $precio, $id]);
    echo json_encode(['status' => 'success']);
} catch (Exception $e) {
    echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
}
