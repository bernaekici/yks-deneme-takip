import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="YKS Deneme & Eksik Takip Sistemi", layout="wide")

# Veri saklama dosyası
DATA_FILE = "yks_denemeler.json"

# --- MÜFREDAT SÖZLÜĞÜ ---
MUPREDAT = {
    "Türkçe": [
        "Sözcükte Anlam", "Söz Yorumu", "Deyim and Atasözü", "Cümlede Anlam", "Paragraf",
        "Paragrafta Anlatım Teknikleri", "Paragrafta Düşünceyi Geliştirme Yolları", "Paragrafta Yapı",
        "Paragrafta Konu-Ana Düşünce", "Paragrafta Yardımcı Düşünce", "Ses Bilgisi", "Yazım Kuralları",
        "Noktalama İşaretleri", "Sözcükte Yapı/Ekler", "Sözcük Türleri", "İsimler", "Zamirler",
        "Sıfatlar", "Zarflar", "Edat – Bağlaç – Ünlem", "Fiiller", "Fiilde Anlam (Kip-Kişi-Yapı)",
        "Ek Fiil", "Fiilimsi", "Fiilde Çatı", "Sözcük Grupları", "Cümlenin Ögeleri", "Cümle Türleri",
        "Anlatım Bozukluğu"
    ],
    "Matematik": [
        "Temel Kavramlar", "Sayı Basamakları", "Bölme ve Bölünebilme", "EBOB – EKOK", "Rasyonel Sayılar",
        "Basit Eşitsizlikler", "Mutlak Değer", "Üslü Sayılar", "Köklü Sayılar", "Çarpanlara Ayırma",
        "Oran Orantı", "Denklem Çözme", "Sayı Problemleri", "Kesir Problemleri", "Yaş Problemleri",
        "Hareket Hız Problemleri", "İşçi Emek Problemleri", "Yüzde Problemleri", "Kar Zarar Problemleri",
        "Karışım Problemleri", "Grafik Problemleri", "Rutin Olmayan Problemleri", "Kümeler – Kartezyen Çarpım",
        "Mantık", "Fonksiyonlar", "Polinomlar", "2.Dereceden Denklemler", "Permütasyon ve Kombinasyon", "Olasılık",
        "Veri – İstatistik"
    ],
    "Geometri": [
        "Temel Kavramlar", "Doğruda Açılar", "Üçgende Açılar", "Özel Üçgenler (Dik/İkizkenar/Eşkenar)",
        "Açıortay", "Kenarortay", "Eşlik ve Benzerlik", "Üçgende Alan", "Açı Kenar Bağıntıları",
        "Çokgenler", "Özel Dörtgenler (Deltoid/Paralelkenar/Eşkenar Dörtgen/Dikdörtgen/Kare/Yamuk)",
        "Çember ve Daire (Açı/Uzunluk/Alan)", "Analitik Geometri (Nokta/Doğru/Dönüşüm/Çemberin Analitiği)",
        "Katı Cisimler (Prizmalar/Silindir/Piramit/Koni/Küre)"
    ],
    "Tarih (Sosyal)": [
        "Tarih ve Zaman", "İnsanlığın İlk Dönemleri", "Ortaçağ’da Dünya", "İlk ve Orta Çağlarda Türk Dünyası",
        "İslam Medeniyetinin Doğuşu", "İlk Türk İslam Devletleri",
        "Yerleşme ve Devletleşme Sürecinde Selçuklu Türkiyesi",
        "Beylikten Devlete Osmanlı Siyaseti(1300-1453)", "Dünya Gücü Osmanlı Devleti (1453-1600)",
        "Yeni Çağ Avrupa Tarihi",
        "Yakın Çağ Avrupa Tarihi", "Osmanlı Devletinde Arayış Yılları", "18. Yüzyılda Değişim ve Diplomasi",
        "En Uzun Yüzyıl", "Osmanlı Kültür ve Medeniyeti", "20. Yüzyılda Osmanlı Devleti", "I. Dünya Savaşı",
        "Mondros Ateşkesi, İşgaller ve Cemiyetler", "Kurtuluş Savaşına Hazırlık Dönemi", "I. TBMM Dönemi",
        "Kurtuluş Savaşı ve Antlaşmalar", "II. TBMM Dönemi ve Çok Partili Hayata Geçiş", "Türk İnkılabı",
        "Atatürk İlkeleri", "Atatürk Dönemi Türk Dış Politikası"
    ],
    "Coğrafya (Sosyal)": [
        "Doğa ve İnsan", "Dünya’nın Şekli ve Hareketleri", "Coğrafi Konum", "Harita Bilgisi", "Atmosfer ve Sıcaklık",
        "İklimler", "Basınç ve Rüzgarlar", "Nem, Yağış ve Buharlaşma", "İç Kuvvetler / Dış Kuvvetler",
        "Su – Toprak ve Bitkiler", "Nüfus", "Göç", "Yerleşme", "Türkiye’nin Yer Şekilleri", "Ekonomik Faaliyetler",
        "Bölgeler", "Uluslararası Ulaşım Hatları", "Çevre and Toplum", "Doğal Afetler"
    ],
    "Felsefe (Sosyal)": [
        "Felsefenin Konusu", "Bilgi Felsefesi", "Varlık Felsefesi", "Din, Kültür ve Medeniyet", "Ahlak Felsefesi",
        "Sanat Felsefesi", "Din Felsefesi", "Siyaset Felsefesi", "Bilim Felsefesi"
    ],
    "Din Kültürü (Sosyal)": [
        "İnanç", "İbadet", "Ahlak ve Değerler", "Din, Kültür ve Medeniyet", "Hz. Muhammed (S.A.V.)",
        "Vahiy ve Akıl", "Dünya ve Ahiret", "Kur’an'a göre Hz. Muhammed (S.A.V.)", "İnançla İlgili Meseleler",
        "Yahudilik ve Hristiyanlık", "İslam ve Bilim", "Anadolu'da İslam", "İslam Düşüncesinde Tasavvufi Yorumlar",
        "Güncel Dini Meseler", "Hint and Çin Dinleri"
    ],
    "Fizik (Fen)": [
        "Fizik Bilimine Giriş", "Madde ve Özellikleri", "Sıvıların Kaldırma Kuvveti", "Basınç",
        "Isı, Sıcaklık ve Genleşme", "Hareket ve Kuvvet", "Dinamik", "İş, Güç ve Enerji",
        "Elektrik", "Manyetizma", "Dalgalar", "Optik"
    ],
    "Kimya (Fen)": [
        "Kimya Bilimi", "Atom ve Periyodik Sistem", "Kimyasal Türler Arası Etkileşimler", "Maddenin Hâlleri",
        "Doğa ve Kimya", "Kimyanın Temel Kanunları ve Kimyasal Hesaplamalar", "Karışımlar",
        "Asitler, Bazlar ve Tuzlar", "Kimya Her Yerde"
    ],
    "Biyoloji (Fen)": [
        "Canlıların Ortak Özellikleri", "Canlıların Temel Bileşenleri", "Hücre ve Organelleri",
        "Hücre Zarından Madde Geçişi", "Canlıların Sınıflandırılması", "Mitoz and Eşeysiz Üreme",
        "Mayoz and Eşeyli Üreme", "Kalıtım", "Ekosistem Ekolojisi", "Güncel Çevre Sorunları"
    ]
}


