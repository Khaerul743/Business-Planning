const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const express = require('express');

const app = express();
app.use(express.json());
const PORT = process.env.PORT || 3000;

function get_body_message(sender, message) {
    const body_message = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "ID_AKUN_WABA",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "NOMOR_ANDA",
                                "phone_number_id": "12345678"
                            },
                            "contacts": [
                                {
                                    "profile": {
                                        "name": "-"
                                    },
                                    "wa_id": "-"
                                }
                            ],
                            "messages": [
                                {
                                    "from": "6281386606463",
                                    "id": "ID_PESAN_UNIK",
                                    "timestamp": "WAKTU",
                                    "text": {
                                        "body": message
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    return body_message
}

// URL Webhook Backend Python kamu (sesuaikan port-nya)
const PYTHON_BACKEND_URL = 'http://localhost:8000/api/whatsapp/webhook';

// Inisialisasi client WhatsApp dengan fitur simpan sesi otomatis
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Jalur 1: Menampilkan QR Code untuk di-scan
client.on('qr', (qr) => {
    console.log('[-] Silahkan scan QR Code di bawah ini menggunakan WhatsApp HP-mu:');
    qrcode.generate(qr, { small: true });
});

// Jalur 2: Notifikasi jika berhasil masuk
client.on('ready', () => {
    console.log('[+] WhatsApp Bridge SIAP! Menunggu chat masuk...');
});

// Fungsi pembantu untuk membuat jeda (delay)
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Jalur 3: Mendengarkan pesan masuk secara real-time
client.on('message', async (msg) => {
    // Abaikan pesan yang berasal dari grup (hanya proses chat pribadi)
    if (msg.from.includes('@g.us')) return;
    // console.log(msg)
    // const namaPengirim = msg.notifyName || 'User WhatsApp';

    // Ambil data detail kontak si pengirim
    const contact = await msg.getContact();

    // contact.number akan menghasilkan nomor HP murni (contoh: 6285880171247)
    const nomorHP = contact.number;
    const namaPengirim = msg.notifyName || contact.pushname || 'User WhatsApp';

    console.log(`[+] Pesan masuk dari No: [${nomorHP}] nama [${namaPengirim}]: ${msg.body}`);

    try {
        // 1. SIMULASI MEMBACA: Tahan 1 - 2 detik seolah-olah baru sadar ada chat masuk
        const jedaMembaca = Math.floor(Math.random() * (2000 - 1000 + 1)) + 1000; // antara 1000ms s.d 2000ms
        await sleep(jedaMembaca);

        // 3. Teruskan data chat ke backend Python menggunakan Axios
        const response = await axios.post(PYTHON_BACKEND_URL, get_body_message(msg.from, msg.body), { timeout: 10000 });

    } catch (error) {
        console.error(`[x] Gagal berkomunikasi dengan Backend Python: ${error.message}`);
    }
});

// Jalankan service bridge
client.initialize();

// Endpoint untuk menerima pesan dari backend dan mengirimkannya ke WhatsApp
app.post('/api/send-message', async (req, res) => {
    try {
        const { to, message } = req.body;

        if (!to || !message) {
            return res.status(400).json({ error: 'Parameter "to" dan "message" wajib diisi' });
        }

        const chatId = to.includes('@') ? to : `${to}@c.us`;

        // Simulasi mengetik sebelum mengirim pesan
        try {
            const chat = await client.getChatById(chatId);
            await chat.sendStateTyping();

            // Tahan sedikit agar natural
            const jedaMengetik = Math.floor(Math.random() * (10000 - 5000 + 1)) + 5000;
            await sleep(jedaMengetik);

            await client.sendMessage(chatId, message);
            await chat.clearState();
        } catch (chatError) {
            // Jika objek chat belum ada atau gagal mendapatkan chat, langsung kirim pesan
            await client.sendMessage(chatId, message);
        }

        console.log(`[->] Berhasil mengirim pesan via Express webhook ke [${chatId}]: ${message}`);
        return res.status(200).json({ status: 'success', message: 'Pesan berhasil dikirim' });
    } catch (error) {
        console.error(`[x] Gagal mengirim pesan via webhook: ${error.message}`);
        return res.status(500).json({ error: 'Gagal mengirim pesan', details: error.message });
    }
});

// Jalankan Express server
app.listen(PORT, () => {
    console.log(`[+] Express webhook server berjalan di port ${PORT}`);
});