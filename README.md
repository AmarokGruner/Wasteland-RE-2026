# Verbrannte Zone 3 - Reverse Engineering

## 🎯 Ziel

Vollständiges Reverse Engineering der **Verbrannten Zone 3** (https://v3.verbranntezone.ch) um das Spiel lokal zum Laufen zu bringen.

**Phase 1:** Reverse Engineering & zum Laufen bringen  
**Phase 2:** Fusion mit Wasteland-2026-new (später)

---

## 📋 Status

### Phase 1: Reverse Engineering
- [x] Website strukturell analysiert (14 Seiten + Assets)
- [x] HTML/CSS/JS extrahiert
- [x] API-Endpunkte identifiziert (14 Endpunkte)
- [ ] Datenbank-Struktur reverse-engineeren
- [ ] Spielmechaniken dokumentieren
- [ ] Lokaler Server zum Laufen bringen

### Phase 2: Fusion (später)
- [ ] Code mit Wasteland-2026-new zusammenführen
- [ ] Moderne Technologien integrieren
- [ ] Multiplayer-Funktionalität aufbauen

---

## 🏗️ Projektstruktur

```
wasteland-re-2026/
├── README.md              # Diese Datei
├── docs/                  # Dokumentation der Analysen
│   ├── 01_website_structure.md
│   ├── 02_api_endpoints.md
│   └── ...
├── assets/                # Externe Assets (Bilder, Fonts)
├── scripts/               # Analyse-Skripte
│   ├── crawl_site.py      # Website crawler
│   └── analyze_api.py     # API analyzer
├── crawled_site/          - Gecrawlte Seiten (HTML)
└── api_analysis/          - API-Daten (JSON)
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

### 3. Dokumentation lesen
Siehe `docs/` Ordner für detaillierte Analysen.

---

## 📊 Aktuelle Ergebnisse (20.11.2026)

- **Seiten gecrawlt:** 14 HTML-Seiten + 6 Bilder
- **API Endpunkte:** 14 identifiziert
- **Design-Assets:** 3 PNG (Navigation) + 6 JPG (Screenshots)
- **Gesamtgröße:** ~1.2 MB

---

## ⚠️ Rechtlicher Hinweis

Dieses Projekt dient **ausschließlich Bildungszwecken**.
- Keine kommerzielle Nutzung
- Respektvolle API-Nutzung (Rate Limiting)
- Nur private, nicht-kommerzielle Zwecke

---

**Original:** Verbrannte Zone 3 by Sandro Barbieri  
**Website:** https://v3.verbranntezone.ch
