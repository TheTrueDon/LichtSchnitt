# Prüfprotokoll für RAY5 und DLC32

## Zweck

Dieses Protokoll führt vom sicheren Erkennen des Zielgeräts zu einem reproduzierbaren Kompatibilitätsnachweis. Version v0.0.1 dokumentiert die Prüfung; sie verbindet sich noch nicht mit der Maschine.

## Sicherheitsgrenze für v0.0.1 bis v0.0.3

- Keine Bewegungsbefehle senden.
- Keine Laserbefehle oder Leistungswerte senden.
- Keine Firmware aktualisieren oder Controllerparameter schreiben.
- Bei unerwarteter Bewegung, Lichtemission oder unbekanntem Maschinenzustand abbrechen und den Befund dokumentieren.

## Prüfschritte nach Version

### v0.0.1 – Geräteangaben festhalten

- [x] Longer RAY5 10W als Zielgerät notiert.
- [x] Arbeitsbereich 400 × 400 mm notiert.
- [x] Controller MKS DLC32 V2.1 notiert.
- [x] Angezeigte Firmware notiert.
- [ ] Profil mit dem tatsächlich angeschlossenen Gerät abgleichen.

### v0.0.2 – Serielle Schnittstelle erkennen

Noch auszuführen, sobald die Schnittstellenerkennung implementiert ist:

1. Im Projektordner `PYTHONPATH=src python3 -m lichtschnitt watch` starten.
2. Maschine per USB mit dem Ubuntu-PC verbinden.
3. Den erkannten Gerätepfad, stabilen `/dev/serial/by-id`-Pfad, USB-Kennung und Dateizugriffsrechte protokollieren.
4. Gerät trennen und erneut verbinden; prüfen, ob beide Ereignisse erkannt werden.
5. Mit `Strg+C` beenden. Der Port wird nicht geöffnet; es werden keine Bytes an den Controller gesendet.

**Bestanden, wenn:** das Gerät reproduzierbar erkannt wird, An- und Abstecken korrekt gemeldet werden und keine Daten über die serielle Schnittstelle gesendet werden.

### v0.0.3 – Lesende Controller-Abfragen

Erst nach Implementierung und Prüfung der Abfragen:

1. Verbindung mit dokumentierter serieller Konfiguration öffnen.
2. Bootmeldung oder Controllerkennung erfassen.
3. Nur lesende Abfragen für Status und Einstellungen einzeln senden.
4. Antwort, Zeit bis zur Antwort und Verbindungszustand protokollieren.
5. Verbindung schließen, erneut öffnen und den Ablauf wiederholen.

Die tatsächlich unterstützten Abfragen werden aus dem beobachteten Verhalten und der Firmwaredokumentation abgeleitet. Ein Protokollbefehl gilt nicht allein deshalb als sicher, weil er in einer anderen GRBL-Variante verfügbar ist.

**Bestanden, wenn:** Antworten reproduzierbar sind, keine Bewegung oder Laseremission auftritt und Verbindungsfehler erkennbar gemeldet werden.

### v0.1.0 – Kompatibilität nachweisen

- Mindestens drei vollständige Verbindungs- und Abfragezyklen protokollieren.
- Abweichungen zwischen erwartetem und beobachtetem Verhalten festhalten.
- Tatsächlich bestätigte Werte in das Geräteprofil übernehmen.
- Unbekannte Werte weiterhin als unbekannt führen.

## Ergebnisprotokoll

Die Einträge werden erst bei einem realen Test ergänzt. Zugangsdaten, private Pfade und individuelle Hardwarekennungen gehören nicht in ein öffentliches Testergebnis.

| Lauf | Datum | Ubuntu-Version | Erkannter Port | Firmwareantwort | Ergebnis / Bemerkung |
| --- | --- | --- | --- | --- | --- |
| – | noch nicht ausgeführt | – | – | – | Testprogramm wird ab v0.0.2 ergänzt |
