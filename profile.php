<?php
require 'db.php';

if (!is_logged_in()) {
    header("Location: login.php");
    exit;
}

$userId = $_SESSION['user_id'];
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name']);
    $bio = trim($_POST['bio']);
    $skills = trim($_POST['skills']);

    if (empty($name) || strlen($name) < 2 || strlen($name) > 50) {
        $error = "Имя должно быть от 2 до 50 символов.";
    } else {
        $stmt = $db->prepare("UPDATE users SET name = ?, bio = ?, skills = ? WHERE id = ?");
        $stmt->execute([$name, $bio, $skills, $userId]);
        $_SESSION['user_name'] = $name;
        header("Location: profile.php");
        exit;
    }
}

$stmt = $db->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$userId]);
$user = $stmt->fetch();

$userName = $_SESSION['user_name'] ?? '';
$initial = $userName !== '' ? strtoupper(substr($userName, 0, 1)) : '';
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Личный кабинет — Колледж.Банк</title>
    <style>
        body { font-family: sans-serif; background: #f4f7f6; margin: 0; }
        .header-inner { display: flex; justify-content: space-between; align-items: center; padding: 0 30px; height: 60px; background: #2c3e50; color: #fff; }
        .logo { font-size: 20px; font-weight: bold; color: #fff; text-decoration: none; }
        .nav { display: flex; gap: 20px; align-items: center; }
        .nav a { color: #ccc; text-decoration: none; font-size: 15px; }
        .nav a:hover { color: #fff; }
        .nav-right { margin-left: auto; }
        .user-panel { display: flex; align-items: center; gap: 15px; }
        .user-info { display: flex; align-items: center; gap: 10px; text-decoration: none; color: inherit; }
        .avatar { width: 32px; height: 32px; background: #3498db; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; color: #fff; }
        .user-name { font-size: 14px; color: #fff; }
        .role-badge { background: #e74c3c; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-left: 5px; }
        .logout-btn { color: #ccc; display: flex; padding: 5px; border-radius: 4px; }
        .logout-btn:hover { color: #e74c3c; background: rgba(255,255,255,0.1); }
        .container { max-width: 700px; margin: 30px auto; }
        .card { background: #fff; padding: 25px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .info-row { margin-bottom: 15px; font-size: 16px; color: #333; }
        .info-label { font-weight: bold; color: #555; display: inline-block; width: 100px; }
        .bio-text { margin-top: 5px; line-height: 1.6; color: #333; font-size: 15px; }
        .form-group { margin-bottom: 15px; }
        input, textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-family: sans-serif; }
        button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .error-msg { color: #e74c3c; background: #fadbd8; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
    </style>
</head>
<body>
    <header>
        <div class="header-inner">
            <a href="index.php" class="logo">Колледж.Банк</a>
            <nav class="nav">
                <a href="index.php">Заявки</a>
                <a href="responses.php">Мои отклики</a>
                <a href="profile.php" class="nav-right">Личный кабинет</a>
            </nav>
            <div class="user-panel">
                <a href="profile.php" class="user-info">
                    <div class="avatar"><?= htmlspecialchars($initial) ?></div>
                    <span class="user-name"><?= htmlspecialchars($userName) ?></span>
                    <?php if (is_admin()): ?><span class="role-badge">ADMIN</span><?php endif; ?>
                </a>
                <a href="login.php?logout=1" class="logout-btn">
                    <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                </a>
            </div>
        </div>
    </header>

    <div class="container">
        <?php if ($error) echo "<div class='error-msg'>$error</div>"; ?>

        <div class="card">
            <h2 style="margin-top: 0; color: #2c3e50;"><?= htmlspecialchars($user['name']) ?></h2>
            <div class="info-row"><span class="info-label">Email:</span> <?= htmlspecialchars($user['email']) ?></div>
            <div class="info-row"><span class="info-label">Роль:</span> <?= $user['role'] === 'admin' ? 'Администратор' : 'Пользователь' ?></div>
            <div class="info-row"><span class="info-label">Навыки:</span> <?= htmlspecialchars($user['skills'] ?: 'Не указаны') ?></div>
            <div class="info-row" style="margin-top: 20px;">
                <span class="info-label" style="width: auto; display: block; margin-bottom: 5px;">О себе:</span>
                <div class="bio-text"><?= nl2br(htmlspecialchars($user['bio'] ?: 'Информация не заполнена')) ?></div>
            </div>
        </div>

        <div class="card">
            <h3 style="margin-top: 0;">Редактировать профиль</h3>
            <form method="POST">
                <div class="form-group"><input type="text" name="name" value="<?= htmlspecialchars($user['name']) ?>" placeholder="Имя" required></div>
                <div class="form-group"><input type="text" name="skills" value="<?= htmlspecialchars($user['skills']) ?>" placeholder="Навыки"></div>
                <div class="form-group"><textarea name="bio" rows="4" placeholder="Расскажите о себе"><?= htmlspecialchars($user['bio']) ?></textarea></div>
                <button type="submit">Сохранить изменения</button>
            </form>
        </div>
    </div>
</body>
</html>