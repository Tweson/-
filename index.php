<?php
require 'db.php';

$is_auth = is_logged_in();
$is_admin = is_admin();
$userId = $is_auth ? $_SESSION['user_id'] : null;
$action = $_GET['action'] ?? 'list';
$id = (int)($_GET['id'] ?? 0);
$error = '';
$categories = $db->query("SELECT * FROM categories")->fetchAll();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $is_auth) {
    if (isset($_POST['create'])) {
        $title = trim($_POST['title']);
        $desc = trim($_POST['description']);
        
        if (empty($title) || empty($desc) || empty($_POST['category_id'])) {
            $error = "Заполните все поля!";
        } elseif (mb_strlen($title) > 100) {
            $error = "Заголовок не должен превышать 100 символов.";
        } else {
            $stmt = $db->prepare("INSERT INTO requests (user_id, category_id, title, description) VALUES (?, ?, ?, ?)");
            $stmt->execute([$userId, $_POST['category_id'], $title, $desc]);
            header("Location: index.php");
            exit;
        }
    }
    if (isset($_POST['update'])) {
        $title = trim($_POST['title']);
        $desc = trim($_POST['description']);
        
        if (empty($title) || empty($desc) || empty($_POST['category_id'])) {
            $error = "Заполните все поля!";
        } elseif (mb_strlen($title) > 100) {
            $error = "Заголовок не должен превышать 100 символов.";
        } else {
            if ($is_admin) {
                $stmt = $db->prepare("UPDATE requests SET title = ?, description = ?, category_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?");
                $stmt->execute([$title, $desc, $_POST['category_id'], $id]);
            } else {
                $stmt = $db->prepare("UPDATE requests SET title = ?, description = ?, category_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?");
                $stmt->execute([$title, $desc, $_POST['category_id'], $id, $userId]);
            }
            header("Location: index.php");
            exit;
        }
    }
    if (isset($_POST['delete'])) {
        if ($is_admin) {
            $stmt = $db->prepare("DELETE FROM requests WHERE id = ?");
            $stmt->execute([$id]);
        } else {
            $stmt = $db->prepare("DELETE FROM requests WHERE id = ? AND user_id = ?");
            $stmt->execute([$id, $userId]);
        }
        header("Location: index.php");
        exit;
    }
}

$viewReq = null;
if ($id > 0) {
    $stmt = $db->prepare("SELECT r.*, u.name as author_name, c.name as category_name FROM requests r JOIN users u ON r.user_id = u.id LEFT JOIN categories c ON r.category_id = c.id WHERE r.id = ?");
    $stmt->execute([$id]);
    $viewReq = $stmt->fetch();
    if ($viewReq) {
        $viewReq['can_edit'] = ($is_auth && ($is_admin || $viewReq['user_id'] == $userId));
    }
}

$requests = $db->query("SELECT r.*, u.name as author_name, c.name as category_name FROM requests r JOIN users u ON r.user_id = u.id LEFT JOIN categories c ON r.category_id = c.id WHERE r.status = 'active' ORDER BY r.id DESC")->fetchAll();

