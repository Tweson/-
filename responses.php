<?php
require 'db.php';

if (!is_logged_in()) {
    header("Location: login.php");
    exit;
}

$userId = $_SESSION['user_id'];
$error = '';
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $offer_id = (int)$_POST['offer_id'];

    if (isset($_POST['accept']) || isset($_POST['reject'])) {
        $new_status = isset($_POST['accept']) ? 'accepted' : 'rejected';
        $stmt = $db->prepare("UPDATE offers SET status = ? WHERE id = ? AND receiver_id = ? AND status = 'pending'");
        $stmt->execute([$new_status, $offer_id, $userId]);
        if ($stmt->rowCount() > 0) {
            $success = "Статус отклика обновлен.";
        } else {
            $error = "Ошибка: нет прав или отклик уже обработан.";
        }
    }
    if (isset($_POST['cancel'])) {
        $stmt = $db->prepare("UPDATE offers SET status = 'cancelled' WHERE id = ? AND sender_id = ? AND status = 'pending'");
        $stmt->execute([$offer_id, $userId]);
        if ($stmt->rowCount() > 0) {
            $success = "Отклик отменен.";
        } else {
            $error = "Ошибка: нет прав или отклик уже обработан.";
        }
    }
}

$stmt_in = $db->prepare("
    SELECT o.*, r.title AS req_title, u.name AS sender_name 
    FROM offers o 
    JOIN requests r ON o.request_id = r.id 
    JOIN users u ON o.sender_id = u.id 
    WHERE o.receiver_id = ? 
    ORDER BY o.id DESC
");
$stmt_in->execute([$userId]);
$incoming = $stmt_in->fetchAll();

$stmt_out = $db->prepare("
    SELECT o.*, r.title AS req_title, u.name AS receiver_name 
    FROM offers o 
    JOIN requests r ON o.request_id = r.id 
    JOIN users u ON o.receiver_id = u.id 
    WHERE o.sender_id = ? 
    ORDER BY o.id DESC
");
$stmt_out->execute([$userId]);
$outgoing = $stmt_out->fetchAll();

$userName = $_SESSION['user_name'] ?? '';
$initial = $userName !== '' ? strtoupper(substr($userName, 0, 1)) : '';
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Мои отклики — Колледж.Банк</title>
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
        .container { max-width: 900px; margin: 30px auto; }
        .card { background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .btn { background: #3498db; color: #fff; text-decoration: none; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 13px; }
        .btn-green { background: #2ecc71; }
        .btn-red { background: #e74c3c; }
        .btn-grey { background: #95a5a6; }
        .status { font-weight: bold; padding: 3px 8px; border-radius: 4px; color: #fff; font-size: 12px; }
        .status-pending { background: #f39c12; }
        .status-accepted { background: #2ecc71; }
        .status-rejected { background: #e74c3c; }
        .status-cancelled { background: #95a5a6; }
        .error-msg { color: #e74c3c; background: #fadbd8; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
        .success-msg { color: #27ae60; background: #eafaf1; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
        h2 { border-bottom: 2px solid #ddd; padding-bottom: 10px; margin-top: 30px; }
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
        <?php if ($success) echo "<div class='success-msg'>$success</div>"; ?>

        <h2>Входящие (отклики на мои заявки)</h2>
        <?php if (empty($incoming)): ?>
            <p style="color: #777;">Вам пока никто не откликался.</p>
        <?php else: ?>
            <?php foreach ($incoming as $offer): ?>
                <div class="card">
                    <p><b>Заявка:</b> <?= htmlspecialchars($offer['req_title']) ?></p>
                    <p><b>От кого:</b> <?= htmlspecialchars($offer['sender_name']) ?></p>
                    <p><b>Сообщение:</b> <?= nl2br(htmlspecialchars($offer['message'])) ?></p>
                    <p>Статус: <span class="status status-<?= $offer['status'] ?>"><?= $offer['status'] ?></span></p>
                    
                    <?php if ($offer['status'] === 'pending'): ?>
                        <form method="POST" style="margin-top: 10px;">
                            <input type="hidden" name="offer_id" value="<?= $offer['id'] ?>">
                            <button type="submit" name="accept" class="btn btn-green">Принять (Accept)</button>
                            <button type="submit" name="reject" class="btn btn-red">Отклонить (Reject)</button>
                        </form>
                    <?php endif; ?>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>

        <h2>Исходящие (мои отклики)</h2>
        <?php if (empty($outgoing)): ?>
            <p style="color: #777;">Вы пока не откликались на чужие заявки.</p>
        <?php else: ?>
            <?php foreach ($outgoing as $offer): ?>
                <div class="card">
                    <p><b>Заявка:</b> <?= htmlspecialchars($offer['req_title']) ?></p>
                    <p><b>Кому:</b> <?= htmlspecialchars($offer['receiver_name']) ?></p>
                    <p><b>Ваше сообщение:</b> <?= nl2br(htmlspecialchars($offer['message'])) ?></p>
                    <p>Статус: <span class="status status-<?= $offer['status'] ?>"><?= $offer['status'] ?></span></p>
                    
                    <?php if ($offer['status'] === 'pending'): ?>
                        <form method="POST" style="margin-top: 10px;">
                            <input type="hidden" name="offer_id" value="<?= $offer['id'] ?>">
                            <button type="submit" name="cancel" class="btn btn-grey" onclick="return confirm('Отменить отклик?')">Отменить (Cancel)</button>
                        </form>
                    <?php endif; ?>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>
    </div>
</body>
</html>