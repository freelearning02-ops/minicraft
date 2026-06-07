import time
from mcpi.minecraft import Minecraft
from mcpi import block

def goz qirpiminda_yox_olan_yol():
    mc = Minecraft.create()
    x, y, z = mc.player.getTilePos()
    
    mc.postToChat("=== YOK OLAN RENGBERENG PARKUR ===")
    mc.postToChat("Yol hazirlanir... 3 saniye gozleyin.")
    time.sleep(3)
    
    # 1. RƏNGBƏRƏNG YOLUN TİKİLMƏSİ (Uzunluq: 30 blok)
    yol_uzunlugu = 30
    yol_y = y + 5 # Oyunçunun başı üzərində, havada tikilir
    
    mc.postToChat("Yol tikildi! Yuxari teleport olunursunuz...")
    
    # Dövr ilə hər bloka fərqli rəng kodu (0-15 arası) verərək yol tikirik
    for i in range(yol_uzunlugu):
        reng_kodu = i % 15
        # 35 - Yun blokunun ID-sidir
        mc.setBlock(x + i, yol_y, z, 35, reng_kodu)
        mc.setBlock(x + i, yol_y, z + 1, 35, reng_kodu) # Yolu 2 blok genişlikdə edirik
        
    # Oyunçunu yolun başlanğıcına teleport edirik
    time.sleep(1)
    mc.player.setTilePos(x, yol_y + 1, z)
    mc.postToChat("QAÇIN!!! Bloklar arxanizca yox olur!")

    # 2. ANLIQ REAKSİYA VƏ HƏRƏKƏT DÖVRÜ
    yox_olan_bloklar = []
    
    try:
        while True:
            # Oyunçunun ayaq basdığı anlıq koordinatı alırıq
            p_x, p_y, p_z = mc.player.getTilePos()
            
            # Əgər oyunçu hələ də bizim tikdiyimiz yolun hündürlüyündədirsə
            if p_y == yol_y + 1:
                # Oyunçunun tam altındakı bloku yoxlayırıq
                alt_blok_x = p_x
                alt_blok_z = p_z
                
                # Oyunçunun altındakı blokun ID-sini alırıq (Hava deyilsə)
                b_id = mc.getBlock(alt_blok_x, yol_y, alt_blok_z)
                
                if b_id != 0: # 0 = Hava (AIR) blokudur, yəni boşluq deyil qaçırsa
                    # 1. Addım: Ayaq dəyən bloku XƏBƏRDARLIQ üçün QIRMIZI yuna çevir (Rəng kodu: 14)
                    mc.setBlock(alt_blok_x, yol_y, alt_blok_z, 35, 14)
                    
                    # Bu blokun koordinatını və toxunma vaxtını siyahıya əlavə et
                    # Bizə lazımdır ki, tam 0.5 - 1 saniyə sonra yox olsun (istifadəçi qaçmağa çatdırsın)
                    if (alt_blok_x, alt_blok_z) not in [b[0] for b in yox_olan_bloklar]:
                        yox_olan_bloklar.append(((alt_blok_x, alt_blok_z), time.time()))
            
            # Zamanı gələn blokları arxadan silmək (Yox etmək) mexanizmi
            cari_zaman = time.time()
            for b_koordinat, t_vaxt in list(yox_olan_bloklar):
                if cari_zaman - t_vaxt > 0.6: # 0.6 saniyə sonra blok havaya çevrilir!
                    mc.setBlock(b_koordinat[0], yol_y, b_koordinat[1], block.AIR.id)
                    yox_olan_bloklar.remove((b_koordinat, t_vaxt))
            
            # Əgər oyunçu aşağı düşübsə (Yoldan yıxılıbsa) oyunu bitir
            if p_y < yol_y:
                mc.postToChat("Yixildiniz! Oyun Bitdi.")
                break
                
            time.sleep(0.05) # Çox sürətli yoxlama (Saniyədə 20 dəfə)
            
    except KeyboardInterrupt:
        mc.postToChat("Oyun dayandirildi.")

if __name__ == "__main__":
    goz_qirpiminda_yox_olan_yol()
