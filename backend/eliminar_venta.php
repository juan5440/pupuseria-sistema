<?php
include 'conexion.php';

$id = $_POST['id'] ?? null;

if ($id) {
    try {
        $stmt = $pdo->prepare("DELETE FROM ventas WHERE id = ?");
        $stmt->execute([$id]);
        echo json_encode(['status' => 'success']);
    } catch (Exception $e) {
        echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'ID no proporcionado']);
}
?>