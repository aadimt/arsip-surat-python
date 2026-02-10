import mysql.connector
import random
from datetime import datetime, timedelta
from config import Config

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )

def random_date(start_year=2024, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# Valid departments from tb_bagian
departments = [
    "CAMAT", "Plt. SEKRETARIS KECAMATAN", "KASUBAG PROGRAM DAN KEUANGAN",
    "KASUBAG UMUM DAN KEPEGAWAIAN", "KASI PEMERINTAHAN", "KASI PEMBERDAYAAN MASYARAKAT",
    "KASI PEMBANGUNAN", "KASI SOSIAL BUDAYA", "KASI KETENTRAMAN DAN KETERTIBAN UMUM",
    "ARSIPARIS TERAMPIL"
]

subjects = [
    "Undangan Rapat Koordinasi", "Permohonan Izin Kegiatan", "Pemberitahuan Pelaksanaan Fogging",
    "Laporan Triwulan Pemberdayaan Masyarakat", "Surat Pengantar Pindah Domisili",
    "Pemberitahuan Bantuan Sosial", "Koordinasi Pembangunan Infrastruktur Desa",
    "Evaluasi Kinerja Pegawai", "Surat Teguran Kedisiplinan", "Monitoring Dana Desa 2024",
    "Rencana Kerja Anggaran 2025", "Undangan Sosialisasi Pajak Daerah",
    "Himbauan Kebersihan Lingkungan", "Surat Penugasan Petugas Lapangan",
    "Permintaan Data Kependudukan", "Laporan Hasil Pemeriksaan", "Surat Keputusan Camat",
    "Berita Acara Serah Terima Jabatan", "Konfirmasi Kehadiran Seminar",
    "Pemberitahuan Jadwal Monitoring", "Surat Mandat Delegasi Kecamatan"
]

senders_receivers = [
    "Dinas Kesehatan Kabupaten", "Dinas Pendidikan", "Bappeda Kabupaten",
    "Kementerian Dalam Negeri", "Sekretariat Daerah", "Perusahaan Listrik Negara",
    "Bank Pembangunan Daerah", "Polres Kabupaten", "Kodim Kabupaten",
    "Kepala Desa Sukamaju", "Kepala Desa Mekarsari", "Lurah Karang Tengah",
    "Balai Besar Wilayah Sungai", "Kantor Pajak Pratama", "BPJS Kesehatan"
]

def generate_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    print("Generating 35 records for tb_suratmasuk...")
    for i in range(35):
        dt_masuk = random_date()
        dt_surat = dt_masuk - timedelta(days=random.randint(2, 7))
        kode = random.choice(["KM", "SK", "INV", "PRT"])
        no_urut = f"{800 + i}"
        no_surat = f"{random.randint(100, 999)}/{kode}/X/{dt_surat.year}"
        pengirim = random.choice(senders_receivers)
        kepada = "Camat"
        perihal = random.choice(subjects)
        disposisi = random.choice(departments)
        
        sql = """INSERT INTO tb_suratmasuk (tanggalmasuk_suratmasuk, kode_suratmasuk, nomorurut_suratmasuk, 
                 nomor_suratmasuk, tanggalsurat_suratmasuk, pengirim, kepada_suratmasuk, perihal_suratmasuk, 
                 file_suratmasuk, operator, disposisi1) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (dt_masuk, kode, no_urut, no_surat, dt_surat.date(), pengirim, kepada, perihal, "dummy_masuk.pdf", "Admin", disposisi)
        try:
            cursor.execute(sql, val)
        except Exception as e:
            print(f"Error Masuk {i}: {e}")

    print("Generating 35 records for tb_suratkeluar...")
    for i in range(35):
        dt_keluar = random_date()
        dt_surat = dt_keluar - timedelta(days=random.randint(0, 3))
        kode = random.choice(["001", "440", "800", "900"])
        no_surat = f"{kode}/{random.randint(100, 999)}/ Kec.Slt/{dt_surat.year}"
        no_urut = f"{900 + i}"
        bagian = random.choice(departments)
        kepada = random.choice(senders_receivers)
        perihal = random.choice(subjects)
        
        sql = """INSERT INTO tb_suratkeluar (tanggalkeluar_suratkeluar, kode_suratkeluar, nomor_suratkeluar, 
                 nomorurut_suratkeluar, nama_bagian, tanggalsurat_suratkeluar, kepada_suratkeluar, 
                 perihal_suratkeluar, file_suratkeluar, operator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (dt_keluar, kode, no_surat, no_urut, bagian, dt_surat.date(), kepada, perihal, "dummy_keluar.pdf", "Admin")
        try:
            cursor.execute(sql, val)
        except Exception as e:
            print(f"Error Keluar {i}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("Dummy data generation completed successfully!")

if __name__ == "__main__":
    generate_data()
