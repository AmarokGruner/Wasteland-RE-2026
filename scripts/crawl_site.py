#!/usr/bin/env python3
"""
Verbrannte Zone 3 - Website Crawler
Extrahiert alle Seiten, Assets und strukturiert die Daten.
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


class SiteCrawler:
    def __init__(self, base_url, output_dir):
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.pages = {}  # url -> {html, title, links, timestamp}
        self.assets = {}  # url -> local_path
        self.visited = set()
        self.errors = []
        
    def crawl(self, max_pages=50):
        """Haupt-Crawl-Methode"""
        print(f"🕷️  Starte Crawl von {self.base_url}")
        print(f"📁 Output: {self.output_dir}")
        print("=" * 60)
        
        queue = [self.base_url]
        pages_crawled = 0
        
        while queue and pages_crawled < max_pages:
            url = queue.pop(0)
            
            if url in self.visited:
                continue
            
            print(f"\n[{pages_crawled + 1}] Crawling: {url}")
            self.visited.add(url)
            
            result = self.crawl_page(url)
            if result:
                pages_crawled += 1
                
                # Neue Links zur Warteschlange hinzufügen
                for link in result.get('links', []):
                    if link not in self.visited and self.base_url in link:
                        queue.append(link)
        
        # Metadaten speichern
        self.save_metadata()
        
        print(f"\n{'=' * 60}")
        print(f"✅ Crawl abgeschlossen!")
        print(f"   Seiten: {pages_crawled}")
        print(f"   Assets: {len(self.assets)}")
        print(f"   Fehler: {len(self.errors)}")
        
    def crawl_page(self, url):
        """Eine einzelne Seite crawlen"""
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; VZ-RE-Crawler/1.0)',
                    'Accept': 'text/html,application/xhtml+xml',
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('iso-8859-1', errors='replace')
                
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            self.errors.append({'url': url, 'error': str(e)})
            return None
        
        # HTML speichern
        safe_url = urllib.parse.urlparse(url).path.strip('/')
        if not safe_url:
            safe_url = 'index'
        
        filename = f"{safe_url.replace('/', '_')}.html"
        filepath = self.output_dir / 'pages' / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='iso-8859-1') as f:
            f.write(html)
        
        # Metadaten extrahieren
        title = self.extract_title(html)
        links = self.extract_links(html, url)
        assets = self.extract_assets(html, url)
        
        page_data = {
            'url': url,
            'title': title,
            'filename': filename,
            'links': links,
            'assets': assets,
            'crawled_at': datetime.now().isoformat(),
            'size': len(html)
        }
        
        self.pages[url] = page_data
        
        print(f"   ✅ {title} ({len(html)} bytes)")
        
        return page_data
    
    def extract_title(self, html):
        """Titel aus HTML extrahieren"""
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return 'Unbekannt'
    
    def extract_links(self, html, base_url):
        """Alle Links aus HTML extrahieren"""
        links = []
        
        # <a href="...">
        pattern = r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(pattern, html, re.IGNORECASE)
        
        for link in matches:
            # Absolute URLs erstellen
            if not link.startswith('http'):
                parsed_base = urllib.parse.urlparse(base_url)
                base_path = parsed_base.path.rsplit('/', 1)[0] if '/' in parsed_base.path else ''
                link = urllib.parse.urljoin(f"{parsed_base.scheme}://{parsed_base.netloc}{base_path}/", link)
            
            links.append(link)
        
        return list(set(links))  # Duplikate entfernen
    
    def extract_assets(self, html, base_url):
        """Assets (Bilder, CSS, JS) extrahieren"""
        assets = []
        parsed_base = urllib.parse.urlparse(base_url)
        
        # Bilder
        pattern = r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>'
        for src in re.findall(pattern, html, re.IGNORECASE):
            if not src.startswith('http'):
                base_path = parsed_base.path.rsplit('/', 1)[0] if '/' in parsed_base.path else ''
                src = urllib.parse.urljoin(f"{parsed_base.scheme}://{parsed_base.netloc}{base_path}/", src)
            assets.append({'type': 'image', 'url': src})
        
        # CSS
        pattern = r'<link\s+[^>]*href=["\']([^"\']+)["\'][^>]*type=["\']text/css["\']'
        for href in re.findall(pattern, html, re.IGNORECASE):
            if not href.startswith('http'):
                base_path = parsed_base.path.rsplit('/', 1)[0] if '/' in parsed_base.path else ''
                href = urllib.parse.urljoin(f"{parsed_base.scheme}://{parsed_base.netloc}{base_path}/", href)
            assets.append({'type': 'css', 'url': href})
        
        # JavaScript
        pattern = r'<script\s+[^>]*src=["\']([^"\']+)["\'][^>]*>'
        for src in re.findall(pattern, html, re.IGNORECASE):
            if not src.startswith('http'):
                base_path = parsed_base.path.rsplit('/', 1)[0] if '/' in parsed_base.path else ''
                src = urllib.parse.urljoin(f"{parsed_base.scheme}://{parsed_base.netloc}{base_path}/", src)
            assets.append({'type': 'js', 'url': src})
        
        return assets
    
    def save_metadata(self):
        """Crawl-Metadaten speichern"""
        metadata = {
            'base_url': self.base_url,
            'crawled_at': datetime.now().isoformat(),
            'total_pages': len(self.pages),
            'total_assets': len(self.assets),
            'total_errors': len(self.errors),
            'pages': list(self.pages.values()),
            'errors': self.errors
        }
        
        filepath = self.output_dir / 'crawl_metadata.json'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Metadaten gespeichert: {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Verbrannte Zone 3 - Website Crawler")
        print("\nUsage: python3 crawl_site.py <base_url> [output_dir]")
        print("\nExample:")
        print("  python3 crawl_site.py https://v3.verbranntezone.ch")
        sys.exit(1)
    
    base_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'crawled_site'
    
    crawler = SiteCrawler(base_url, output_dir)
    crawler.crawl(max_pages=50)


if __name__ == '__main__':
    main()
