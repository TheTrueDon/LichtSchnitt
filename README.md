# LichtSchnitt

LichtSchnitt ist ein geplantes Ubuntu-Programm zum Erstellen, Vorbereiten und Steuern von CNC-Lasergravur- und Schneidaufträgen. Dieses Repository enthält Version **v0.0.2**: Projektgrundlage, dokumentiertes Zielgerät und die read-only Erkennung passender USB-Seriellgeräte unter Linux. Es sendet keine Daten an einen Laser.

## Erstes Zielgerät

- Longer RAY5 10W, blauer Diodenlaser
- Arbeitsbereich: 400 × 400 mm
- Controller: MKS DLC32 V2.1
- Angezeigte Firmware: V2.20 (8M.H35.20230626)
- Geplante erste Verbindung: USB unter Ubuntu

Die Firmwarefamilie ist laut MKS-Quellcode Grbl_ESP32-basiert. Das konkrete Verhalten dieses Geräts gilt erst als bestätigt, wenn die geplanten Tests am RAY5 erfolgreich abgeschlossen wurden. Baudrate, PWM-Höchstwert und weitere Controllerparameter bleiben bis zum Auslesen ausdrücklich offen.

## Version v0.0.2 starten

Voraussetzung ist Python 3.10 oder neuer. Es werden keine zusätzlichen Python-Pakete benötigt.

```bash
cd LichtSchnitt
PYTHONPATH=src python3 -m lichtschnitt --version
PYTHONPATH=src python3 -m lichtschnitt profil
PYTHONPATH=src python3 -m lichtschnitt ports
```

`ports` listet USB-Seriellgeräte vom Typ `/dev/ttyUSB*` und `/dev/ttyACM*`, mögliche stabile `/dev/serial/by-id`-Pfade und Dateisystem-Berechtigungen auf. Es wird kein serieller Port geöffnet und es werden keine Bytes gesendet. Mit `watch` lässt sich das An- und Abstecken beobachten:

```bash
PYTHONPATH=src python3 -m lichtschnitt watch
```

Beenden mit `Strg+C`. Die Beobachtung fragt nur Linux-Gerätedateien und sysfs-Metadaten ab; Laser und Bewegungen werden nicht angesteuert.

## Entwicklung prüfen

```bash
cd LichtSchnitt
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Projektstruktur

```text
src/lichtschnitt/       Anwendungskern
  profiles/             Maschinenprofile
docs/                   Geräte- und Testdokumentation
tests/                  automatisierte Prüfungen
```

## Nächste Versionen

- **v0.0.3:** sichere, lesende Abfragen für Controllerkennung, Status und Einstellungen testen.
- **v0.1.0:** Kompatibilität am konkreten RAY5 reproduzierbar nachweisen.

Der vollständige Funktionsumfang und die Freigabekriterien stehen im separaten LichtSchnitt-Rahmenplan.

## Projektentscheidungen

Die Softwarelizenz und die GUI-Technologie werden festgelegt, bevor öffentliche Beiträge oder größere Abhängigkeiten hinzukommen. Geräte- und Testdateien enthalten keine individuelle Controller-ID.