# Veri yükleme fonksiyonu
def verileri_yukle():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def verileri_kaydet(veri):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)


kayitlar = verileri_yukle()

st.title("🎯 YKS Deneme Takip ve Eksik Analiz Sistemi")

# Sekmeler
tab1, tab2, tab3 = st.tabs(["📝 Yeni Deneme Ekle", "📊 Genel Durum & Eksik Analizi", "📚 Geçmiş Denemeler"])

with tab1:
    st.subheader("Yeni Deneme Sonucu ve Eksikleri Gir")

    with st.form("deneme_ekleme_formu"):
        col1, col2 = st.columns(2)
        with col1:
            deneme_adi = st.text_input("Deneme Adı / Yayın (Örn: 3D Yayınları TYT 1)")
        with col2:
            deneme_turu = st.selectbox("Deneme Türü", ["TYT", "AYT", "YDT"])

        st.markdown("---")
        st.info("Her ders için netini gir ve o denemede yanlış/boş yaptığın konuları işaretle.")

        ders_netleri = {}
        ders_eksikleri = {}

        # Dersleri döngüye sokalım
        for ders_adi, konular in MUPREDAT.items():
            with st.expander(f"📌 {ders_adi}"):
                net = st.number_input(f"{ders_adi} Neti", min_value=0.0, max_value=120.0, step=0.25,
                                      key=f"net_{ders_adi}")
                ders_netleri[ders_adi] = net

                st.write("Eksik/Yanlış Yapılan Konular:")
                secilenler = []
                cols = st.columns(2)
                for i, konu in enumerate(konumlar := konular):  # Python esnekliği için
                    with cols[i % 2]:
                        if st.checkbox(konu, key=f"ch_{ders_adi}_{konu}"):
                            secilenler.append(konu)
                ders_eksikleri[ders_adi] = secilenler

        kaydet_butonu = st.form_submit_button("Denemeyi Kaydet ve Analiz Et")

        if kaydet_butonu:
            if not deneme_adi:
                st.warning("Lütfen deneme adını giriniz!")
            else:
                yeni_kayit = {
                    "deneme_adi": deneme_adi,
                    "deneme_turu": deneme_turu,
                    "netler": ders_netleri,
                    "eksikler": ders_eksikleri
                }
                kayitlar.append(yeni_kayit)
                verileri_kaydet(kayitlar)
                st.success("Deneme başarıyla kaydedildi! 'Genel Durum & Eksik Analizi' sekmesinden inceleyebilirsin.")

