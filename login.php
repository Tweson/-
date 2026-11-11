<?php
require 'db.php';

if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: login.php");
    exit;
}

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email']);
    $password = $_POST['password'];

    if ($email === 'admin') {
        $email = 'admin@local';
    }

    if (empty($email) || empty($password)) {
        $error = "Заполните все поля!";
    } else {
        $stmt = $db->prepare("SELECT * FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user['password_hash'])) {
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['user_name'] = $user['name'];
            $_SESSION['user_role'] = $user['role'];
            header("Location: index.php");
            exit;
        } else {
            $error = "Неверный логин или пароль.";
        }
    }
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Вход — Колледж.Банк</title>
    <style>
        body { font-family: sans-serif; background: #f4f7f6; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .card { background: #fff; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        h2 { margin-top: 0; color: #2c3e50; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        .btn-login { width: 100%; padding: 12px; background: #3498db; color: #fff; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; margin-top: 10px; }
        .btn-login:hover { background: #2980b9; }
        .error { color: #e74c3c; margin-bottom: 10px; font-size: 14px; }
        .divider { margin: 20px 0; border-top: 1px solid #eee; position: relative; }
        .divider span { background: #fff; padding: 0 10px; position: relative; top: -10px; color: #999; font-size: 14px; }
        .btn-register { display: block; width: 100%; padding: 12px; background: #2ecc71; color: #fff; text-decoration: none; border-radius: 5px; font-size: 16px; font-weight: bold; box-sizing: border-box; }
        .btn-register:hover { background: #27ae60; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Вход в систему</h2>
        <?php if ($error) echo "<p class='error'>$error</p>"; ?>
        <form method="POST">
            <input type="text" name="email" placeholder="Email или admin" required>
            <input type="password" name="password" placeholder="Пароль" required>
            <button type="submit" class="btn-login">Войти</button>
        </form>
        <div class="divider"><span>или</span></div>
        <a href="register.php" class="btn-register">Создать новый аккаунт</a>
    </div>
</body>
</html>