# Verbrannte Zone 3 - Reverse Engineering Phasen

**Datum:** 20. November 2026  
**Status:** Phase 1 aktiv

---

## 📋 Gesamt-Phasenplan

```
Phase 1: Website Analyse & Extraktion (AKTIV)
    ↓
Phase 2: Login & Session Analyse
    ↓
Phase 3: Spielmechaniken Reverse Engineering
    ↓
Phase 4: Datenbank-Struktur Extraktion
    ↓
Phase 5: Lokaler Server Aufbau
    ↓
Phase 6: Testing & Validierung
    ↓
Phase 7: Dokumentation Abschluss
    ↓
Phase 8: Fusion mit Wasteland-2026-new (separates Repo)
```

---

## 🔍 Phase 1: Website Analyse & Extraktion (AKTIV)

**Ziel:** Alle öffentlichen Seiten und Assets extrahieren

### Aufgaben:
- [x] Website crawlen (14 Seiten + 6 Bilder) ✅
- [x] API-Endpunkte identifizieren (14 Endpunkte) ✅
- [x] HTML/CSS/JS Struktur dokumentieren ✅
- [ ] Design-Assets lokal speichern (3 PNG + 6 JPG)
- [ ] JavaScript-Code analysieren (falls vorhanden)

### Deliverables:
- `crawled_site/` - Alle HTML-Seiten
- `api_analysis/api_endpoints.json` - Strukturierte API-Daten
- `docs/01_website_structure.md` - Seiten-Analyse
- `docs/02_api_endpoints.md` - API-Dokumentation

### Status: 80% abgeschlossen

---

## 🔐 Phase 2: Login & Session Analyse

**Ziel:** Authentifizierungs-Prozess vollständig verstehen und lokal nachbilden

### Aufgaben:
- [ ] Spieler-Account auf v3.verbranntezone.ch erstellen
- [ ] Login-Prozess mit DevTools analysieren (Network Tab)
- [ ] Session-Cookies extrahieren und speichern
- [ ] Login-Formular Parameter dokumentieren (nick, passwort, lsguid)
- [ ] Session-Management verstehen (PHPSESSID)
- [ ] Logout-Prozess analysieren
- [ ] Gespeicherte Credentials sicher verwalten

### Erwartete Erkenntnisse:
```python
# Typischer Login-Flow:
1. POST /index.php mit {nick, passwort, lsguid}
2. Server validiert Credentials gegen Datenbank
3. Server setzt PHPSESSID Cookie
4. Server speichert Spieler-Daten in $_SESSION
5. Redirect zum Spiel-Dashboard (gleiche URL, anderer Inhalt)

# Session-Wiederverwendung:
headers = {
    'Cookie': 'PHPSESSID=abc123...',
}
response = requests.get('https://v3.verbranntezone.ch/index.php', headers=headers)
```

### Deliverables:
- `docs/04_login_session.md` - Authentifizierungs-Dokumentation
- `scripts/login_analyzer.py` - Login-Testing Skript
- `assets/credentials.example` - Beispiel-Credentials (NICHT echt!)

### Status: 0% - Wartet auf Account-Erstellung

---

## 🎮 Phase 3: Spielmechaniken Reverse Engineering

**Ziel:** Alle spielbaren Aktionen und Mechaniken identifizieren

### Aufgaben:
- [ ] Nach Login: Spiel-Dashboard analysieren
- [ ] Alle Navigations-Menüs dokumentieren (Ressourcen, Einheiten, Gebäude, etc.)
- [ ] Spielaktionen identifizieren:
  - [ ] Einheiten bewegen (Befehl senden)
  - [ ] Gebäude bauen/upgrade
  - [ ] Ressourcen sammeln/tauschen
  - [ ] Angriffe starten
  - [ ] Nachrichten senden/empfangen
- [ ] Alle POST-Requests im Network Tab loggen
- [ ] Request/Response-Struktur dokumentieren

### Typische Browsergame-Aktionen (Beispiele):
```python
# Beispiel: Einheit bewegen
action_payload = {
    'action': 'move_unit',
    'unit_id': 123,
    'x': 45,
    'y': 67,
    'turn': 15
}

# Beispiel: Gebäude bauen
action_payload = {
    'action': 'build',
    'building_type': 'barracks',
    'x': 10,
    'y': 20,
    'cost': {'holz': 100, 'stein': 50}
}

# Beispiel: Angriff
action_payload = {
    'action': 'attack',
    'target_unit_id': 456,
    'attacker_unit_id': 123
}
```

