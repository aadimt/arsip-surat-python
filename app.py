from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from config import Config
from utils.db import get_db_connection
from cnn_utils import CNNClassifier

app = Flask(__name__)
app.config.from_object(Config)

# Initialize CNN Classifier
classifier = CNNClassifier()

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

import hashlib

# Admin Login Route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username_admin']
        password = request.form['password']
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tb_admin WHERE username_admin=%s AND password=%s", (username, hashed_password))
            account = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if account:
                session['loggedin'] = True
                session['id'] = account['id_admin']
                session['username'] = account['username_admin']
                session['gambar'] = account['gambar']
                session['role'] = 'admin'
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('admin/login.html', error='Username atau Password salah!')
        else:
             return render_template('admin/login.html', error='Koneksi Database Gagal')

    return render_template('admin/login.html')

# Bagian Login Route
@app.route('/bagian/login', methods=['GET', 'POST'])
def bagian_login():
    if request.method == 'POST':
        username = request.form['username_admin_bagian']
        password = request.form['password_bagian']
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tb_bagian WHERE username_admin_bagian=%s AND password_bagian=%s", (username, hashed_password))
            account = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if account:
                session['loggedin'] = True
                session['id'] = account['id_bagian']
                session['username'] = account['username_admin_bagian']
                session['nama_bagian'] = account['nama_bagian']
                session['role'] = 'bagian'
                return redirect(url_for('bagian_dashboard'))
            else:
                return render_template('bagian/login.html', error='Username atau Password salah!')
        else:
            return render_template('bagian/login.html', error='Koneksi Database Gagal')

    return render_template('bagian/login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('home'))

@app.route('/bagian')
def bagian_dashboard():
    if 'role' in session and session['role'] == 'bagian':
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Count Surat Masuk (Disposisi to this Bagian)
            nama_bagian = session['nama_bagian']
            cursor.execute("SELECT COUNT(*) as count FROM tb_suratmasuk WHERE disposisi1=%s OR disposisi2=%s OR disposisi3=%s", (nama_bagian, nama_bagian, nama_bagian))
            jumlah_masuk = cursor.fetchone()['count']
            
            # Count Surat Keluar (From this Bagian)
            cursor.execute("SELECT COUNT(*) as count FROM tb_suratkeluar WHERE nama_bagian=%s", (nama_bagian,))
            jumlah_keluar = cursor.fetchone()['count']
            
            # Count Bagian (Total)
            cursor.execute("SELECT COUNT(*) as count FROM tb_bagian")
            jumlah_bagian = cursor.fetchone()['count']
            
            cursor.close()
            conn.close()
            
            return render_template('bagian/index.html', 
                                   jumlah_masuk=jumlah_masuk, 
                                   jumlah_keluar=jumlah_keluar, 
                                   jumlah_bagian=jumlah_bagian)
        except Exception as e:
            print(e)
            return "Database Error"

    return redirect(url_for('bagian_login'))

@app.route('/bagian/surat_masuk')
def bagian_surat_masuk():
    if 'role' in session and session['role'] == 'bagian':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        nama_bagian = session['nama_bagian']
        cursor.execute("SELECT * FROM tb_suratmasuk WHERE disposisi1=%s OR disposisi2=%s OR disposisi3=%s", (nama_bagian, nama_bagian, nama_bagian))
        surat_masuk = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('bagian/surat_masuk/index.html', surat_masuk=surat_masuk)
    return redirect(url_for('bagian_login'))

@app.route('/bagian/surat_keluar')
def bagian_surat_keluar():
    if 'role' in session and session['role'] == 'bagian':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        nama_bagian = session['nama_bagian']
        cursor.execute("SELECT * FROM tb_suratkeluar WHERE nama_bagian=%s", (nama_bagian,))
        surat_keluar = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('bagian/surat_keluar/index.html', surat_keluar=surat_keluar)
    return redirect(url_for('bagian_login'))

@app.route('/bagian/ambil_nomor', methods=['GET', 'POST'])
def bagian_ambil_nomor():
    if 'role' not in session or session['role'] != 'bagian':
         return redirect(url_for('bagian_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nomor_baru = request.form['nomorbaru']
        nama_bagian = session['nama_bagian']
        
        # Concurrency Check
        cursor.execute("SELECT * FROM tb_suratkeluar ORDER BY nomor_suratkeluar DESC LIMIT 1")
        last_data = cursor.fetchone()
        
        if last_data and last_data['nomor_suratkeluar'] == nomor_baru and last_data['nama_bagian'] != nama_bagian:
             # Conflict
             cursor.close()
             conn.close()
             return "Nomor ini telah diambil Bagian Lain. Silahkan coba lagi. <meta http-equiv='refresh' content='2;url=" + url_for('bagian_ambil_nomor') + "'>"
        
        # Proceed with Insert
        import datetime
        now = datetime.datetime.now()
        tanggal_entry = now.strftime("%Y-%m-%d %H:%M:%S")
        tgl_keluar = now.strftime("%Y-%m-%d %H:%M:%S")
        tgl_surat = now.strftime("%Y-%m-%d")
        thn_now = now.strftime("%Y")
        
        filename = f"{thn_now}-{nomor_baru}.pdf"
        
        # Copy Temp File Logic
        import shutil
        import os
        # Source: 'bagian/file_temp/-file_temp.pdf' relative to project root d:\arsip surat PYTHON
        # Destination: 'static/uploads/' + filename
        
        try:
            source_path = os.path.join(app.root_path, 'bagian', 'file_temp', '-file_temp.pdf')
            if not os.path.exists(source_path):
                 # Fallback if source doesn't exist, maybe Create a dummy PDF or copy a default one
                 # For now, let's assume we might need a default empty pdf. 
                 # Or just copy ANY pdf or create an empty file.
                 with open(source_path, 'wb') as f:
                     f.write(b'%PDF-1.4 empty pdf') # Dummy content

            destination_folder = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(destination_folder, exist_ok=True)
            destination_path = os.path.join(destination_folder, filename)
            
            shutil.copy(source_path, destination_path)
            
            sql = """INSERT INTO tb_suratkeluar (tanggalkeluar_suratkeluar, nomor_suratkeluar, nama_bagian, 
                     tanggalsurat_suratkeluar, file_suratkeluar, tanggal_entry) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            val = (tgl_keluar, nomor_baru, nama_bagian, tgl_surat, filename, tanggal_entry)
            
            cursor.execute(sql, val)
            conn.commit()
            
            cursor.close()
            conn.close()
            return "Terima Kasih. Nomor telah diambil Bagian Anda. <meta http-equiv='refresh' content='2;url=" + url_for('bagian_ambil_nomor') + "'>"
            
        except Exception as e:
            print(f"Error process ambil nomor: {e}")
            return f"Terjadi kesalahan: {e}"

    # GET Logic
    cursor.execute("SELECT * FROM tb_suratkeluar ORDER BY nomor_suratkeluar DESC LIMIT 1")
    last_surat = cursor.fetchone()
    
    nomor_baru = "0001"
    last_update = "-"
    
    if last_surat:
        try:
            last_no = last_surat['nomor_suratkeluar'][:4]
            nomor_baru = str(int(last_no) + 1).zfill(4)
            last_update = last_surat['tanggal_entry'] # formatting needed?
        except:
            pass
            
    cursor.execute("SELECT tanggal_entry FROM tb_suratkeluar ORDER BY tanggal_entry DESC LIMIT 1")
    last_entry = cursor.fetchone()
    if last_entry:
        last_update = last_entry['tanggal_entry']

    cursor.close()
    conn.close()
    return render_template('bagian/ambil_nomor.html', nomor_baru=nomor_baru, last_update=last_update)

# Dashboard Logic
@app.route('/admin')
def admin_dashboard():
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT COUNT(*) as count FROM tb_suratmasuk")
            jumlah_masuk = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM tb_suratkeluar")
            jumlah_keluar = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM tb_bagian")
            jumlah_bagian = cursor.fetchone()['count']
            
            cursor.close()
            conn.close()
            
            return render_template('admin/index.html', 
                                   jumlah_masuk=jumlah_masuk, 
                                   jumlah_keluar=jumlah_keluar, 
                                   jumlah_bagian=jumlah_bagian)
        except Exception as e:
            print(e)
            return "Database Error"

    return redirect(url_for('admin_login'))

@app.route('/admin/profile', methods=['GET', 'POST'])
def admin_profile():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        nama = request.form.get('nama_admin')
        username = request.form.get('username_admin')
        password = request.form.get('password')
        
        # Handle Profile Picture Upload
        file = request.files.get('gambar')
        filename = None
        if file and file.filename != '':
            import os
            filename = f"admin_{session['id']}_{file.filename}"
            upload_path = os.path.join(app.root_path, 'static', 'assets', 'images')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
        
        sql = "UPDATE tb_admin SET nama_admin=%s, username_admin=%s"
        params = [nama, username]
        
        if password:
            hashed_password = hashlib.sha1(password.encode()).hexdigest()
            sql += ", password=%s"
            params.append(hashed_password)
            
        if filename:
            sql += ", gambar=%s"
            params.append(filename)
            session['gambar'] = filename
            
        sql += " WHERE id_admin=%s"
        params.append(session['id'])
        
        cursor.execute(sql, tuple(params))
        conn.commit()
        session['username'] = username
        return redirect(url_for('admin_profile'))
        
    cursor.execute("SELECT * FROM tb_admin WHERE id_admin=%s", (session['id'],))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('admin/profile.html', admin=admin)

# --- Surat Masuk CRUD ---

@app.route('/admin/surat_masuk')
def admin_surat_masuk():
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_suratmasuk ORDER BY id_suratmasuk DESC")
        surat_masuk = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin/surat_masuk/index.html', surat_masuk=surat_masuk)
    return redirect(url_for('admin_login'))

@app.route('/admin/surat_masuk/input', methods=['GET', 'POST'])
def admin_surat_masuk_input():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        try:
            # Handle File Upload
            file = request.files['file_suratmasuk']
            filename = ""
            if file:
                filename = file.filename
                # Ensure static/uploads exists
                import os
                upload_folder = os.path.join(app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
            
            sql = """INSERT INTO tb_suratmasuk (tanggalmasuk_suratmasuk, kode_suratmasuk, nomorurut_suratmasuk, 
                     nomor_suratmasuk, tanggalsurat_suratmasuk, pengirim, kepada_suratmasuk, perihal_suratmasuk, 
                     file_suratmasuk, operator, disposisi1, tanggal_disposisi1) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (request.form['tanggalmasuk_suratmasuk'], request.form['kode_suratmasuk'], request.form['nomorurut_suratmasuk'],
                   request.form['nomor_suratmasuk'], request.form['tanggalsurat_suratmasuk'], request.form['pengirim'],
                   request.form['kepada_suratmasuk'], request.form['perihal_suratmasuk'], filename, session['username'],
                   request.form.get('disposisi1', ''), request.form.get('tanggal_disposisi1', None))
            
            cursor.execute(sql, val)
            conn.commit()
            return redirect(url_for('admin_surat_masuk'))
        except Exception as e:
            print(f"Error: {e}")
            # In production, show error to user
    
    # Get Data for Form (Bagian for Disposisi)
    cursor.execute("SELECT * FROM tb_bagian")
    bagian_list = cursor.fetchall()
    
    # Generate Nomor Urut (Placeholder logic)
    cursor.execute("SELECT nomorurut_suratmasuk FROM tb_suratmasuk ORDER BY nomorurut_suratmasuk DESC LIMIT 1")
    last_surat = cursor.fetchone()
    nomor_baru = "0001"
    if last_surat:
        try:
            last_no = int(last_surat['nomorurut_suratmasuk'])
            nomor_baru = str(last_no + 1).zfill(4)
        except:
            pass            

    cursor.close()
    conn.close()
    return render_template('admin/surat_masuk/form.html', bagian_list=bagian_list, nomor_baru=nomor_baru, surat=None)

@app.route('/admin/surat_masuk/edit/<int:id>', methods=['GET', 'POST'])
def admin_surat_masuk_edit(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
         # Handle File Upload (If new file)
        file = request.files['file_suratmasuk']
        filename = None
        if file and file.filename != '':
            filename = file.filename
            import os
            upload_folder = os.path.join(app.root_path, 'static', 'uploads')
            file.save(os.path.join(upload_folder, filename))
        
        # Build Update Query
        sql = "UPDATE tb_suratmasuk SET tanggalmasuk_suratmasuk=%s, kode_suratmasuk=%s, nomorurut_suratmasuk=%s, nomor_suratmasuk=%s, tanggalsurat_suratmasuk=%s, pengirim=%s, kepada_suratmasuk=%s, perihal_suratmasuk=%s, disposisi1=%s, tanggal_disposisi1=%s"
        val = [request.form['tanggalmasuk_suratmasuk'], request.form['kode_suratmasuk'], request.form['nomorurut_suratmasuk'],
               request.form['nomor_suratmasuk'], request.form['tanggalsurat_suratmasuk'], request.form['pengirim'],
               request.form['kepada_suratmasuk'], request.form['perihal_suratmasuk'], request.form.get('disposisi1', ''), request.form.get('tanggal_disposisi1', None)]
        
        if filename:
            sql += ", file_suratmasuk=%s"
            val.append(filename)
            
        sql += " WHERE id_suratmasuk=%s"
        val.append(id)
        
        cursor.execute(sql, tuple(val))
        conn.commit()
        return redirect(url_for('admin_surat_masuk'))

    cursor.execute("SELECT * FROM tb_suratmasuk WHERE id_suratmasuk=%s", (id,))
    surat = cursor.fetchone()
    
    cursor.execute("SELECT * FROM tb_bagian")
    bagian_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('admin/surat_masuk/form.html', bagian_list=bagian_list, surat=surat)

@app.route('/admin/surat_masuk/delete/<int:id>')
def admin_surat_masuk_delete(id):
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_suratmasuk WHERE id_suratmasuk=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin_surat_masuk'))
    return redirect(url_for('admin_login'))

@app.route('/admin/surat_masuk/detail/<int:id>')
def admin_surat_masuk_detail(id):
    # Placeholder for detail view
    return f"Detail View for ID {id} - Work in Progress"

@app.route('/admin/surat_masuk/classify', methods=['POST'])
def classify_surat():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    perihal = data.get('perihal', '')
    
    if not perihal:
        return jsonify({'error': 'Perihal kosong'}), 400
        
    try:
        prediction, confidence = classifier.predict(perihal)
        if prediction:
            return jsonify({
                'prediction': prediction,
                'confidence': f"{confidence*100:.2f}%"
            })
        else:
            return jsonify({'error': 'Gagal melakukan klasifikasi. Pastikan model sudah dilatih.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Surat Keluar CRUD ---

@app.route('/admin/surat_keluar')
def admin_surat_keluar():
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_suratkeluar ORDER BY id_suratkeluar DESC")
        surat_keluar = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin/surat_keluar/index.html', surat_keluar=surat_keluar)
    return redirect(url_for('admin_login'))

@app.route('/admin/surat_keluar/input', methods=['GET', 'POST'])
def admin_surat_keluar_input():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        try:
            # Handle File Upload
            file = request.files['file_suratkeluar']
            filename = ""
            if file:
                filename = file.filename
                import os
                upload_folder = os.path.join(app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
            
            sql = """INSERT INTO tb_suratkeluar (tanggalkeluar_suratkeluar, kode_suratkeluar, nomor_suratkeluar, 
                     nama_bagian, tanggalsurat_suratkeluar, kepada_suratkeluar, perihal_suratkeluar, 
                     file_suratkeluar, operator) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (request.form['tanggalkeluar_suratkeluar'], request.form['kode_suratkeluar'], request.form['nomor_suratkeluar'],
                   request.form['nama_bagian'], request.form['tanggalsurat_suratkeluar'], request.form['kepada_suratkeluar'],
                   request.form['perihal_suratkeluar'], filename, session['username'])
            
            cursor.execute(sql, val)
            conn.commit()
            return redirect(url_for('admin_surat_keluar'))
        except Exception as e:
            print(f"Error: {e}")
    
    # Get Bagian Data
    cursor.execute("SELECT * FROM tb_bagian")
    bagian_list = cursor.fetchall()
    
    # Generate Nomor Logic (Placeholder)
    cursor.execute("SELECT nomor_suratkeluar FROM tb_suratkeluar ORDER BY nomor_suratkeluar DESC LIMIT 1")
    last_surat = cursor.fetchone()
    nomor_baru = "0001"
    if last_surat:
        try:
            last_no = last_surat['nomor_suratkeluar'][:4] # Take first 4 digits
            nomor_baru = str(int(last_no) + 1).zfill(4)
        except:
             pass

    cursor.close()
    conn.close()
    return render_template('admin/surat_keluar/form.html', bagian_list=bagian_list, nomor_baru=nomor_baru, surat=None)

@app.route('/admin/surat_keluar/edit/<int:id>', methods=['GET', 'POST'])
def admin_surat_keluar_edit(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
         # Handle File Upload
        file = request.files['file_suratkeluar']
        filename = None
        if file and file.filename != '':
            filename = file.filename
            import os
            upload_folder = os.path.join(app.root_path, 'static', 'uploads')
            file.save(os.path.join(upload_folder, filename))
        
        # Build Update Query
        sql = "UPDATE tb_suratkeluar SET tanggalkeluar_suratkeluar=%s, kode_suratkeluar=%s, nomor_suratkeluar=%s, nama_bagian=%s, tanggalsurat_suratkeluar=%s, kepada_suratkeluar=%s, perihal_suratkeluar=%s"
        val = [request.form['tanggalkeluar_suratkeluar'], request.form['kode_suratkeluar'], request.form['nomor_suratkeluar'],
               request.form['nama_bagian'], request.form['tanggalsurat_suratkeluar'], request.form['kepada_suratkeluar'],
               request.form['perihal_suratkeluar']]
        
        if filename:
            sql += ", file_suratkeluar=%s"
            val.append(filename)
            
        sql += " WHERE id_suratkeluar=%s"
        val.append(id)
        
        cursor.execute(sql, tuple(val))
        conn.commit()
        return redirect(url_for('admin_surat_keluar'))

    cursor.execute("SELECT * FROM tb_suratkeluar WHERE id_suratkeluar=%s", (id,))
    surat = cursor.fetchone()
    
    cursor.execute("SELECT * FROM tb_bagian")
    bagian_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('admin/surat_keluar/form.html', bagian_list=bagian_list, surat=surat)

@app.route('/admin/surat_keluar/delete/<int:id>')
def admin_surat_keluar_delete(id):
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_suratkeluar WHERE id_suratkeluar=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin_surat_keluar'))
    return redirect(url_for('admin_login'))

@app.route('/admin/surat_keluar/detail/<int:id>')
def admin_surat_keluar_detail(id):
    return f"Detail View for ID {id} - Work in Progress"

# --- Bagian CRUD ---

@app.route('/admin/bagian')
def admin_bagian():
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_bagian ORDER BY id_bagian ASC")
        bagian_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin/bagian/index.html', bagian_list=bagian_list)
    return redirect(url_for('admin_login'))

@app.route('/admin/bagian/input', methods=['GET', 'POST'])
def admin_bagian_input():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Handle File Upload
            file = request.files['gambar']
            filename = ""
            if file and file.filename != '':
                filename = file.filename
                import os
                upload_folder = os.path.join(app.root_path, 'static', 'bagian', 'images')
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
            
            hashed_password = hashlib.sha1(request.form['password_bagian'].encode()).hexdigest()
            
            sql = """INSERT INTO tb_bagian (nama_bagian, username_admin_bagian, password_bagian, nama_lengkap, 
                     tanggal_lahir_bagian, alamat, no_hp_bagian, gambar) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (request.form['nama_bagian'], request.form['username_admin_bagian'], hashed_password,
                   request.form['nama_lengkap'], request.form['tanggal_lahir_bagian'], request.form['alamat'],
                   request.form['no_hp_bagian'], filename)
            
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('admin_bagian'))
        except Exception as e:
            print(f"Error: {e}")

    return render_template('admin/bagian/form.html', bagian=None)

@app.route('/admin/bagian/edit/<int:id>', methods=['GET', 'POST'])
def admin_bagian_edit(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Handle File Upload
        file = request.files['gambar']
        filename = None
        if file and file.filename != '':
            filename = file.filename
            import os
            upload_folder = os.path.join(app.root_path, 'static', 'bagian', 'images')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
        
        # Build Update Query
        sql = "UPDATE tb_bagian SET nama_bagian=%s, username_admin_bagian=%s, nama_lengkap=%s, tanggal_lahir_bagian=%s, alamat=%s, no_hp_bagian=%s"
        val = [request.form['nama_bagian'], request.form['username_admin_bagian'],
               request.form['nama_lengkap'], request.form['tanggal_lahir_bagian'], request.form['alamat'],
               request.form['no_hp_bagian']]
        
        # Update Password if provided
        if request.form['password_bagian']:
             hashed_password = hashlib.sha1(request.form['password_bagian'].encode()).hexdigest()
             sql += ", password_bagian=%s"
             val.append(hashed_password)

        if filename:
            sql += ", gambar=%s"
            val.append(filename)
            
        sql += " WHERE id_bagian=%s"
        val.append(id)
        
        cursor.execute(sql, tuple(val))
        conn.commit()
        return redirect(url_for('admin_bagian'))

    cursor.execute("SELECT * FROM tb_bagian WHERE id_bagian=%s", (id,))
    bagian = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return render_template('admin/bagian/form.html', bagian=bagian)

@app.route('/admin/bagian/delete/<int:id>')
def admin_bagian_delete(id):
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_bagian WHERE id_bagian=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin_bagian'))
    return redirect(url_for('admin_login'))

@app.route('/admin/bagian/detail/<int:id>')
def admin_bagian_detail(id):
    return f"Bagian Detail View for ID {id} - Work in Progress"

# --- Report Generation Routes ---

from utils.report_generator import generate_surat_masuk_excel, generate_surat_keluar_excel
from flask import send_file

@app.route('/admin/laporan/surat_masuk', methods=['POST'])
def admin_laporan_surat_masuk():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    bulan = request.form.get('bulan')
    tahun = request.form.get('tahun')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM tb_suratmasuk WHERE 1=1"
    params = []
    
    if bulan and bulan != 'Pilih Bulan':
        query += " AND MONTH(tanggalmasuk_suratmasuk) = %s"
        params.append(bulan)
    if tahun and tahun != 'Pilih Tahun':
        query += " AND YEAR(tanggalmasuk_suratmasuk) = %s"
        params.append(tahun)
        
    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    output = generate_surat_masuk_excel(data, bulan, tahun)
    return send_file(output, as_attachment=True, download_name=f'Laporan_Surat_Masuk_{bulan}_{tahun}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/admin/laporan/surat_keluar', methods=['POST'])
def admin_laporan_surat_keluar():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    bulan = request.form.get('bulan')
    tahun = request.form.get('tahun')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM tb_suratkeluar WHERE 1=1"
    params = []
    
    if bulan and bulan != 'Pilih Bulan':
        query += " AND MONTH(tanggalkeluar_suratkeluar) = %s"
        params.append(bulan)
    if tahun and tahun != 'Pilih Tahun':
        query += " AND YEAR(tanggalkeluar_suratkeluar) = %s"
        params.append(tahun)
        
    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    output = generate_surat_keluar_excel(data, bulan, tahun)
    return send_file(output, as_attachment=True, download_name=f'Laporan_Surat_Keluar_{bulan}_{tahun}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/bagian/laporan/surat_masuk', methods=['POST'])
def bagian_laporan_surat_masuk():
    if 'role' not in session or session['role'] != 'bagian':
        return redirect(url_for('bagian_login'))
    
    bulan = request.form.get('bulan')
    tahun = request.form.get('tahun')
    nama_bagian = session['nama_bagian']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM tb_suratmasuk WHERE (disposisi1=%s OR disposisi2=%s OR disposisi3=%s)"
    params = [nama_bagian, nama_bagian, nama_bagian]
    
    if bulan and bulan != 'Pilih Bulan':
        query += " AND MONTH(tanggalmasuk_suratmasuk) = %s"
        params.append(bulan)
    if tahun and tahun != 'Pilih Tahun':
        query += " AND YEAR(tanggalmasuk_suratmasuk) = %s"
        params.append(tahun)
        
    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    output = generate_surat_masuk_excel(data, bulan, tahun, bagian_name=nama_bagian)
    return send_file(output, as_attachment=True, download_name=f'Laporan_Surat_Masuk_Bagian_{bulan}_{tahun}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/bagian/laporan/surat_keluar', methods=['POST'])
def bagian_laporan_surat_keluar():
    if 'role' not in session or session['role'] != 'bagian':
        return redirect(url_for('bagian_login'))
    
    bulan = request.form.get('bulan')
    tahun = request.form.get('tahun')
    nama_bagian = session['nama_bagian']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM tb_suratkeluar WHERE nama_bagian=%s"
    params = [nama_bagian]
    
    if bulan and bulan != 'Pilih Bulan':
        query += " AND MONTH(tanggalkeluar_suratkeluar) = %s"
        params.append(bulan)
    if tahun and tahun != 'Pilih Tahun':
        query += " AND YEAR(tanggalkeluar_suratkeluar) = %s"
        params.append(tahun)
        
    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    output = generate_surat_keluar_excel(data, bulan, tahun, bagian_name=nama_bagian)
    return send_file(output, as_attachment=True, download_name=f'Laporan_Surat_Keluar_Bagian_{bulan}_{tahun}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(debug=True)