with tab2:
    st.subheader("📊 Genel Durum ve En Çok Yanlış Yapılan Konular")

    if not kayitlar:
        st.warning("Henüz kayıtlı bir deneme bulunmuyor. Önce 'Yeni Deneme Ekle' sekmesinden deneme girişi yap.")
    else:
        konu_frekanslari = {}
        for kayit in kayitlar:
            for ders, eksik_listesi in kayit["eksikler"].items():
                for konu in eksik_listesi:
                    anahtar = f"{ders} ➔ {konu}"
                    konu_frekanslari[anahtar] = konu_frekanslari.get(anahtar, 0) + 1

        if konu_frekanslari:
            st.markdown("### ⚠️ En Çok Tekrar Eden Eksiklerin (Kırmızı Alarm)")
            st.info(
                "Aşağıdaki konular farklı denemelerde en çok yanlış yaptığın veya boş bıraktığın konuları gösterir. Önceliği bunlara vermelisin!")

            df_eksik = pd.DataFrame(list(konu_frekanslari.items()), columns=["Ders ve Konu", "Yanlış Yapılma Sayısı"])
            df_eksik = df_eksik.sort_values(by="Yanlış Yapılma Sayısı", ascending=False).reset_index(drop=True)

            st.dataframe(df_eksik, use_container_width=True)
        else:
            st.success("Harika! Henüz hiçbir denemede konu eksiği işaretlenmemiş.")

        st.markdown("---")
        st.markdown("### 📈 Deneme Netleri Gelişimi")
        net_verileri = []
        for kayit in kayitlar:
            for ders, net in kayit["netler"].items():
                if net > 0:
                    net_verileri.append({
                        "Deneme": kayit["deneme_adi"],
                        "Ders": ders,
                        "Net": net
                    })
        if net_verileri:
            df_netler = pd.DataFrame(net_verileri)
            st.line_chart(df_netler, x="Deneme", y="Net", color="Ders")

with tab3:
    st.subheader("📚 Kayıtlı Geçmiş Denemeler")
    if not kayitlar:
        st.info("Kayıtlı deneme yok.")
    else:
        for index, kayit in enumerate(kayitlar):
            with st.expander(f"📌 {kayit['deneme_adi']} ({kayit['deneme_turu']})"):
                st.write("**Ders Netleri:**")
                net_str = " | ".join([f"{d}: {n}" for d, n in kayit["netler"].items() if n > 0])
                st.write(net_str if net_str else "Net girilmemiş.")

                st.write("**Bu Denemedeki Eksik Konular:**")
                bos_mu = True
                for ders, eksikler in kayit["eksikler"].items():
                    if eksikler:
                        bos_mu = False
                        st.markdown(f"- **{ders}:** {', '.join(eksikler)}")
                if bos_mu:
                    st.write("Bu denemede eksik konu işaretlenmemiş.")

                if st.button("Bu Denemeyi Sil", key=f"sil_{index}"):
                    kayitlar.pop(index)
                    verileri_kaydet(kayitlar)
                    st.rerun()