# Dokumentasi Integrasi WhatsApp Channel Session (Frontend)

Dokumen ini menjelaskan alur, REST API endpoints, dan integrasi WebSocket yang digunakan oleh *Frontend* untuk memanajemen sesi (session) perangkat WhatsApp Business. 

> **Catatan Keamanan:** Endpoint internal yang digunakan untuk *webhook* Meta, event bridge dari Node.js (seperti `/webhook`, `/event`, dan `/session/save`), sengaja **tidak dicantumkan** di sini karena bersifat internal server-to-server. Frontend tidak boleh dan tidak perlu mengakses endpoint tersebut.

---

## 1. REST API Endpoints

Semua endpoint REST di bawah ini memiliki *base URL*: `/api/whatsapp`

### A. Membuat Sesi Baru (Create Session)
Endpoint ini digunakan untuk menginisialisasi pembuatan sesi WhatsApp baru untuk sebuah bisnis. Biasanya memicu *service* untuk mencetak *QR Code* pertama kali.

* **URL:** `/session`
* **Method:** `POST`
* **Request Body (JSON):**
  ```json
  {
    "business_id": "string (UUID)"
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "status": "success",
    "message": "Operation successful.",
    "data": {
      "business_id": "string",
      "session_id": "string",
      "status": "pending_qr",
      "qr_code": "data:image/png;base64,...",
      "metadata": null
    }
  }
  ```

### B. Mendapatkan Status Sesi (Get Session Status)
Digunakan untuk mengecek *state* terakhir dari koneksi WhatsApp (apakah sedang meminta QR, terhubung, atau terputus) saat user memuat halaman (page load).

* **URL:** `/session/{business_id}`
* **Method:** `GET`
* **Response (200 OK):**
  ```json
  {
    "status": "success",
    "message": "Operation successful.",
    "data": {
      "business_id": "string",
      "session_id": "string",
      "status": "connected",
      "qr_code": null,
      "metadata": {
        "phone_number": "628123456789",
        "display_name": "Toko Baju Kita"
      }
    }
  }
  ```

### C. Menghapus/Logout Sesi (Delete Session)
Digunakan ketika user sengaja ingin me-logout perangkat WhatsApp mereka dari dashboard.

* **URL:** `/session/{business_id}`
* **Method:** `DELETE`
* **Response (200 OK):**
  ```json
  {
    "status": "success",
    "message": "Operation successful.",
    "data": {
      "business_id": "string",
      "status": "destroyed"
    }
  }
  ```

### D. Menghubungkan Ulang Sesi (Reconnect Session)
Jika status sesi sempat `disconnected` atau macet, frontend dapat memanggil endpoint ini untuk meminta *service* mencoba me-restart koneksi secara paksa, yang dapat menghasilkan status `connected` kembali atau `pending_qr` (meminta scan ulang).

* **URL:** `/session/reconnect/{business_id}`
* **Method:** `POST`
* **Response (200 OK):**
  *(Format response identik dengan endpoint Create Session)*

---

## 2. Integrasi WebSocket (Real-Time Events)

Karena proses penautan WhatsApp (seperti memuat QR, *scan* QR, proses sinkronisasi pesan, atau putus tiba-tiba) terjadi secara asinkron di belakang layar, **Frontend sangat diwajibkan** untuk melakukan koneksi ke WebSocket. 

Dengan WebSocket, status UI dapat berubah otomatis tanpa perlu metode *polling* (request terus menerus) ke API REST.

### Detail Koneksi WebSocket
* **URL:** `ws://<domain-backend>/ws/channels/{business_id}`
* **Keterangan:** Ganti `ws://` menjadi `wss://` jika menggunakan backend dengan koneksi HTTPS di production.

### Struktur Pesan WebSocket (Payload Event)
Pesan dikirim dari Server (WebSocket) dalam bentuk format string JSON (skema internal: `WhatsappEventPayload`). Frontend harus melakukan *parsing* (`JSON.parse()`) lalu membaca properti `event` untuk mengetahui tindakan apa yang harus dilakukan di sisi UI.

**Format Payload (Contoh):**
```json
{
  "event": "qr",
  "business_id": "06a8a34c-12f8-42c6-bf09-33f2e3a08171",
  "status": "pending_qr",
  "qr_code": "data:image/png;base64,iVBORw0KGgo...",
  "message": "QR Code diperbarui",
  "metadata": null,
  "data": null
}
```

### Jenis-Jenis `event` pada WebSocket & Action Frontend

| Nilai `event` | Nilai `status` (Terkait) | Deskripsi & Tindakan Frontend |
| :--- | :--- | :--- |
| **`qr`** | `pending_qr` | **Deskripsi:** Server baru saja men-generate QR Code baru (QR WhatsApp kedaluwarsa tiap belasan detik). <br><br>**Tindakan UI:** Render ulang tag `<img>` atau *image view* menggunakan isi dari properti `qr_code`. |
| **`authenticated`** | `authenticating` | **Deskripsi:** User baru saja memindai (scan) QR Code melalui HP-nya, dan WhatsApp sedang mencocokkan kredensial. <br><br>**Tindakan UI:** Hilangkan gambar QR Code. Tampilkan indikator *Loading/Spinner* dan teks "Sedang memverifikasi perangkat...". |
| **`ready`** | `connected` | **Deskripsi:** Kredensial disetujui, riwayat chat (bila ada) telah di-sync, dan WhatsApp siap mengirim/menerima pesan. <br><br>**Tindakan UI:** Ubah tampilan status menjadi **"Terhubung" (Connected)**. Buka akses panel *chatting* atau tutup modal QR Code. |
| **`disconnected`** | `disconnected` | **Deskripsi:** Koneksi ke HP terputus (bisa karena HP mati, tidak ada kuota, atau di-logout dari HP secara langsung). <br><br>**Tindakan UI:** Ubah tampilan menjadi "Terputus" dan tunjukkan peringatan kepada user. Munculkan tombol untuk memanggil API `reconnect`. |
| **`state_changed`** | *(beragam)* | **Deskripsi:** *Event* umum ketika status sesi mengalami transisi namun bukan termasuk momen krusial. Berguna jika sekadar ingin meng-update label teks status di UI. |

---

## 3. Contoh Best-Practice Alur Integrasi (Flow) Frontend

1. **Memasuki Halaman Dashboard WhatsApp:**
   - Frontend memanggil API `GET /api/whatsapp/session/{business_id}`.
   - Frontend **segera** membuka koneksi WebSocket ke `/ws/channels/{business_id}`.
   - Sesuai dengan respons GET tadi, ubah UI (jika `connected`, tampilkan menu chat. Jika `pending_qr`, tampilkan QR).

2. **Menambahkan/Menautkan Sesi Baru:**
   - Frontend memanggil `POST /api/whatsapp/session`.
   - UI memunculkan *Modal* / Popup kosong sembari menunggu QR Code.
   - Frontend menangkap event WebSocket dengan `event: "qr"` dan merender QR Code ke dalam Modal tersebut.
   - Jika ada pesan `event: "ready"` dari WebSocket, Frontend otomatis menutup Modal dan men-trigger fungsi success.

3. **Logika Koneksi WebSocket yang Tangguh:**
   - Harap terapkan logika *auto-reconnect* pada koneksi WebSocket di browser. Karena jika koneksi internet user terganggu 1 detik saja, *socket browser* akan mati (close) dan *event* penting seperti `ready` bisa jadi tidak akan pernah diterima.
