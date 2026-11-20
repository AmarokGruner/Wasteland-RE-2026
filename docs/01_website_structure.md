# Verbrannte Zone 3 - Website Struktur Analyse

**Datum:** 20. November 2026  
**Quelle:** https://v3.verbranntezone.ch  
**Crawler:** VZ-RE-Crawler v1.0

---

## 📊 Crawl-Ergebnisse

| Metrik | Wert |
|--------|------|
| **Gecrawlte Seiten** | 14 HTML-Seiten + 6 Bilder |
| **Gesamtgröße** | ~1.2 MB |
| **Design-Assets** | 3 PNG-Bilder (Navigation) |
| **Screenshots** | 6 JPG-Bilder |

---

## 🗂️ Seiten-Struktur

### Hauptseiten (Navigation)

| Seite | Pfad | Größe | Beschreibung |
|-------|------|-------|--------------|
| **Startseite** | `/` oder `/index.php` | 16.5 KB | Login + Navigation |
| **News** | `/news.php` | 12.8 KB | Aktuelle Nachrichten |
| **Geschichte** | `/geschichte.php` | 13.4 KB | Spiel-Lore/Story |
| **Spiel Infos** | `/infos.php` | 15.3 KB | Allgemeine Informationen |
| **Regeln** | `/regeln.php` | 23.7 KB | Spielregeln (größte Seite) |
| **Screenshots** | `/screenshots.php` | 11.6 KB | Spiel-Screenshots |

### Spieler-Seiten

| Seite | Pfad | Größe | Beschreibung |
|-------|------|-------|--------------|
| **Anmelden** | `/anmelden.php` | 11.5 KB | Neue Spieler erstellen |
| **Aktivieren** | `/aktivieren.php` | 11.7 KB | Spieler-Aktivierung |
| **Passwort** | `/passwort.php` | 11.3 KB | Passwort vergessen |

### Info-Seiten

| Seite | Pfad | Größe | Beschreibung |
|-------|------|-------|--------------|
| **Browsertest** | `/browsertest.php` | 11.4 KB | Browser-Kompatibilität |
| **Kontakt** | `/kontakt.php` | 11.6 KB | Kontaktinformationen |
| **Impressum** | `/impressum.php` | 10.8 KB | Rechtliches |
| **Links** | `/links.php` | 12.0 KB | Externe Links |
| **Datenschutz** | `/datenschutz.php` | 13.0 KB | Datenschutz-Bestimmungen |

---

## 🎨 Design-Assets

### Navigation (Links)
```
/design/vz3nt.png  - 23 KB - Obere Navigation (Header links)
/design/vz3nb.png  - 35 KB - Untere Navigation (Menü links)
```

### Header
```
/design/vz3t3new.png - 120 KB - Haupt-Header Bild (Mitte)
```

### Screenshots
```
/shots/shot01.jpg - 139 KB
/shots/shot02.jpg - 151 KB
/shots/shot03.jpg - 130 KB
/shots/shot04.jpg - 159 KB
/shots/shot05.jpg - 127 KB
/shots/shot06.jpg - 136 KB
```

### Icons
```
/favicon.png     - 2.5 KB
/favicon.ico     - Fallback Icon
```

---

## 🏗️ HTML-Struktur

### Grundlegendes Layout (index.php)

```html
<table width="100%">
  <tr height="150">
    <!-- Linke Navigation (168px) -->
    <td width="168">
      <img src="design/vz3nt.png"> <!-- Header -->
      <form>...</form>              <!-- Login -->
      <img src="design/vz3nb.png">  <!-- Menü -->
    </td>
    
    <!-- Hauptinhalt (640px+) -->
    <td min-width="640">
      <!-- Dynamischer Inhalt -->
    </td>
    
    <!-- Rechte Leiste (5px) -->
    <td width="5"></td>
  </tr>
  
  <!-- Untere Navigation (fortgesetzt) -->
  <tr>
    <td rowspan="2">
      <img src="design/vz3nb.png"> <!-- Unteres Menü -->
    </td>
  </tr>
</table>
```

### CSS-Design (Original)

**Farbschema:**
- Hintergrund: `#C8887C` (Terrakotta)
- Primär: `#8C5D52` (Dunkles Braun/Rot)
- Text: `#000000` (Schwarz)
- Formular: `#211818` (Sehr dunkel)

**Schriftart:** Tahoma, 10-16pt

**Besondere Stile:**
- `.kontur` - Text mit starkem Schatten (8px in alle Richtungen)
- `.link` - Navigationslinks mit Hover-Effekt
- `.news td` - News-Boxen mit abgerundeten Rändern

---

## 🔐 Authentifizierung

### Login-Prozess
1. **Login-Formular** auf `index.php`
2. **POST-Daten:**
   - `nick` - Spielername
   - `passwort` - Passwort (hidden input)
   - `lsguid` - Session/Tracking-ID
3. **Session:** Cookies werden gesetzt
4. **Erfolg:** Weiterleitung zum Spiel-Dashboard

### Spieler-Erstellung (`anmelden.php`)
- Formular für neue Spieler
- Aktivierung über E-Mail (`aktivieren.php`)

---

## 📝 Zusammenfassung

Die Verbrannte Zone 3 ist eine **klassische PHP-basierte Website** mit:
- ✅ Einfacher, tabellenbasierten Layout (älteres Design)
- ✅ Server-seitigem Rendering (kein SPA)
- ✅ Cookie-basierter Authentifizierung
- ✅ Statischem Design mit PNG-Navigation
- ✅ 14 funktionale Seiten

**Technologien:**
- PHP (server-side)
- HTML 4.01 / XHTML
- CSS (inline + style tags)
- JavaScript (minimal)
- MySQL/MariaDB (vermutet, Datenbank `verbrannte_zone.db`)

---

**Nächste Schritte:**
1. API-Endpunkte analysieren (Login, Spielaktionen)
2. Datenbank-Struktur reverse-engineeren
3. Spielmechaniken dokumentieren
