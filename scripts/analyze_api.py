#!/usr/bin/env python3
"""
Verbrannte Zone 3 - API Analyzer
Identifiziert und dokumentiert alle API-Endpunkte.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.parse
import re


class APIAnalyzer:
    def __init__(self, base_url, output_dir):
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.endpoints = []  # Gefundene Endpunkte
        self.requests_log = []  # Alle gesendeten Requests
        self.responses_log = []  # Alle Responses
        
    def analyze(self):
        """Hauptanalyse-Methode"""
        print(f"🔍 Starte API-Analyse von {self.base_url}")
        print("=" * 60)
        
        # 1. HTML-Seiten analysieren (Formulare, Links)
        print("\n📄 Phase 1: HTML-Analyse...")
        self.analyze_html_forms()
        
        # 2. Bekannte Endpunkte testen
        print("\n🔗 Phase 2: Endpunkt-Tests...")
        self.test_known_endpoints()
        
        # 3. Ergebnisse speichern
        print("\n💾 Phase 3: Ergebnisse speichern...")
        self.save_results()
        
        print(f"\n{'=' * 60}")
        print(f"✅ Analyse abgeschlossen!")
        print(f"   Endpunkte gefunden: {len(self.endpoints)}")
    
    def analyze_html_forms(self):
        """Formulare und API-Referenzen in HTML analysieren"""
        try:
            req = urllib.request.Request(
                self.base_url,
                headers={'User-Agent': 'Mozilla/5.0 (API-Analyzer/1.0)'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('iso-8859-1', errors='replace')
                
        except Exception as e:
            print(f"   ❌ Fehler beim Laden der Seite: {e}")
            return
        
        # Formulare extrahieren
        form_pattern = r'<form\s+[^>]*action=["\']([^"\']*)["\'][^>]*method=["\']([A-Z]+)["\'][^>]*>'
        forms = re.findall(form_pattern, html, re.IGNORECASE)
        
        for action, method in forms:
            if not action.startswith('http'):
                parsed = urllib.parse.urlparse(self.base_url)
                base_path = parsed.path.rsplit('/', 1)[0] if '/' in parsed.path else ''
                action = urllib.parse.urljoin(f"{parsed.scheme}://{parsed.netloc}{base_path}/", action)
            
            endpoint = {
                'type': 'form',
                'url': action,
                'method': method.upper(),
                'source': 'html_form',
                'parameters': self.extract_form_parameters(html, action)
            }
            
            if not any(e['url'] == endpoint['url'] for e in self.endpoints):
                self.endpoints.append(endpoint)
                print(f"   📝 Formular: {method} {action}")
        
        # JavaScript API-Calls suchen
        js_pattern = r'(fetch|XMLHttpRequest|\.post|\.get)\s*\([^)]*["\'](/[^"\']+)["\']'
        js_calls = re.findall(js_pattern, html, re.IGNORECASE)
        
        for call_type, path in js_calls:
            if not path.startswith('http'):
                parsed = urllib.parse.urlparse(self.base_url)
                base_path = parsed.path.rsplit('/', 1)[0] if '/' in parsed.path else ''
                path = urllib.parse.urljoin(f"{parsed.scheme}://{parsed.netloc}{base_path}/", path)
            
            endpoint = {
                'type': 'javascript',
                'url': path,
                'method': 'POST' if 'post' in call_type.lower() else 'GET',
                'source': 'javascript',
                'parameters': []
            }
            
            if not any(e['url'] == endpoint['url'] for e in self.endpoints):
                self.endpoints.append(endpoint)
                print(f"   ⚡ JS-Call: {endpoint['method']} {path}")
    
    def extract_form_parameters(self, html, form_action):
        """Parameter eines Formulars extrahieren"""
        parameters = []
        
        # Suche nach Input-Feldern im relevanten Formular
        form_start = html.find(f'action="{form_action}"') or html.find(f"action='{form_action}'")
        if form_start == -1:
            return parameters
        
        # Formular-Ende finden (nächstes </form> oder Ende des Dokuments)
        form_end = html.find('</form>', form_start)
        if form_end == -1:
            form_end = len(html)
        
        form_html = html[form_start:form_end]
        
        # Input-Felder extrahieren
        input_pattern = r'<input\s+[^>]*name=["\']([^"\']+)["\'][^>]*(?:type=["\']([A-Z]+)["\'])?'
        inputs = re.findall(input_pattern, form_html, re.IGNORECASE)
        
        for name, input_type in inputs:
            parameters.append({
                'name': name,
                'type': input_type or 'text',
                'required': 'required' in form_html.lower()
            })
        
        return parameters
    
    def test_known_endpoints(self):
        """Bekannte Endpunkte der Verbrannten Zone testen"""
        known_paths = [
            'index.php',
            'news.php',
            'geschichte.php',
            'infos.php',
            'screenshots.php',
            'regeln.php',
            'datenschutz.php',
            'anmelden.php',
            'aktivieren.php',
            'browsertest.php',
            'links.php',
            'kontakt.php',
            'impressum.php',
            'passwort.php'
        ]
        
        for path in known_paths:
            url = f"{self.base_url}/{path}"
            
            try:
                req = urllib.request.Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0 (API-Analyzer/1.0)'}
                )
                
                with urllib.request.urlopen(req, timeout=5) as response:
                    status = response.status
                    content_type = response.headers.get('Content-Type', '')
                    size = len(response.read())
                    
                print(f"   ✅ {path}: {status} ({size} bytes)")
                
                endpoint = {
                    'type': 'page',
                    'url': url,
                    'method': 'GET',
                    'status': status,
                    'content_type': content_type,
                    'size': size,
                    'source': 'known_endpoint'
                }
                
                if not any(e['url'] == url for e in self.endpoints):
                    self.endpoints.append(endpoint)
                    
            except Exception as e:
                print(f"   ❌ {path}: {str(e)[:50]}")
    
    def save_results(self):
        """Analyse-Ergebnisse speichern"""
        results = {
            'base_url': self.base_url,
            'analyzed_at': datetime.now().isoformat(),
            'total_endpoints': len(self.endpoints),
            'endpoints': self.endpoints,
            'summary': {
                'forms': len([e for e in self.endpoints if e.get('type') == 'form']),
                'pages': len([e for e in self.endpoints if e.get('type') == 'page']),
                'javascript': len([e for e in self.endpoints if e.get('type') == 'javascript'])
            }
        }
        
        filepath = self.output_dir / 'api_endpoints.json'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"   📄 API-Endpunkte: {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Verbrannte Zone 3 - API Analyzer")
        print("\nUsage: python3 analyze_api.py <base_url> [output_dir]")
        sys.exit(1)
    
    base_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'api_analysis'
    
    analyzer = APIAnalyzer(base_url, output_dir)
    analyzer.analyze()


if __name__ == '__main__':
    main()
