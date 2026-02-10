import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle
from cnn_utils import create_cnn_model
from utils.db import get_db_connection

def train_model():
    print("[INFO] Memulai proses ekstraksi data dari database...")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Ambil data asli dari database
    cursor.execute("SELECT perihal_suratmasuk, disposisi1 FROM tb_suratmasuk WHERE disposisi1 != ''")
    records = cursor.fetchall()
    
    texts = [r['perihal_suratmasuk'] for r in records]
    labels = [r['disposisi1'] for r in records]
    
    # 2. Dataset Expansion (Data Sintetis untuk Akademis/Demo)
    # Menambahkan variasi teks untuk memperkuat akurasi model
    synthetic_data = [
        ("Undangan Rapat Koordinasi Kecamatan", "CAMAT"),
        ("Permohonan Izin Keramaian Lingkungan", "KESRA"),
        ("Laporan Bulanan Keuangan Operasional", "KASUBAG PROGRAM DAN KEUANGAN"),
        ("Surat Mutasi Pegawai Negeri Sipil", "KASUBAG UMUM DAN KEPEGAWAIAN"),
        ("Himbauan Kebersihan dan Kerja Bakti", "TU"),
        ("Pengantar Pindah Domisili Penduduk", "KASI PEMERINTAHAN"),
        ("Permohonan Bantuan Sosial Masyarakat", "KESRA"),
        ("Koordinasi Proyek Infrastruktur Desa", "KASI PEMBANGUNAN"),
        ("Rencana Kerja Tahunan Kecamatan", "CAMAT"),
        ("Monitoring Dana Desa tahap satu", "KASI PEMBANGUNAN"),
        ("Verifikasi Data Kependudukan Sipil", "KASI PEMERINTAHAN"),
        ("Undangan Sosialisasi Pajak Daerah", "UMUM"),
        ("Evaluasi Kinerja Staf Kecamatan", "KASUBAG UMUM DAN KEPEGAWAIAN"),
        ("Laporan Realisasi Anggaran Triwulan", "KASUBAG PROGRAM DAN KEUANGAN"),
        ("Surat Perintah Tugas Lapangan", "SEKDA")
    ]
    
    for text, label in synthetic_data:
        texts.append(text)
        labels.append(label)

    print(f"[INFO] Total dataset: {len(texts)} sampel.")

    # 3. Preprocessing
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)
    vocab_size = len(tokenizer.word_index) + 1
    
    sequences = tokenizer.texts_to_sequences(texts)
    max_length = 50
    X = pad_sequences(sequences, maxlen=max_length, padding='post')
    
    label_encoder = LabelEncoder()
    y = label_encoder.fit_on_texts(labels)
    y_encoded = label_encoder.transform(labels)
    num_classes = len(label_encoder.classes_)

    # 4. Build & Train Model
    print("[INFO] Membangun arsitektur CNN...")
    model = create_cnn_model(vocab_size, num_classes, max_length)
    
    print("[INFO] Melatih model (Training)...")
    # Menggunakan epochs lebih banyak untuk dataset kecil agar stabil
    model.fit(X, y_encoded, epochs=50, verbose=1)

    # 5. Simpan Model dan Resource
    print("[INFO] Menyimpan model dan metadata...")
    model.save('letter_cnn_model.h5')
    
    tokenizer_json = tokenizer.to_json()
    with open('tokenizer.json', 'w') as f:
        f.write(tokenizer_json)
        
    with pickle.dump(label_encoder, open('label_encoder.pkl', 'wb')):
        pass # Using file handle directly in pickle.dump
    
    # Correct pickle save
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)

    print("[SUCCESS] Model CNN berhasil dilatih dan disimpan.")

if __name__ == "__main__":
    train_model()