### Deliverables:
- `docs/05_game_mechanics.md` - Alle Spielmechaniken
- `scripts/action_analyzer.py` - API Request Logger
- `data/game_actions.json` - Dokumentierte Aktionen

### Status: 0% - Wartet auf Phase 2

---

## 🗄️ Phase 4: Datenbank-Struktur Extraktion

**Ziel:** Datenbankschema und -inhalte reverse-engineeren

### Aufgaben:
- [ ] Vermutete Tabellen identifizieren (aus HTML/JS)
  - `players` - Spieler-Daten
  - `units` - Einheiten
  - `buildings` - Gebäude
  - `resources` - Ressourcen
  - `messages` - Nachrichten
  - `map` / `tiles` - Spielkarte
- [ ] Datenstrukturen aus API-Responses ableiten
- [ ] Beziehungen zwischen Tabellen verstehen
- [ ] Beispiel-Daten extrahieren (wenn möglich)

### Erwartete Datenbank-Struktur:
```sql
-- Vermutetes Schema (muss validiert werden)

CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    nick VARCHAR(50),
    passwort_hash VARCHAR(255),
    email VARCHAR(100),
    aktiviert BOOLEAN,
    created_at DATETIME,
    last_login DATETIME
);

CREATE TABLE resources (
    player_id INTEGER,
    holz INTEGER DEFAULT 0,
    stein INTEGER DEFAULT 0,
    nahrung INTEGER DEFAULT 0,
    gold INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE units (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    unit_type VARCHAR(50),
    x INTEGER,
    y INTEGER,
    health INTEGER,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE buildings (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    building_type VARCHAR(50),
    x INTEGER,
    y INTEGER,
    level INTEGER DEFAULT 1,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE map_tiles (
    x INTEGER,
    y INTEGER,
    terrain_type VARCHAR(50),
    PRIMARY KEY (x, y)
);
```

### Deliverables:
- `docs/06_database_schema.md` - Datenbank-Dokumentation
- `scripts/db_analyzer.py` - Schema Extraktor
- `data/schema.sql` - Vermutetes SQL-Schema

### Status: 0% - Wartet auf Phase 3

---

## 🖥️ Phase 5: Lokaler Server Aufbau

**Ziel:** Spiel lokal zum Laufen bringen (ohne Original-Server)

### Aufgaben:
- [ ] PHP-Server aufsetzen (oder Python/Node.js Alternative)
- [ ] Datenbank lokal erstellen (SQLite für Einfachheit)
- [ ] Login-Funktionalität implementieren
- [ ] Spielaktionen als API endpunkte bereitstellen
- [ ] Session-Management nachbilden

### Technologie-Entscheidungen:
```python
# Option A: PHP (originalgetreu)
# - XAMPP/MAMP aufsetzen
# - Original-Code anpassen
# - Vorteil: Nah am Original

# Option B: Python Flask/FastAPI (modern)
from flask import Flask, session, request

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/login', methods=['POST'])
def login():
    nick = request.form['nick']
    password = request.form['passwort']
    
    # Validierung gegen Datenbank
    player = db.query("SELECT * FROM players WHERE nick=?", (nick,))
    if player and verify_password(password, player.passwort_hash):
        session['player_id'] = player.id
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Option C: Node.js/Express
# - Modern, JavaScript-basiert
# - Gut für Echtzeit-Spiele
```

### Deliverables:
- `server/` - Lokaler Server-Code
- `server/config.json` - Konfiguration
- `server/database/` - Lokale Datenbank
- `docs/07_local_server.md` - Setup-Anleitung

### Status: 0% - Wartet auf Phase 4

---

## 🧪 Phase 6: Testing & Validierung

**Ziel:** Funktionierenden lokalen Server validieren

### Aufgaben:
- [ ] Login mit Test-Account testen
- [ ] Alle Spielaktionen gegen lokalen Server testen
- [ ] Session-Management validieren
- [ ] Fehlerbehandlung testen
- [ ] Performance unter Last testen

