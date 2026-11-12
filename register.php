<?php
require 'db.php';

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name']);
    $email = trim($_POST['email']);
    $password = $_POST['password'];

    if (empty($name) || empty($email) || empty($password)) {
        $error = "Заполните все поля!";
    } elseif (strlen($name) < 2 || strlen($name) > 50) {
        $error = "Имя должно быть от 2 до 50 символов.";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error = "Введите корректный email.";
    } elseif (strlen($password) < 6) {
        $error = "Пароль должен быть не менее 6 символов.";
    } elseif (strlen($password) > 50) {
        $error = "Пароль не должен превышать 50 символов.";
    } else {
        $hash = password_hash($password, PASSWORD_DEFAULT);
        try {
            $stmt = $db->prepare("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)");
            $stmt->execute([$name, $email, $hash]);
            header("Location: login.php");
            exit;
        } catch (PDOException $e) {
            $error = "Этот email уже занят.";
        }
    }
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Регистрация — Колледж.Банк</title>
    <style>
        body { font-family: sans-serif; background: #f4f7f6; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .card { background: #fff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        h2 { margin-top: 0; color: #2c3e50; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        .btn-reg { width: 100%; padding: 12px; background: #2ecc71; color: #fff; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; margin-top: 10px; }
        .btn-reg:hover { background: #27ae60; }
        .error { color: #e74c3c; margin-bottom: 10px; font-size: 14px; }
        .link-back { display: block; margin-top: 15px; color: #3498db; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Регистрация</h2>
        <?php if ($error) echo "<p class='error'>$error</p>"; ?>
        <form method="POST">
            <input type="text" name="name" placeholder="Ваше имя" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Пароль (от 6 до 50 символов)" required>
            <button type="submit" class="btn-reg">Зарегистрироваться</button>
        </form>
        <a href="login.php" class="link-back">Уже есть аккаунт? Войти</a>
    </div>
</body>
</html>