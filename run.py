import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

# Load .env
load_dotenv()
WP_API_URL = os.getenv("WP_API_URL")
WP_USER = os.getenv("WP_USER")
WP_PASS = os.getenv("WP_PASS")

def ambil_tabel_hongkong():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = "http://206.189.86.19/data-keluaran-hongkong/"

            # Tambahkan retry maksimal 3x
            for attempt in range(3):
                try:
                    print(f"🌐 Akses ke {url} (percobaan {attempt + 1})")
                    page.goto(url, timeout=90000, wait_until="load")
                    page.wait_for_selector("table.baru", timeout=10000)
                    break  # sukses, keluar dari loop
                except Exception as e:
                    print(f"🔁 Gagal buka halaman (percobaan {attempt + 1}): {e}")
                    if attempt == 2:
                        raise  # kalau 3x gagal, lempar error

            html = page.content()
            browser.close()

            soup = BeautifulSoup(html, "html.parser")
            tabel_list = soup.find_all("table", class_="baru")

            if not tabel_list:
                print("❌ Tidak ada tabel ditemukan.")
                return None

            hasil = []

            for table in tabel_list:
                heading = table.find_previous(["h2", "h3", "h4"])
                if heading:
                    hasil.append(f"<{heading.name}>{heading.text.strip()}</{heading.name}>")

                # Ubah warna lama ke warna baru
                table_html = str(table).replace("#68a225", "#29bfe5").replace("#265c00", "#30257d")
                hasil.append(table_html)

            print(f"✅ Ditemukan {len(tabel_list)} tabel + judul.")
            return "\n".join(hasil)

    except Exception as e:
        print(f"❌ Error ambil data: {e}")
        return None


def gabungkan_ke_template(tabel_html):
    try:
        bagian_atas = """
<article id="post-4735" class="single-view post-4735 post type-post status-publish format-standard hentry category-data-hk tag-data-hk tag-keluaran-hk tag-paito-hk tag-pengeluaran-hk" itemprop="blogPost" itemscope="" itemtype="http://schema.org/BlogPosting">
<header class="entry-header cf">
<h1 class="entry-title" itemprop="headline"><a href="./">Data Keluaran Hongkong 2025</a></h1>
</header>
<div class="entry-byline cf">		
</div>
<div class="entry-content cf" itemprop="text">
<p><strong>Data Keluaran Hongkong 2025, Data HK 2024, Angka Pengeluaran HK terlengkap</strong></p>
<p>Rekap <a href="./"><span style="text-decoration: underline;"><strong>Pengeluaran togel hongkong</strong></span></a> terbaru, Result togel hk tercepat hari ini, Angka keluaran Hk lengkap mulai tahun 2018 sampai 2025. Data Hk 1st terpercaya, nomor togel hongkong akurat yang diambil dari situs resmi keluaran togel hkg pools.</p>
<p><strong>Data Hongkong 2018-2025</strong> yang rangkum kedalam tabel paito togel hongkong secara lengkap. Hasil nomor pengeluaran togel hk tercepat, Angka keluaran hkg 4D hari ini terpercaya, Data togel hongkong terbaru cocok untuk mecari angka terikan paito.</p>
<div id="attachment_4769" style="width: 1010px" class="wp-caption alignnone"><p id="caption-attachment-4769" class="wp-caption-text">Data Keluaran Hongkong 2025, Data Hk pools terbaru</p></div>
<table>
<tbody>
<tr>
<td><span style="color: #800000;"><strong>Keluaran togel hongkong aktif setiap hari dan untuk jam result <a href="./"><span style="text-decoration: underline;">pengeluaran hk</span></a> adalah pukul 23.00 WIB. Tabel ini di update setelah hasil akhir result hk 1st prize.</strong></span></td>
</tr>
</tbody>
</table>
<h3>Data Keluaran HK 2018</h3>
<table class="baru">
<tbody>
</table>
"""

        bagian_bawah = """
<p><strong>Data Pengeluaran HK</strong> diatas merupakan hasil resmi result hongkong malam ini, Hasil result <a href="./"><span style="text-decoration: underline;"><strong>keluaran hongkong 2025</strong></span></a>, Angka keluar togel hk terbaru, paito toto hongkong4d tercepat, Data hk 2023 terbaru, data hongkong terlengkap.</p>
<blockquote><p>Kamu juga mungkin membutuhkan <a href="./"><strong>Data SGP 2025</strong></a></p></blockquote>
<p>Untuk <strong><em>Hasil togel hongkong 2025</em></strong> akan kami update setelah pemutaran live draw prize 1st berakhir, keluaran togel hk hari ini, rekap bola jatuh togel hongkong terbaru. Kamu dapat gunakan data hongkong untuk merumus hk jitu.</p>
<h3>Data HK Pools 2025</h3>
<p><strong>Data keluaran Hongkong 2025</strong> menjadi landasan yang penting dalam pemasangan angka, karena dengan <a href="./"><strong>Data togel hk</strong></a> terlengkap, pencarian angka yang sering keluar lebih mudah. Pemilahan angka yang belum pernah tampil dalam paito juga akan terlihat.</p>
<p>Sekianlah Data Keluaran Hongkong 2025 yang bisa kami sampaikan buat kawan semuanya, jangan lupa berbagi prediksi dikolom komentar ya, supaya kita lebih kompak untuk menang togel. Berkunjung kembali kemari jika ingin melihat <span style="text-decoration: underline;"><strong>Data Pengeluaran Hk 2025</strong></span> terbaru.</p>
<h4>Incoming search terms:</h4><ul><li>Data HK 2024</li><li>Data pengeluaran hk 2024</li><li>data angka keluar hongkong</li><li>pengeluaran hk pools</li><li>togel keluaran hongkong 2024</li><li>Data HK 2023</li><li>Data pengluaran h k</li><li>data angka hk</li><li>angka keluar hkg</li><li>Pengeluaran hk 2024</li></ul>
</div>
<footer class="entry-footer cf">
</footer>
</article>
"""

        hasil_html = bagian_atas + tabel_html + bagian_bawah

        with open("result_hongkong.html", "w", encoding="utf-8") as f:
            f.write(hasil_html)

        print("✅ result_hongkong.html berhasil dibuat.")
        return hasil_html
    except Exception as e:
        print(f"❌ Error saat gabung template: {e}")
        return None

def post_ke_wordpress(html_content):
    if not WP_API_URL or not WP_USER or not WP_PASS:
        print("❌ Data .env tidak lengkap.")
        return

    headers = {"Content-Type": "application/json"}
    data = {
        "title": "",
        "content": html_content,
        "status": "publish"
    }

    try:
        r = requests.post(WP_API_URL, json=data, auth=(WP_USER, WP_PASS), headers=headers)
        if r.status_code in [200, 201]:
            print("✅ Berhasil posting ke WordPress.")
            print(f"🔗 Link: {r.json().get('link')}")
        else:
            print(f"❌ Gagal post: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Error saat post ke WordPress: {e}")

if __name__ == "__main__":
    tabel_html = ambil_tabel_hongkong()
    if tabel_html:
        full_html = gabungkan_ke_template(tabel_html)
        if full_html:
            post_ke_wordpress(full_html)
