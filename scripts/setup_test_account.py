#!/usr/bin/env python3
"""
Verbrannte Zone 3 - Test Account Setup
Erstellt einen Test-Account auf der Original-Website für Reverse Engineering.
"""

import sys
import os
from pathlib import Path


def print_banner():
    """Banner anzeigen"""
    print("=" * 70)
    print("🎮 Verbrannte Zone 3 - Test Account Setup")
    print("=" * 70)
    print()
    print("Dieses Skript erstellt einen Test-Account auf der Original-Website")
    print("für Reverse Engineering-Zwecke.")
    print()
    print("⚠️  WICHTIG:")
    print("   - Nur für private, nicht-kommerzielle Nutzung")
    print("   - Respektvolle API-Nutzung (Rate Limiting)")
    print("   - Keine kommerzielle Verwertung")
    print()


def get_user_credentials():
    """Benutzer-Eingaben für Test-Account"""
    print("📝 Bitte gib die Daten für den Test-Account ein:")
    print("-" * 70)
    
    # Generiere einen eindeutigen Test-Namen
    import time
    timestamp = int(time.time()) % 10000
    
    default_nick = f"RE_Test_{timestamp}"
    default_email = f"re-test-{timestamp}@example.com"
    
    nick = input(f"   Spielername [{default_nick}]: ").strip() or default_nick
    password = input(f"   Passwort [{nick.lower()}123]: ").strip() or f"{nick.lower()}123"
    email = input(f"   E-Mail [{default_email}]: ").strip() or default_email
    
    print("-" * 70)
    print(f"\n✅ Zusammenfassung:")
    print(f"   Spielername: {nick}")
    print(f"   Passwort: {'*' * len(password)}")
    print(f"   E-Mail: {email}")
    print()
    
    confirm = input("   Daten korrekt? (j/N): ").strip().lower()
    
    if confirm != 'j':
        print("   ❌ Abgebrochen.")
        sys.exit(0)
    
    return nick, password, email


def create_manual_instructions(nick, password, email):
    """Anleitung zum manuellen Erstellen des Accounts"""
    
    instructions = f"""
======================================================================
📋 ANLEITUNG: Test-Account manuell erstellen

1. Öffne die Website: https://v3.verbranntezone.ch/anmelden.php

2. Fülle das Formular aus:
   ┌─────────────────────────────────────┐
   │ Spielername: {nick:<28}│
   │ Passwort:    {'*' * len(password):<28}│
   │ E-Mail:      {email:<28}│
   │ (ggf. weitere Felder)               │
   └─────────────────────────────────────┘

3. Klicke auf "Anmelden" oder "Erstellen"

4. Prüfe deine E-Mail ({email}) auf Aktivierungslink

5. Aktiviere den Account über den Link in der E-Mail

6. Logge dich ein mit:
   - Spielername: {nick}
   - Passwort: {password}

======================================================================
🔧 AUTOMATISCHER MODUS (optional)

Um den Account automatisch zu erstellen, führe aus:

    python3 login_analyzer.py https://v3.verbranntezone.ch \
        login_analysis {nick} {password}

======================================================================
📊 NÄCHSTE SCHRITTE NACH DEM LOGIN:

1. Network Tab der Browser DevTools öffnen (F12)
2. Alle API-Requests loggen
3. Session-Cookies speichern
4. Spielaktionen analysieren

======================================================================
"""
    
    return instructions


def main():
    print_banner()
    
    # Prüfen ob Output-Verzeichnis existiert
    output_dir = Path('login_analysis')
    output_dir.mkdir(exist_ok=True)
    
    # Benutzer-Eingaben
    nick, password, email = get_user_credentials()
    
    # Anleitung speichern
    instructions = create_manual_instructions(nick, password, email)
    
    # In Datei speichern
    instructions_file = output_dir / 'ACCOUNT_SETUP_INSTRUCTIONS.txt'
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    # Credentials (nur als Beispiel, NICHT echt speichern!)
    credentials_example = {
        'example_account': {
            'nick': nick,
            'password_example': f"{password[:2]}***{password[-2:]}",  # Nur zur Veranschaulichung
            'email': email,
            'created_at': None  # Wird später ausgefüllt
        }
    }
    
    credentials_file = output_dir / 'credentials_example.json'
    with open(credentials_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(credentials_example, f, indent=2)
    
    # Anleitung anzeigen
    print(instructions)
    
    print(f"\n💾 Anleitung gespeichert: {instructions_file}")
    print(f"📄 Beispiel-Credentials: {credentials_file}")
    print()
    print("=" * 70)
    print("✅ Setup abgeschlossen!")
    print("=" * 70)


if __name__ == '__main__':
    main()
