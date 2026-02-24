# Cisco CUCM Real-Time Registered Device IP Scanner

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Cisco](https://img.shields.io/badge/Cisco-CUCM%20v11.5%20--%20v15-orange)

Bu proje, **Cisco Unified Communications Manager (CUCM)** altyapısında bulunan IP telefonların ve cihazların gerçek zamanlı IP adreslerini toplamak için geliştirilmiş bir otomasyon aracıdır. Proje, özellikle büyük ölçekli ses networklerinde envanter takibi ve troubleshooting süreçlerini manuel olmaktan kurtarıp otomatik hale getirir.

## Teknik Mimari
Bu script iki temel Cisco servisini birleştirir:
1. **AXL API (Administrative XML):** CUCM veritabanından cihaz listesini ve model bilgilerini çekmek için kullanılır.
2. **RISPort (Real-time Information Service):** Cihazların o andaki "Registered" durumunu ve aktif IPv4 adreslerini çekmek için kullanılır.

### Öne Çıkan Özellikler
- **Model Filtreleme:** Kullanıcı girişi ile belirli bir modele (Örn: 7841, 8821) veya tüm envantere odaklanma.
- **Akıllı Rate Limiting:** Cisco RISPort servisinin uyguladığı **dakikada 15 istek** limitini aşmamak için arka planda `time.sleep` mekanizması ile hız yönetimi yapar.

## Gereksinimler
Projenin çalışması için aşağıdaki kütüphanelerin yüklü olması gerekir:
- `ciscoaxl`
- `zeep` (SOAP istemcisi için)
- `requests`

## Proje Çıktısı

```text
Model giriniz (tüm modeller için ENTER): 7841

REGISTERED: SEP9A711D0578AA -> 10.87.74.15
REGISTERED: SEPCD9E1F457BEE -> 10.8.20.96
REGISTERED: SEP6C8D77D068A3 -> 10.1.47.177
REGISTERED: SEP009E1EDF1A22 -> 192.168.1.1
...
...
...
REGISTERED: SEP7A8F2DFC3A45 -> 192.168.1.22
[OK] Sonuçlar 'cucm_registered_ips.txt' dosyasına yazıldı.

Toplam Aktif Cihaz Sayısı: 1478

```



