<?php
$host = "localhost";
$user = "root";
$password = "";
$database = "arsipsurat";

$conn = mysqli_connect($host, $user, $password, $database);

// ⬇️ TAMBAHKAN BARIS INI
$db = $conn;

if (!$conn) {
    die("Koneksi gagal: " . mysqli_connect_error());
}
?>
