# Geräteprofil für den Longer RAY5 10W

## Bekannte Angaben

| Merkmal | Wert |
| --- | --- |
| Gerät | Longer RAY5 10W |
| Laserart | Blauer Diodenlaser |
| Arbeitsbereich | 400 × 400 mm |
| Controller | MKS DLC32 V2.1 |
| Anzeige Firmware | V2.20 (8M.H35.20230626) |
| Wellenlänge laut Modul | 450–460 nm |
| Optische Leistung laut Modul | 10–11 W |
| Maximale elektrische Eingangsangabe am Modul | 12 V, 3,2 A |
| Erste Verbindung | USB unter Ubuntu |

Die Geräteangaben werden auch in `src/lichtschnitt/profiles/longer_ray5_10w_mks_dlc32_v2_1.json` geführt.

## Noch zu ermitteln

Die konkreten Werte müssen in einer späteren Version am Controller ausgelesen oder getestet werden:

- Linux-Gerätepfad und verwendeter USB-Seriell-Chip
- Baudrate und serielle Einstellungen
- Controllerkennung und unterstützte Statusfelder
- Arbeitskoordinaten, Ursprung und Endschalterverhalten
- Firmwareseitiger Leistungsbereich und Laser-PWM-Konfiguration

Die Modulwerte für Spannung, Strom und optische Leistung legen die G-Code-Leistungswerte nicht fest. Wir übernehmen keine Baudrate oder PWM-Grenze aus einem anderen RAY5-Profil.

## Datenschutz und Git

Die auf dem Display angezeigte CPU-ID wird nicht in das gemeinsam nutzbare Geräteprofil übernommen. Falls sie für eine lokale Testnotiz gebraucht wird, bleibt sie außerhalb der öffentlichen Profil- und Protokolldateien.