$userName = $_SESSION['user_name'] ?? '';
$initial = mb_substr($userName, 0, 1);
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Заявки — Колледж.Банк</title>
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
        .container { max-width: 800px; margin: 30px auto; }
        .card { background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .badge { background: #e1f5fe; color: #0288d1; padding: 3px 8px; border-radius: 12px; font-size: 12px; }
        .btn { background: #3498db; color: #fff; text-decoration: none; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; display: inline-block; font-size: 14px; }
        .btn-del { background: #e74c3c; }
        .btn-edit { background: #f39c12; }
        .btn-toggle { background: #2ecc71; }
        .form-group { margin-bottom: 15px; }
        input, textarea, select { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-family: sans-serif; }
        .create-form { display: none; background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #2ecc71; }
        .create-form.active { display: block; }
        .full-card { background: #fff; padding: 30px; border-radius: 8px; }
        .meta { color: #777; font-size: 14px; margin-bottom: 20px; }
        .back { color: #3498db; text-decoration: none; display: inline-block; margin-bottom: 20px; }
        .desc-preview { color: #444; font-size: 15px; line-height: 1.5; margin: 10px 0; }
        .author-info { font-size: 12px; color: #777; margin-bottom: 15px; }
        .error-msg { color: #e74c3c; background: #fadbd8; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
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
        <?php if ($error) echo "<div class='error-msg'>$error</div>"; ?>

        <?php if ($action === 'view' && $viewReq): ?>
            <a href="index.php" class="back">← Назад</a>
            <div class="full-card">
                <h1><?= htmlspecialchars($viewReq['title']) ?></h1>
                <p class="meta">Категория: <span class="badge"><?= htmlspecialchars($viewReq['category_name'] ?? 'Нет') ?></span> | Автор: <b><?= htmlspecialchars($viewReq['author_name']) ?></b></p>
                <h3>Описание</h3>
                <div style="font-size: 16px; line-height: 1.6; color: #333;">
                    <?= nl2br(htmlspecialchars($viewReq['description'])) ?>
                </div>
                <?php if ($viewReq['can_edit']): ?>
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                        <a href="index.php?action=edit&id=<?= $viewReq['id'] ?>" class="btn btn-edit">Редактировать</a>
                        <a href="index.php?action=delete&id=<?= $viewReq['id'] ?>" class="btn btn-del">Удалить</a>
                    </div>
                <?php endif; ?>
            </div>

        <?php elseif ($action === 'edit' && $viewReq && $viewReq['can_edit']): ?>
            <div class="card">
                <h2>Редактировать</h2>
                <form method="POST">
                    <div class="form-group"><input type="text" name="title" value="<?= htmlspecialchars($viewReq['title']) ?>" required></div>
                    <div class="form-group">
                        <select name="category_id" required>
                            <?php foreach ($categories as $cat): ?>
                                <option value="<?= $cat['id'] ?>" <?= $cat['id'] == $viewReq['category_id'] ? 'selected' : '' ?>><?= htmlspecialchars($cat['name']) ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <div class="form-group"><textarea name="description" rows="5" required><?= htmlspecialchars($viewReq['description']) ?></textarea></div>
                    <button type="submit" name="update" class="btn">Сохранить</button>
                    <a href="index.php" class="btn" style="background:#95a5a6;">Отмена</a>
                </form>
            </div>

        <?php elseif ($action === 'delete' && $viewReq && $viewReq['can_edit']): ?>
            <div class="card" style="text-align: center;">
                <h2>Удалить?</h2>
                <p>Вы уверены, что хотите удалить "<?= htmlspecialchars($viewReq['title']) ?>"?</p>
                <form method="POST">
                    <button type="submit" name="delete" class="btn btn-del">Да</button>
                    <a href="index.php" class="btn" style="background:#95a5a6;">Нет</a>
                </form>
            </div>

        <?php else: ?>
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                <h2>Заявки</h2>
                <?php if ($is_auth): ?>
                    <button class="btn btn-toggle" onclick="document.getElementById('createForm').classList.toggle('active')">+ Создать</button>
                <?php endif; ?>
            </div>

            <?php if ($is_auth): ?>
                <div id="createForm" class="create-form">
                    <form method="POST">
                        <div class="form-group"><input type="text" name="title" placeholder="Заголовок (кратко)" required></div>
                        <div class="form-group">
                            <select name="category_id" required>
                                <option value="">Категория</option>
                                <?php foreach ($categories as $cat): ?>
                                    <option value="<?= $cat['id'] ?>"><?= htmlspecialchars($cat['name']) ?></option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                        <div class="form-group"><textarea name="description" rows="4" placeholder="Подробное описание задачи" required></textarea></div>
                        <button type="submit" name="create" class="btn">Опубликовать</button>
                    </form>
                </div>
            <?php endif; ?>

            <?php foreach ($requests as $req): ?>
                <div class="card">
                    <h3 style="margin-top: 0;"><a href="index.php?action=view&id=<?= $req['id'] ?>" style="color: #2c3e50; text-decoration: none;"><?= htmlspecialchars($req['title']) ?></a></h3>
                    <p style="margin-bottom: 10px;"><span class="badge"><?= htmlspecialchars($req['category_name'] ?? 'Без категории') ?></span></p>
                    <div class="desc-preview"><?= htmlspecialchars(mb_substr($req['description'], 0, 100)) ?>...</div>
                    <p class="author-info">Автор: <?= htmlspecialchars($req['author_name']) ?></p>
                    <a href="index.php?action=view&id=<?= $req['id'] ?>" class="btn">Подробнее</a>
                    <?php if ($is_auth && ($is_admin || $req['user_id'] == $userId)): ?>
                        <a href="index.php?action=edit&id=<?= $req['id'] ?>" class="btn btn-edit">Ред.</a>
                        <a href="index.php?action=delete&id=<?= $req['id'] ?>" class="btn btn-del">Удал.</a>
                    <?php endif; ?>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>
    </div>
</body>
</html>