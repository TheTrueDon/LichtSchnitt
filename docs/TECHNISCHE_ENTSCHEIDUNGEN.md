# Technische Entscheidungen

## 0001 – Zuerst ein explizites RAY5-Geräteprofil

- **Status:** angenommen für v0.0.1
- **Entscheidung:** Das erste Profil beschreibt exakt den Longer RAY5 10W mit MKS DLC32 V2.1 und der angegebenen Firmware.
- **Grund:** Der Rahmenplan verlangt einen reproduzierbaren Kompatibilitätsnachweis am vorhandenen Gerät.
- **Folge:** Firmwarefamilie und Anschlussart sind Erwartungen; Schnittstellenwerte und Maschinenreaktionen bleiben bis zum Gerätetest unbestätigt.

## 0002 – Keine geratenen seriellen oder Leistungswerte

- **Status:** angenommen für v0.0.1
- **Entscheidung:** Baudrate, serielle Datenparameter und PWM-Grenzen bleiben offen, bis sie am Controller nachgelesen oder gemessen wurden.
- **Grund:** Elektrische Angaben des Lasermoduls bestimmen nicht die Einstellungen, die ein Controller per G-Code erwartet.

## 0003 – Frühe Versionen bleiben frei von Maschinensteuerung

- **Status:** angenommen für v0.0.1 bis v0.0.3
- **Entscheidung:** Die ersten Stufen dokumentieren das Gerät, erkennen den USB-Port und erproben ausschließlich lesende Abfragen. Bewegung und Laserleistung sind deaktiviert.
- **Grund:** Die Kompatibilität muss zuerst belegt werden; unerwartete Maschinenreaktionen sind in dieser Phase nicht Teil des Tests.

## 0004 – GUI-Technologie und Softwarelizenz

- **Status:** offen
- **Entscheidung:** Wird vor dem Editor-Grundgerüst in v0.3.0 anhand von Ubuntu-Unterstützung, Vektor-/Rasteranforderungen, Paketierung und Lizenzbedingungen getroffen.
