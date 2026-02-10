<?php
/**
 * KATEGORI SURAT - 5 Jenis Surat
 * Naive Bayes Classification System
 */
session_start();
include "../koneksi/ceksession.php";
include "../koneksi/koneksi.php";
include "lib/CategoryMapper.php";
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>5 Kategori Surat - Naive Bayes</title>
    <link href="../assets/vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="../assets/vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
    <style>
        body { background: #f5f5f5; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center; }
        .header h1 { margin: 0; font-size: 32px; }
        .header p { margin: 10px 0 0 0; font-size: 16px; opacity: 0.9; }
        .category-card { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #667eea; }
        .category-header { display: flex; align-items: center; margin-bottom: 15px; }
        .category-label { background: #667eea; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; margin-right: 15px; }
        .category-label.se { background: #4CAF50; }
        .category-label.sk { background: #2196F3; }
        .category-label.sp { background: #FF9800; }
        .category-label.st { background: #F44336; }
        .category-label.su { background: #9C27B0; }
        .category-title { font-size: 22px; font-weight: bold; color: #333; }
        .category-desc { color: #666; font-size: 14px; line-height: 1.6; margin: 10px 0; }
        .examples { background: #f9f9f9; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .examples h5 { color: #333; margin-bottom: 10px; }
        .examples ul { margin: 0; padding-left: 20px; }
        .examples li { margin: 5px 0; color: #555; }
        .summary-table { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-top: 30px; }
        .summary-table table { width: 100%; border-collapse: collapse; }
        .summary-table th { background: #667eea; color: white; padding: 12px; text-align: left; }
        .summary-table td { padding: 12px; border-bottom: 1px solid #ddd; }
        .summary-table tr:hover { background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>📋 5 Kategori Surat</h1>
            <p>Sistem Klasifikasi Otomatis menggunakan Naive Bayes Algorithm</p>
        </div>

        <!-- KATEGORI 1 -->
        <div class="category-card">
            <div class="category-header">
                <div class="category-label se">SE</div>
                <div>
                    <div class="category-title">Surat Edaran (SE)</div>
                    <div class="category-desc">Label Numerik: <strong>1</strong></div>
                </div>
            </div>
            <p class="category-desc">
                Surat yang berisi pemberitahuan, informasi, atau instruksi yang ditujukan kepada pihak lain secara umum untuk diberitahukan mengenai suatu hal penting.
            </p>
            <div class="examples">
                <h5><i class="fa fa-lightbulb-o"></i> Contoh Perihal:</h5>
                <ul>
                    <li>Pemberitahuan perubahan jam kerja kantor</li>
                    <li>Informasi hari libur nasional</li>
                    <li>Pengumuman pelaksanaan rapat kerja</li>
                    <li>Pemberitahuan penyelenggaraan kegiatan</li>
                    <li>Edaran kebijakan baru</li>
                </ul>
            </div>
        </div>

        <!-- KATEGORI 2 -->
        <div class="category-card">
            <div class="category-header">
                <div class="category-label sk">SK</div>
                <div>
                    <div class="category-title">Surat Keputusan (SK)</div>
                    <div class="category-desc">Label Numerik: <strong>2</strong></div>
                </div>
            </div>
            <p class="category-desc">
                Surat resmi yang memuat keputusan atau penetapan dari pimpinan atau otoritas yang berwenang, biasanya mengikat dan harus dilaksanakan.
            </p>
            <div class="examples">
                <h5><i class="fa fa-gavel"></i> Contoh Perihal:</h5>
                <ul>
                    <li>Keputusan pengangkatan jabatan</li>
                    <li>Keputusan pemberian tunjangan kinerja</li>
                    <li>Penetapan penerima bantuan sosial</li>
                    <li>Keputusan penghentian kontrak</li>
                    <li>Penetapan kuota distribusi</li>
                </ul>
            </div>
        </div>

        <!-- KATEGORI 3 -->
        <div class="category-card">
            <div class="category-header">
                <div class="category-label sp">SP</div>
                <div>
                    <div class="category-title">Surat Permohonan (SP)</div>
                    <div class="category-desc">Label Numerik: <strong>3</strong></div>
                </div>
            </div>
            <p class="category-desc">
                Surat yang berisi permintaan atau permohonan dari satu pihak kepada pihak lain untuk mendapatkan sesuatu yang diinginkan atau dibutuhkan.
            </p>
            <div class="examples">
                <h5><i class="fa fa-hand-paper-o"></i> Contoh Perihal:</h5>
                <ul>
                    <li>Permohonan izin cuti</li>
                    <li>Permintaan data dan informasi</li>
                    <li>Permohonan surat keterangan</li>
                    <li>Permintaan bantuan teknis</li>
                    <li>Permohonan dukungan anggaran</li>
                </ul>
            </div>
        </div>

        <!-- KATEGORI 4 -->
        <div class="category-card">
            <div class="category-header">
                <div class="category-label st">ST</div>
                <div>
                    <div class="category-title">Surat Tugas (ST)</div>
                    <div class="category-desc">Label Numerik: <strong>4</strong></div>
                </div>
            </div>
            <p class="category-desc">
                Surat yang berisi penugasan atau perintah dari pimpinan kepada pegawai atau tim untuk melaksanakan tugas atau pekerjaan tertentu.
            </p>
            <div class="examples">
                <h5><i class="fa fa-briefcase"></i> Contoh Perihal:</h5>
                <ul>
                    <li>Penugasan mengikuti pelatihan</li>
                    <li>Penugasan perjalanan dinas</li>
                    <li>Tugas investigasi atau audit</li>
                    <li>Penugasan menjadi panitia</li>
                    <li>Tugas verifikasi lapangan</li>
                </ul>
            </div>
        </div>

        <!-- KATEGORI 5 -->
        <div class="category-card">
            <div class="category-header">
                <div class="category-label su">SU</div>
                <div>
                    <div class="category-title">Surat Undangan (SU)</div>
                    <div class="category-desc">Label Numerik: <strong>5</strong></div>
                </div>
            </div>
            <p class="category-desc">
                Surat yang berisi ajakan atau undangan kepada pihak lain untuk menghadiri atau berpartisipasi dalam suatu acara atau kegiatan tertentu.
            </p>
            <div class="examples">
                <h5><i class="fa fa-calendar"></i> Contoh Perihal:</h5>
                <ul>
                    <li>Undangan menghadiri rapat strategis</li>
                    <li>Undangan seminar/workshop</li>
                    <li>Undangan acara penutupan program</li>
                    <li>Undangan launching produk</li>
                    <li>Undangan kegiatan koordinasi</li>
                </ul>
            </div>
        </div>

        <!-- SUMMARY TABLE -->
        <div class="summary-table">
            <h3>📊 Ringkasan 5 Kategori Surat</h3>
            <table>
                <thead>
                    <tr>
                        <th style="width: 50px;">No</th>
                        <th style="width: 80px;">Kode</th>
                        <th>Nama Kategori</th>
                        <th style="width: 200px;">Deskripsi Singkat</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>1</strong></td>
                        <td><span class="badge" style="background: #4CAF50;">SE</span></td>
                        <td><strong>Surat Edaran</strong></td>
                        <td>Pemberitahuan & Informasi umum</td>
                    </tr>
                    <tr>
                        <td><strong>2</strong></td>
                        <td><span class="badge" style="background: #2196F3;">SK</span></td>
                        <td><strong>Surat Keputusan</strong></td>
                        <td>Keputusan resmi yang mengikat</td>
                    </tr>
                    <tr>
                        <td><strong>3</strong></td>
                        <td><span class="badge" style="background: #FF9800;">SP</span></td>
                        <td><strong>Surat Permohonan</strong></td>
                        <td>Permintaan atau permohonan</td>
                    </tr>
                    <tr>
                        <td><strong>4</strong></td>
                        <td><span class="badge" style="background: #F44336;">ST</span></td>
                        <td><strong>Surat Tugas</strong></td>
                        <td>Penugasan & perintah kerja</td>
                    </tr>
                    <tr>
                        <td><strong>5</strong></td>
                        <td><span class="badge" style="background: #9C27B0;">SU</span></td>
                        <td><strong>Surat Undangan</strong></td>
                        <td>Ajakan atau undangan acara</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- INFO BOX -->
        <div style="background: #d1ecf1; border: 1px solid #bee5eb; border-radius: 5px; padding: 15px; margin-top: 30px; color: #0c5460;">
            <h4><i class="fa fa-info-circle"></i> Cara Kerja Sistem Klasifikasi</h4>
            <p style="margin-bottom: 10px;">
                Sistem Naive Bayes akan <strong>otomatis memprediksi kategori</strong> surat berdasarkan:
            </p>
            <ul style="margin: 0; padding-left: 20px;">
                <li><strong>Perihal Surat</strong> - Kata-kata yang digunakan dalam perihal</li>
                <li><strong>Pola Historis</strong> - Kesamaan dengan surat masa lalu</li>
                <li><strong>Probabilitas</strong> - Perhitungan tingkat kepercayaan</li>
            </ul>
            <p style="margin: 10px 0 0 0; font-size: 13px;">
                ✓ Admin tetap dapat <strong>memperbaiki atau mengubah kategori</strong> jika prediksi sistem tidak akurat.
            </p>
        </div>

        <!-- FOOTER -->
        <div style="text-align: center; margin-top: 30px; padding: 20px; color: #666; border-top: 1px solid #ddd;">
            <p>Sistem Klasifikasi Surat Otomatis | Naive Bayes Algorithm</p>
            <p style="font-size: 12px;">5 Kategori Terstandar untuk Pengarsipan Surat</p>
        </div>
    </div>

    <script src="../assets/vendors/jquery/dist/jquery.min.js"></script>
    <script src="../assets/vendors/bootstrap/dist/js/bootstrap.min.js"></script>
</body>
</html>
