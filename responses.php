<?php
require 'db.php';

$is_auth = is_logged_in();
$is_admin = is_admin();
$userName = $_SESSION['user_name'] ?? '';
$initial = mb_substr($userName, 0, 1);
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Отклики — Колледж.Банк</title>
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
        .container { max-width: 800px; margin: 30px auto; text-align: center; }
        .empty-state { background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .btn { background: #3498db; color: #fff; text-decoration: none; border: none; padding: 10px 20px; border-radius: 4px; display: inline-block; font-size: 16px; margin-top: 15px; }
    </style>
</head>
<body>
    <header>
        <div class="header-inner">
            <a href="index.php" class="logo">Колледж.Банк</a>
            <nav class="nav">
                <a href="index.php">Заявки</a>
                <a href="responses.php">Отклики</a>
                <?php if ($is_auth): ?>
                    <a href="profile.php" class="nav-right">Личный кабинет</a>
                <?php else: ?>
                    <a href="login.php" class="nav-right">Вход</a>
                    <a href="register.php">Регистрация</a>
                <?php endif; ?>
            </nav>
            <div class="user-panel">
                <?php if ($is_auth): ?>
                    <a href="profile.php" class="user-info">
                        <div class="avatar"><?= htmlspecialchars(mb_strtoupper($initial)) ?></div>
                        <span class="user-name"><?= htmlspecialchars($userName) ?></span>
                        <?php if ($is_admin): ?><span class="role-badge">ADMIN</span><?php endif; ?>
                    </a>
                    <a href="login.php?logout=1" class="logout-btn">
                        <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                    </a>
                <?php endif; ?>
            </div>
        </div>
    </header>

    <div class="container">
        <div class="empty-state">
            <h2>Мои отклики</h2>
            <?php if ($is_auth): ?>
                <p style="color: #777; font-size: 16px;">Здесь пока пусто. Вы еще не оставляли откликов на заявки.</p>
                <a href="index.php" class="btn">Перейти к заявкам</a>
            <?php else: ?>
                <p style="color: #777; font-size: 16px;">Вы не авторизованы. Войдите в аккаунт, чтобы увидеть свои отклики.</p>
                <a href="login.php" class="btn">Войти в аккаунт</a>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>