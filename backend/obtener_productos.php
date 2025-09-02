<?php
include 'conexion.php';

$stmt = $pdo->query("SELECT id, nombre, precio FROM productos ORDER BY nombre");
$productos = $stmt->fetchAll(PDO::FETCH_ASSOC);

header('Content-Type: application/json');
echo json_encode($productos);
