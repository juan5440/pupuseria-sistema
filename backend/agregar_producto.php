<?php
include 'conexion.php';

$nombre = trim($_POST['nombre'] ?? '');
$precio = $_POST['precio'] ?? null;

if (!$nombre || !$precio || !is_numeric($precio)) {
    echo json_encode(['status' => 'error', 'message' => 'Datos inválidos']);
    exit;
}

try {
    $stmt = $pdo->prepare("INSERT INTO productos (nombre, precio) VALUES (?, ?)");
    $stmt->execute([$nombre, $precio]);
    echo json_encode(['status' => 'success']);
} catch (Exception $e) {
    echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
}