### Test-Szenarien:
```python
# Beispiel-Tests (mit pytest)

def test_login_success():
    """Erfolgreicher Login"""
    response = client.post('/login', data={
        'nick': 'testplayer',
        'passwort': 'test123'
    })
    assert response.status_code == 200
    assert 'player_id' in session

def test_login_invalid_password():
    """Falsches Passwort"""
    response = client.post('/login', data={
        'nick': 'testplayer',
        'passwort': 'wrong_password'
    })
    assert response.status_code == 401

def test_move_unit():
    """Einheit bewegen"""
    client.post('/login', data={'nick': 'testplayer', 'passwort': 'test123'})
    response = client.post('/action/move', json={
        'unit_id': 1,
        'x': 10,
        'y': 20
    })
    assert response.status_code == 200
    assert response.json['success'] == True

def test_session_timeout():
    """Session-Timeout nach Inaktivität"""
    # Login
    client.post('/login', data={'nick': 'testplayer', 'passwort': 'test123'})
    
    # Simuliere Zeitverzögerung (oder setze Session-Expires)
    
    # Zugriff sollte fehlschlagen
    response = client.get('/game/state')
    assert response.status_code == 401
```

### Deliverables:
- `tests/` - Test-Suite
- `docs/08_testing.md` - Test-Dokumentation
- `test_results.log` - Test-Ergebnisse

### Status: 0% - Wartet auf Phase 5

---

## 📚 Phase 7: Dokumentation Abschluss

**Ziel:** Vollständige Reverse-Engineering-Dokumentation

### Aufgaben:
- [ ] Alle bisherigen Docs zusammenführen
- [ ] Architektur-Diagramme erstellen
- [ ] API-Referenz vervollständigen
- [ ] Setup-Anleitungen schreiben
- [ ] Known Issues dokumentieren

### Deliverables:
- `docs/09_architecture.md` - System-Architektur
- `docs/10_api_reference.md` - Vollständige API-Doku
- `docs/README_COMPLETE.md` - Zusammenfassung

### Status: 0% - Wartet auf Phasen 1-6

---

## 🔀 Phase 8: Fusion mit Wasteland-2026-new (SEPARATES REPO)

**Ziel:** Reverse Engineering Ergebnisse mit bestehendem Nachbau fusionieren

### Repository: **Wasteland-Fusion-2026** (wird später erstellt)

### Aufgaben:
- [ ] Neues Repository `Wasteland-Fusion-2026` erstellen
- [ ] Code aus `Wasteland-RE-2026` importieren
- [ ] Code aus `Wasteland-2026-new` importieren
- [ ] Konflikte auflösen und kombinieren
- [ ] Moderne Technologien integrieren (React/Vue, etc.)
- [ ] Multiplayer-Funktionalität aufbauen

### Deliverables:
- `Wasteland-Fusion-2026/` - Fusioniertes Repository
- Vollständiges, modernes Browsergame

### Status: 🔲 Nicht gestartet - Wird später erstellt

---

## 📊 Fortschritts-Übersicht

| Phase | Titel | Status | Abgeschlossen |
|-------|-------|--------|---------------|
| **1** | Website Analyse & Extraktion | 🟡 80% | Teilweise ✅ |
| **2** | Login & Session Analyse | ⚪ 0% | ❌ |
| **3** | Spielmechaniken RE | ⚪ 0% | ❌ |
| **4** | Datenbank-Struktur | ⚪ 0% | ❌ |
| **5** | Lokaler Server | ⚪ 0% | ❌ |
| **6** | Testing & Validierung | ⚪ 0% | ❌ |
| **7** | Dokumentation Abschluss | ⚪ 0% | ❌ |
| **8** | Fusion (separates Repo) | 🔲 0% | ❌ |

---

## 🚀 Nächste Sofort-Aktionen:

1. **Sofort:** Spieler-Account auf v3.verbranntezone.ch erstellen (manuell)
2. **Danach:** Login-Prozess mit DevTools analysieren (Phase 2)
3. **Dann:** Spielaktionen loggen und dokumentieren (Phase 3)

---

**Erstellt:** 20. November 2026  
**Letzte Aktualisierung:** 20. November 2026
