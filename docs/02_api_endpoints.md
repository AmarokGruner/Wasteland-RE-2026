# Verbrannte Zone 3 - API Endpunkte Analyse

**Datum:** 20. November 2026  
**Quelle:** https://v3.verbranntezone.ch  
**Analyzer:** VZ-API-Analyzer v1.0

---

## 📊 Analyse-Ergebnisse

| Kategorie | Anzahl |
|-----------|--------|
| **Gesamt Endpunkte** | 14 |
| **PHP-Seiten** | 14 |
| **Formulare** | 2 (Login, Anmeldung) |
| **JavaScript API-Calls** | 0 (keine gefunden) |

---

## 🔗 Alle Endpunkte

### Öffentliche Seiten (GET)

| Endpoint | Methode | Status | Größe | Beschreibung |
|----------|---------|--------|-------|--------------|
| `/index.php` | GET | 200 | 16.5 KB | Startseite + Login |
| `/news.php` | GET | 200 | 12.8 KB | News-Übersicht |
| `/geschichte.php` | GET | 200 | 13.4 KB | Spiel-Hintergrund |
| `/infos.php` | GET | 200 | 15.3 KB | Spiel-Informationen |
| `/regeln.php` | GET | 200 | 23.7 KB | Spielregeln (umfangreich) |
| `/screenshots.php` | GET | 200 | 11.6 KB | Screenshots-Galerie |
| `/browsertest.php` | GET | 200 | 11.4 KB | Browser-Check |
| `/kontakt.php` | GET | 200 | 11.6 KB | Kontaktformular |
| `/impressum.php` | GET | 200 | 10.8 KB | Impressum |
| `/links.php` | GET | 200 | 12.0 KB | Externe Links |
| `/datenschutz.php` | GET | 200 | 13.0 KB | Datenschutz |

### Spieler-Seiten

| Endpoint | Methode | Status | Größe | Beschreibung |
|----------|---------|--------|-------|--------------|
| `/anmelden.php` | GET/POST | 200 | 11.5 KB | Neue Spieler erstellen |
| `/aktivieren.php` | GET/POST | 200 | 11.7 KB | Spieler aktivieren |
| `/passwort.php` | GET/POST | 200 | 11.3 KB | Passwort zurücksetzen |

---

## 🔐 Authentifizierte Endpunkte (POST)

### Login (`index.php`)
```http
POST /index.php HTTP/1.1
Content-Type: application/x-www-form-urlencoded

nick=Spielername&passwort=geheim&lsguid=false
```

**Response:**
- Erfolg: Weiterleitung zum Spiel-Dashboard (gleiche URL, anderer Inhalt)
- Fehler: Login-Fehlermeldung auf index.php

**Session:**
- PHPSESSID Cookie wird gesetzt
- Spieler-Daten im Session-Objekt gespeichert

---

## 🎮 Vermutete Spiel-API (nicht öffentlich dokumentiert)

Basierend auf der HTML-Struktur und typischen Browsergame-Mustern:

### Mögliche Endpunkte

| Vermuteter Endpoint | Methode | Beschreibung |
|---------------------|---------|--------------|
| `/index.php?action=move` | POST | Einheit bewegen |
| `/index.php?action=build` | POST | Gebäude bauen |
| `/index.php?action=attack` | POST | Angriff starten |
| `/index.php?action=trade` | POST | Handel |
| `/nachrichten.php` | GET/POST | Nachrichten lesen/schreiben |

**Hinweis:** Diese Endpunkte müssen durch aktives Spiel-Testing verifiziert werden.

---

## 📝 Formular-Analyse

### Login-Formular (index.php)
```html
<form method="POST" action="index.php">
  <input name="nick" type="text" required>
  <input name="passwort" type="password" required>
  <input name="lsguid" type="hidden" value="false">
  <input type="submit" value="login">
</form>
```

**Parameter:**
- `nick` (string, required) - Spielername
- `passwort` (string, required) - Passwort
- `lsguid` (string, hidden) - Session/Tracking-ID

### Anmelden-Formular (anmelden.php)
```html
<form method="POST" action="anmelden.php">
  <!-- Vermutete Felder: -->
  <input name="nick" type="text">
  <input name="passwort" type="password">
  <input name="email" type="email">
  <!-- ... weitere Felder -->
</form>
```

---

## 🔍 Technische Details

### Content-Type
- Alle Seiten: `text/html`
- Keine JSON-APIs gefunden (reines Server-Side Rendering)

### Session Management
- PHP Sessions (`PHPSESSID` Cookie)
- Keine Token-basierte Authentifizierung (altersloses System)

### Rate Limiting
- Nicht offensichtlich implementiert
- Empfohlen: Max 1 Request/Sekunde für Tests

---

## ⚠️ Sicherheits-Bewertung

| Aspekt | Bewertung | Hinweis |
|--------|-----------|---------|
| **HTTPS** | ❌ Nein | Alle URLs sind HTTP (nicht sicher) |
| **Password Hashing** | ? Unbekannt | Server-seitig |
| **SQL Injection** | ⚠️ Möglich | Älteres PHP-System |
| **XSS** | ⚠️ Möglich | Keine moderne Escaping |
| **CSRF** | ❌ Kein Token | Keine CSRF-Schutzmechanismen |

---

## 📋 Zusammenfassung

Die Verbrannte Zone 3 verwendet ein **klassisches PHP-basiertes System** ohne moderne API:
- ✅ Keine REST/GraphQL APIs
- ✅ Reines Server-Side Rendering
- ✅ Cookie-basierte Sessions
- ⚠️ Veraltetes Sicherheitsniveau (für heutige Standards)

**Für Reverse Engineering empfohlen:**
1. Login mit Test-Account durchführen
2. Network Tab der DevTools beobachten
3. Alle POST-Requests loggen
4. Session-Cookies speichern und wiederverwenden

---

**Nächste Schritte:**
1. Aktives Spiel-Testing (mit Account)
2. WebSocket-Kommunikation analysieren (falls vorhanden)
3. Datenbank-Struktur extrahieren
