# Verbrannte Zone 3 - Reverse Engineering

## 🎯 Ziel

Vollständiges Reverse Engineering der **Verbrannten Zone 3** (https://v3.verbranntezone.ch) um das Spiel lokal zum Laufen zu bringen.

**Phase 1:** Reverse Engineering & zum Laufen bringen  
**Phase 2:** Fusion mit Wasteland-2026-new (später, separates Repo)

---

## 📋 Status

### Phase 1: Website Analyse & Extraktion (AKTIV)
- [x] Website strukturell analysiert (14 Seiten + Assets)
- [x] HTML/CSS/JS extrahiert
- [x] API-Endpunkte identifiziert (14 Endpunkte)
- [ ] Design-Assets lokal speichern
- [ ] JavaScript-Code analysieren

### Phase 2: Login & Session Analyse (NÄCHST)
- [ ] Spieler-Account auf v3.verbranntezone.ch erstellen
- [ ] Login-Prozess mit DevTools analysieren
- [ ] Session-Cookies extrahieren und speichern
- [ ] Login-Formular Parameter dokumentieren
- [ ] Session-Management verstehen

### Phase 3: Spielmechaniken Reverse Engineering
- [ ] Nach Login: Spiel-Dashboard analysieren
- [ ] Alle Navigations-Menüs dokumentieren
- [ ] Spielaktionen identifizieren (Bewegen, Bauen, Angreifen)
- [ ] Alle POST-Requests im Network Tab loggen

### Phase 4: Datenbank-Struktur Extraktion
- [ ] Vermutete Tabellen identifizieren
- [ ] Datenstrukturen aus API-Responses ableiten
- [ ] Beziehungen zwischen Tabellen verstehen

### Phase 5: Lokaler Server Aufbau
- [ ] PHP/Python/Node.js Server aufsetzen
- [ ] Datenbank lokal erstellen (SQLite)
- [ ] Login-Funktionalität implementieren
- [ ] Spielaktionen als API endpunkte bereitstellen

### Phase 6: Testing & Validierung
- [ ] Login mit Test-Account testen
- [ ] Alle Spielaktionen gegen lokalen Server testen
- [ ] Session-Management validieren

### Phase 7: Dokumentation Abschluss
- [ ] Alle Docs zusammenführen
- [ ] Architektur-Diagramme erstellen
- [ ] API-Referenz vervollständigen

### Phase 8: Fusion (separates Repo: Wasteland-Fusion-2026)
- [ ] Neues Repository erstellen
- [ ] Code aus RE-2026 + 2026-new kombinieren
- [ ] Moderne Technologien integrieren

---

## 🏗️ Projektstruktur

```
wasteland-re-2026/
├── README.md              # Diese Datei
├── docs/                  # Dokumentation der Analysen
│   ├── 01_website_structure.md
│   ├── 02_api_endpoints.md
│   └── 03_reverse_engineering_phases.md
├── scripts/               # Analyse-Skripte
│   ├── crawl_site.py      # Website crawler
│   ├── analyze_api.py     # API analyzer
│   ├── login_analyzer.py  # Login & Session Analyzer
│   └── setup_test_account.py # Test Account Setup
├── crawled_site/          - Gecrawlte Seiten (HTML)
├── api_analysis/          - API-Daten (JSON)
└── login_analysis/        - Login-Analyse
```

---

## 🚀 Schnellstart

### 1. Website crawlen
```bash
cd scripts
python3 crawl_site.py https://v3.verbranntezone.ch
```

### 2. API analysieren
```bash
python3 analyze_api.py https://v3.verbranntezone.ch
```

### 3. Test-Account erstellen (manuell)
```bash
# Anleitung siehe: login_analysis/ACCOUNT_SETUP_INSTRUCTIONS.txt
```

### 4. Login analysieren (automatisch)
```bash
python3 login_analyzer.py https://v3.verbranntezone.ch login_analysis <nick> <password>
```

---

## 📊 Aktuelle Ergebnisse (20.11.2026)

- **Seiten gecrawlt:** 14 HTML-Seiten + 6 Bilder ✅
- **API Endpunkte:** 14 identifiziert ✅
- **Design-Assets:** 3 PNG (Navigation) + 6 JPG (Screenshots)
- **Gesamtgröße:** ~1.2 MB
- **Login Analyzer:** Implementiert ✅
- **Phasenplan:** Alle 8 Phasen definiert ✅

---

## ⚠️ Rechtlicher Hinweis

Dieses Projekt dient **ausschließlich Bildungszwecken**.
- Keine kommerzielle Nutzung
- Respektvolle API-Nutzung (Rate Limiting)
- Nur private, nicht-kommerzielle Zwecke

---

**Original:** Verbrannte Zone 3 by Sandro Barbieri  
**Website:** https://v3.verbranntezone.ch
