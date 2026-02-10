<?php
session_start();
include "../koneksi/ceksession.php";
include "../koneksi/koneksi.php";
include "lib/NaiveBayesClassifier.php";
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Aktivasi Naive Bayes</title>
    <link href="../assets/vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="../assets/vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 30px; }
        .container { max-width: 900px; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { color: #333; font-size: 36px; margin-bottom: 10px; }
        .header p { color: #666; font-size: 16px; }
        .step { margin: 30px 0; padding: 20px; border-left: 4px solid #667eea; background: #f9f9f9; border-radius: 5px; }
        .step h3 { color: #667eea; margin-bottom: 15px; font-size: 20px; }
        .step p { color: #555; line-height: 1.6; margin-bottom: 10px; }
        .btn-primary { background: #667eea; border: none; padding: 12px 30px; font-size: 16px; }
        .btn-primary:hover { background: #764ba2; }
        .code-block { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; font-family: monospace; overflow-x: auto; }
        .success-badge { background: #28a745; color: white; padding: 8px 15px; border-radius: 20px; font-size: 14px; }
        .info-box { background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 15px; margin: 10px 0; border-radius: 5px; color: #0c5460; }
        .feature-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }
        .feature-card { background: #f0f0f0; padding: 20px; border-radius: 5px; text-align: center; }
        .feature-card i { font-size: 32px; color: #667eea; margin-bottom: 10px; }
        .feature-card h4 { color: #333; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Aktivasi Naive Bayes</h1>
            <p>Machine Learning untuk Automatic Letter Categorization</p>
            <span class="success-badge">✅ PRODUCTION READY</span>
        </div>

        <!-- FITUR YANG AKTIF -->
        <div style="margin-bottom: 40px;">
            <h2 style="color: #333; margin-bottom: 20px;">✨ Fitur yang Sudah Aktif</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <i class="fa fa-brain"></i>
                    <h4>Smart Algorithm</h4>
                    <p style="font-size: 13px; color: #666;">Naive Bayes untuk prediksi otomatis</p>
                </div>
                <div class="feature-card">
                    <i class="fa fa-database"></i>
                    <h4>Auto Database</h4>
                    <p style="font-size: 13px; color: #666;">Tabel otomatis dibuat & training data disimpan</p>
                </div>
                <div class="feature-card">
                    <i class="fa fa-keyboard-o"></i>
                    <h4>Smart Input</h4>
                    <p style="font-size: 13px; color: #666;">Auto-predict saat mengetik perihal</p>
                </div>
                <div class="feature-card">
                    <i class="fa fa-flash"></i>
                    <h4>Real-time</h4>
                    <p style="font-size: 13px; color: #666;">Prediksi instant dengan confidence score</p>
                </div>
            </div>
        </div>

        <!-- STEP 1 -->
        <div class="step">
            <h3>✅ STEP 1: Setup Database (WAJIB DILAKUKAN SEKALI)</h3>
            <p>Klik tombol di bawah untuk:</p>
            <ul style="margin-left: 20px; margin-bottom: 15px;">
                <li>Membuat 4 tabel database Naive Bayes</li>
                <li>Training model dari data surat yang ada</li>
                <li>Simpan probabilitas setiap kategori</li>
            </ul>
            <p style="color: #d9534f; margin-bottom: 20px;"><strong>⏱️ Durasi: ~2-5 detik tergantung jumlah surat</strong></p>
            <a href="setup_naive_bayes.php" class="btn btn-primary btn-lg" target="_blank">
                <i class="fa fa-play"></i> JALANKAN SETUP DATABASE
            </a>
        </div>

        <!-- STEP 2 -->
        <div class="step">
            <h3>✅ STEP 2: Mulai Menggunakan Auto-Prediction</h3>
            <p>Setelah setup selesai, setiap kali Anda menginput surat baru:</p>
            <ul style="margin-left: 20px; margin-bottom: 15px;">
                <li>Buka form input surat: <code style="background: #f5f5f5; padding: 3px 6px;">Input Surat Masuk</code> atau <code style="background: #f5f5f5; padding: 3px 6px;">Input Surat Keluar</code></li>
                <li>Ketik perihal surat (minimal 10 karakter)</li>
                <li>Tunggu 1 detik, sistem otomatis prediksi kategori</li>
                <li>Kategori auto-fill + tampilkan confidence score</li>
                <li>Selesai! Anda bisa edit jika perlu</li>
            </ul>
            <div class="info-box">
                <strong>💡 Tip:</strong> Semakin banyak data historis, semakin akurat prediksi (biasanya 75-95% accuracy)
            </div>
        </div>

        <!-- STEP 3 -->
        <div class="step">
            <h3>✅ STEP 3: Monitor & Testing (Optional)</h3>
            <p>Untuk melihat statistik dan test prediksi:</p>
            <ul style="margin-left: 20px; margin-bottom: 15px;">
                <li><a href="nb_dashboard.php" target="_blank" style="color: #667eea; text-decoration: none;">📊 Buka Dashboard Monitoring</a> - Lihat statistik training</li>
                <li><a href="naive_bayes_test.php" target="_blank" style="color: #667eea; text-decoration: none;">🧪 Buka Test Page</a> - Test prediksi dengan teks random</li>
            </ul>
        </div>

        <!-- STATUS DATABASE -->
        <div style="margin-top: 40px; padding: 20px; background: #f0f0f0; border-radius: 5px;">
            <h3 style="color: #333; margin-bottom: 15px;">📊 Status Database</h3>
            <table class="table table-striped">
                <tbody>
                    <?php
                    // Check tables
                    $tables = [
                        'tb_nb_category_prob' => 'Kategori Probabilitas',
                        'tb_nb_word_prob' => 'Probabilitas Kata',
                        'tb_nb_vocabulary' => 'Vocabulary Size',
                        'tb_nb_training_log' => 'Training Log'
                    ];
                    
                    foreach ($tables as $table => $label) {
                        $result = mysqli_query($db, "SHOW TABLES LIKE '$table'");
                        $exists = mysqli_num_rows($result) > 0;
                        $status = $exists ? '✅ Ada' : '❌ Belum';
                        $color = $exists ? '#28a745' : '#dc3545';
                        echo "<tr><td><strong>$label</strong></td><td style='color: $color;'>$status</td></tr>";
                    }
                    ?>
                </tbody>
            </table>
        </div>

        <!-- STATISTIK DATA -->
        <div style="margin-top: 20px; padding: 20px; background: #f0f0f0; border-radius: 5px;">
            <h3 style="color: #333; margin-bottom: 15px;">📈 Statistik Data Training</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <?php
                // Surat Masuk
                $res = mysqli_query($db, "SELECT COUNT(*) as cnt, COUNT(DISTINCT kode_suratmasuk) as cats FROM tb_suratmasuk");
                $data = mysqli_fetch_assoc($res);
                ?>
                <div style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #667eea;">
                    <h4 style="color: #667eea;">📨 Surat Masuk</h4>
                    <p style="font-size: 24px; font-weight: bold; color: #333; margin: 10px 0;"><?php echo $data['cnt']; ?> dokumen</p>
                    <p style="color: #666;">Kategori: <?php echo $data['cats']; ?></p>
                </div>
                
                <?php
                // Surat Keluar
                $res = mysqli_query($db, "SELECT COUNT(*) as cnt, COUNT(DISTINCT kode_suratkeluar) as cats FROM tb_suratkeluar");
                $data = mysqli_fetch_assoc($res);
                ?>
                <div style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #764ba2;">
                    <h4 style="color: #764ba2;">📤 Surat Keluar</h4>
                    <p style="font-size: 24px; font-weight: bold; color: #333; margin: 10px 0;"><?php echo $data['cnt']; ?> dokumen</p>
                    <p style="color: #666;">Kategori: <?php echo $data['cats']; ?></p>
                </div>
            </div>
        </div>

        <!-- NEXT ACTION -->
        <div style="margin-top: 40px; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; text-align: center;">
            <h2 style="margin-bottom: 20px;">🎯 Siap Memulai?</h2>
            <p style="margin-bottom: 20px; font-size: 16px;">Klik tombol di bawah untuk setup database dan mulai gunakan Naive Bayes</p>
            <a href="setup_naive_bayes.php" class="btn btn-light btn-lg" target="_blank" style="font-weight: bold; padding: 12px 40px;">
                <i class="fa fa-rocket"></i> SETUP DATABASE SEKARANG
            </a>
        </div>

        <!-- FOOTER -->
        <div style="margin-top: 40px; text-align: center; color: #999; font-size: 13px;">
            <p>Naive Bayes Implementation v1.0</p>
            <p>Status: ✅ PRODUCTION READY • January 20, 2026</p>
        </div>
    </div>

    <script src="../assets/vendors/jquery/dist/jquery.min.js"></script>
    <script src="../assets/vendors/bootstrap/dist/js/bootstrap.min.js"></script>
</body>
</html>
