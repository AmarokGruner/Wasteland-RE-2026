#!/usr/bin/env python3
"""
Verbrannte Zone 3 - Login Analyzer
Analysiert den Login-Prozess und verwaltet Sessions.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.parse
import http.cookiejar


class LoginAnalyzer:
    def __init__(self, base_url, output_dir):
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Session-Management
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        
        self.session_data = {
            'base_url': self.base_url,
            'logged_in': False,
            'player_nick': None,
            'session_cookies': {},
            'login_history': [],
            'analyzed_at': None
        }
    
    def create_account(self, nick, password, email):
        """Neuen Spieler auf der Original-Website erstellen"""
        print(f"\n👤 Erstelle neuen Account: {nick}")
        print("=" * 60)
        
        try:
            # 1. Anmelden-Seite laden
            print("\n[1/4] Lade Anmeldeseite...")
            req = urllib.request.Request(
                f"{self.base_url}/anmelden.php",
                headers={'User-Agent': 'Mozilla/5.0 (VZ-Login-Analyzer/1.0)'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('iso-8859-1', errors='replace')
                print(f"   ✅ Seite geladen ({len(html)} bytes)")
            
            # 2. Formular-Parameter extrahieren
            print("\n[2/4] Analysiere Anmeldeformular...")
            form_params = self.extract_form_parameters(html, 'anmelden.php')
            
            for param in form_params:
                print(f"   📝 {param['name']} ({param['type']})")
            
            # 3. Account erstellen
            print("\n[3/4] Erstelle Account...")
            form_data = urllib.parse.urlencode({
                'nick': nick,
                'passwort': password,
                'email': email,
                # Weitere Parameter je nach Formular
            }).encode('iso-8859-1')
            
            req = urllib.request.Request(
                f"{self.base_url}/anmelden.php",
                data=form_data,
                headers={
                    'User-Agent': 'Mozilla/5.0 (VZ-Login-Analyzer/1.0)',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result_html = response.read().decode('iso-8859-1', errors='replace')
                print(f"   ✅ Account erstellt ({len(result_html)} bytes)")
                
                # Prüfen ob Erfolgsmeldung
                if 'aktivieren' in result_html.lower() or 'bestätigen' in result_html.lower():
                    print("   📧 Aktivierungs-E-Mail wurde gesendet!")
                elif 'existiert' in result_html.lower() or 'bereits' in result_html.lower():
                    print("   ⚠️ Account existiert bereits!")
            
            # 4. Session speichern
            self.save_session_cookies()
            
            print(f"\n✅ Account '{nick}' erfolgreich erstellt!")
            print(f"   ⚠️ Aktivierungs-E-Mail an {email} gesendet")
            
            return {'success': True, 'nick': nick, 'email': email}
            
        except Exception as e:
            print(f"\n❌ Fehler beim Erstellen des Accounts: {e}")
            return {'success': False, 'error': str(e)}
    
    def login(self, nick, password):
        """Mit bestehendem Account einloggen"""
        print(f"\n🔐 Versuche Login: {nick}")
        print("=" * 60)
        
        try:
            # 1. Login-Formular vorbereiten
            form_data = urllib.parse.urlencode({
                'nick': nick,
                'passwort': password,
                'lsguid': 'false'  # Standard-Wert aus HTML
            }).encode('iso-8859-1')
            
            # 2. Login anfordern
            print("\n[1/3] Sende Login-Daten...")
            req = urllib.request.Request(
                f"{self.base_url}/index.php",
                data=form_data,
                headers={
                    'User-Agent': 'Mozilla/5.0 (VZ-Login-Analyzer/1.0)',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                method='POST'
            )
            
            # 3. Response analysieren
            print("[2/3] Analysiere Response...")
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.status
                html = response.read().decode('iso-8859-1', errors='replace')
                
                print(f"   Status: {status}")
                print(f"   Größe: {len(html)} bytes")
                
                # Session-Cookies extrahieren
                cookies = self.extract_cookies()
                print(f"\n[3/3] Session-Cookies:")
                for cookie in self.cookie_jar:
                    print(f"   🍪 {cookie.name}={cookie.value[:20]}... (Domain: {cookie.domain})")
                
                # Prüfen ob Login erfolgreich war
                if 'Spielernamen' in html or 'Ressourcen' in html or nick.lower() in html.lower():
                    print(f"\n✅ Login erfolgreich für: {nick}")
                    self.session_data['logged_in'] = True
                    self.session_data['player_nick'] = nick
                    self.session_data['analyzed_at'] = datetime.now().isoformat()
                    
                    # Login in History speichern
                    self.session_data['login_history'].append({
                        'nick': nick,
                        'timestamp': datetime.now().isoformat(),
                        'success': True
                    })
                    
                    # Session speichern
                    self.save_session_cookies()
                    
                    return {
                        'success': True,
                        'nick': nick,
                        'cookies': cookies,
                        'html_preview': html[:500]
                    }
                else:
                    print(f"\n❌ Login fehlgeschlagen für: {nick}")
                    
                    self.session_data['login_history'].append({
                        'nick': nick,
                        'timestamp': datetime.now().isoformat(),
                        'success': False
                    })
                    
                    return {
                        'success': False,
                        'error': 'Falsche Zugangsdaten oder Account nicht aktiviert',
                        'html_preview': html[:500]
                    }
            
        except urllib.error.HTTPError as e:
            print(f"\n❌ HTTP-Fehler: {e.code} - {e.reason}")
            return {'success': False, 'error': f'HTTP {e.code}'}
        except Exception as e:
            print(f"\n❌ Fehler beim Login: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_game_state(self):
        """Spielzustand mit aktiver Session abrufen"""
        if not self.session_data['logged_in']:
            print("❌ Nicht eingeloggt. Bitte zuerst login() aufrufen.")
            return None
        
        print("\n📊 Rufe Spielzustand ab...")
        
        try:
            req = urllib.request.Request(
                f"{self.base_url}/index.php",
                headers={'User-Agent': 'Mozilla/5.0 (VZ-Login-Analyzer/1.0)'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('iso-8859-1', errors='replace')
                
                # Wichtige Informationen extrahieren
                info = {
                    'status': response.status,
                    'size': len(html),
                    'content_preview': html[:1000],
                    'has_resources': 'Ressourcen' in html or 'holz' in html.lower(),
                    'has_units': 'Einheiten' in html or 'unit' in html.lower(),
                    'has_buildings': 'Gebäude' in html or 'building' in html.lower()
                }
                
                print(f"   Status: {info['status']}")
                print(f"   Größe: {info['size']} bytes")
                print(f"   Ressourcen gefunden: {info['has_resources']}")
                print(f"   Einheiten gefunden: {info['has_units']}")
                print(f"   Gebäude gefunden: {info['has_buildings']}")
                
                return info
                
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            return None
    
    def extract_form_parameters(self, html, form_action):
        """Parameter eines Formulars extrahieren"""
        parameters = []
        
        form_start = html.find(f'action="{form_action}"') or html.find(f"action='{form_action}'")
        if form_start == -1:
            return parameters
        
        form_end = html.find('</form>', form_start)
        if form_end == -1:
            form_end = len(html)
        
        form_html = html[form_start:form_end]
        
        import re
        input_pattern = r'<input\s+[^>]*name=["\']([^"\']+)["\'][^>]*(?:type=["\']([A-Z]+)["\'])?'
        inputs = re.findall(input_pattern, form_html, re.IGNORECASE)
        
        for name, input_type in inputs:
            parameters.append({
                'name': name,
                'type': input_type or 'text',
                'required': 'required' in form_html.lower()
            })
        
        return parameters
    
    def extract_cookies(self):
        """Session-Cookies extrahieren"""
        cookies = {}
        for cookie in self.cookie_jar:
            cookies[cookie.name] = {
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'secure': cookie.secure,
                'expires': cookie.expires
            }
        return cookies
    
    def save_session_cookies(self):
        """Session-Cookies speichern"""
        filepath = self.output_dir / 'session_cookies.json'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'cookies': self.extract_cookies(),
                'session_data': self.session_data,
                'saved_at': datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n💾 Session gespeichert: {filepath}")
    
    def load_session_cookies(self, filepath):
        """Session-Cookies laden"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            print(f"❌ Session-Datei nicht gefunden: {filepath}")
            return False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Cookies wiederherstellen
        for name, cookie_info in data['cookies'].items():
            cookie = http.cookiejar.Cookie(
                version=0,
                name=name,
                value=cookie_info['value'],
                port=None,
                port_specified=False,
                domain=cookie_info['domain'],
                path=cookie_info['path'],
                secure=cookie_info['secure'],
                expires=cookie_info['expires'],
                discard=False,
                comment=None,
                comment_url=None,
                rest={}
            )
            self.cookie_jar.set_cookie(cookie)
        
        # Session-Daten wiederherstellen
        self.session_data.update(data['session_data'])
        
        print(f"✅ Session geladen: {filepath}")
        return True
    
    def save_analysis(self):
        """Gesamte Analyse speichern"""
        filepath = self.output_dir / 'login_analysis.json'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Analyse gespeichert: {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Verbrannte Zone 3 - Login Analyzer")
        print("\nUsage:")
        print("  python3 login_analyzer.py <base_url> [output_dir]")
        print("\nExample:")
        print("  python3 login_analyzer.py https://v3.verbranntezone.ch")
        sys.exit(1)
    
    base_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'login_analysis'
    
    analyzer = LoginAnalyzer(base_url, output_dir)
    
    # Interaktiver Modus oder Batch-Modus
    if len(sys.argv) > 2:
        # Batch-Modus: Login mit Credentials
        if len(sys.argv) >= 5:
            nick = sys.argv[3]
            password = sys.argv[4]
            analyzer.login(nick, password)
            analyzer.get_game_state()
            analyzer.save_analysis()


if __name__ == '__main__':
    main()
