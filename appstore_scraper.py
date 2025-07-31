import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import json
import logging
from urllib.parse import urljoin, urlparse
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AppStoreScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.data = []
        self.max_items = 5000
        
    def get_page(self, url):
        """Get a page with error handling and rate limiting"""
        try:
            # App stores are sensitive to scraping, so use longer delays
            time.sleep(random.uniform(3.0, 5.0))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def scrape_playstore_category(self, category="apps", search_term=None):
        """Scrape Google Play Store apps by category or search"""
        if search_term:
            base_url = f"https://play.google.com/store/search?q={search_term}&c=apps"
        else:
            base_url = f"https://play.google.com/store/apps/category/{category}"
        
        logger.info(f"Scraping Play Store: {base_url}")
        
        html_content = self.get_page(base_url)
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for app cards/items
        app_items = soup.find_all(['div', 'article'], class_=re.compile(r'app|card|item|result'))
        
        for item in app_items:
            if len(self.data) >= self.max_items:
                break
                
            app_data = self.extract_playstore_data(item)
            if app_data:
                self.data.append(app_data)
        
        return self.data
    
    def scrape_appstore_category(self, category="apps", search_term=None):
        """Scrape Apple App Store apps by category or search"""
        if search_term:
            base_url = f"https://apps.apple.com/search?term={search_term}&entity=software"
        else:
            base_url = f"https://apps.apple.com/us/genre/ios/{category}"
        
        logger.info(f"Scraping App Store: {base_url}")
        
        html_content = self.get_page(base_url)
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for app cards/items
        app_items = soup.find_all(['div', 'article'], class_=re.compile(r'app|card|item|result'))
        
        for item in app_items:
            if len(self.data) >= self.max_items:
                break
                
            app_data = self.extract_appstore_data(item)
            if app_data:
                self.data.append(app_data)
        
        return self.data
    
    def extract_playstore_data(self, item):
        """Extract app data from Play Store item"""
        try:
            # Find app name
            name_elem = item.find(['h3', 'h2', 'h4'], class_=re.compile(r'title|name|app'))
            name = name_elem.get_text(strip=True) if name_elem else "N/A"
            
            # Find developer
            dev_elem = item.find(['span', 'div'], class_=re.compile(r'developer|publisher|company'))
            developer = dev_elem.get_text(strip=True) if dev_elem else "N/A"
            
            # Find rating
            rating_elem = item.find(['span', 'div'], class_=re.compile(r'rating|stars|score'))
            rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"
            
            # Find reviews count
            reviews_elem = item.find(['span', 'div'], class_=re.compile(r'reviews|review-count'))
            reviews = reviews_elem.get_text(strip=True) if reviews_elem else "N/A"
            
            # Find price
            price_elem = item.find(['span', 'div'], class_=re.compile(r'price|cost'))
            price = price_elem.get_text(strip=True) if price_elem else "Free"
            
            # Find category
            cat_elem = item.find(['span', 'div'], class_=re.compile(r'category|genre'))
            category = cat_elem.get_text(strip=True) if cat_elem else "N/A"
            
            # Find description
            desc_elem = item.find(['p', 'div'], class_=re.compile(r'description|summary'))
            description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            # Find link
            link_elem = item.find('a')
            link = urljoin("https://play.google.com", link_elem.get('href')) if link_elem else "N/A"
            
            # Find size
            size_elem = item.find(['span', 'div'], class_=re.compile(r'size|download-size'))
            size = size_elem.get_text(strip=True) if size_elem else "N/A"
            
            # Find downloads
            downloads_elem = item.find(['span', 'div'], class_=re.compile(r'downloads|installs'))
            downloads = downloads_elem.get_text(strip=True) if downloads_elem else "N/A"
            
            return {
                'app_name': name,
                'developer': developer,
                'rating': rating,
                'reviews_count': reviews,
                'price': price,
                'category': category,
                'description': description,
                'link': link,
                'size': size,
                'downloads': downloads,
                'store': 'Google Play Store'
            }
        except Exception as e:
            logger.error(f"Error extracting Play Store data: {e}")
            return None
    
    def extract_appstore_data(self, item):
        """Extract app data from App Store item"""
        try:
            # Find app name
            name_elem = item.find(['h3', 'h2', 'h4'], class_=re.compile(r'title|name|app'))
            name = name_elem.get_text(strip=True) if name_elem else "N/A"
            
            # Find developer
            dev_elem = item.find(['span', 'div'], class_=re.compile(r'developer|publisher|company'))
            developer = dev_elem.get_text(strip=True) if dev_elem else "N/A"
            
            # Find rating
            rating_elem = item.find(['span', 'div'], class_=re.compile(r'rating|stars|score'))
            rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"
            
            # Find reviews count
            reviews_elem = item.find(['span', 'div'], class_=re.compile(r'reviews|review-count'))
            reviews = reviews_elem.get_text(strip=True) if reviews_elem else "N/A"
            
            # Find price
            price_elem = item.find(['span', 'div'], class_=re.compile(r'price|cost'))
            price = price_elem.get_text(strip=True) if price_elem else "Free"
            
            # Find category
            cat_elem = item.find(['span', 'div'], class_=re.compile(r'category|genre'))
            category = cat_elem.get_text(strip=True) if cat_elem else "N/A"
            
            # Find description
            desc_elem = item.find(['p', 'div'], class_=re.compile(r'description|summary'))
            description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            # Find link
            link_elem = item.find('a')
            link = urljoin("https://apps.apple.com", link_elem.get('href')) if link_elem else "N/A"
            
            # Find size
            size_elem = item.find(['span', 'div'], class_=re.compile(r'size|download-size'))
            size = size_elem.get_text(strip=True) if size_elem else "N/A"
            
            # Find age rating
            age_elem = item.find(['span', 'div'], class_=re.compile(r'age|content-rating'))
            age_rating = age_elem.get_text(strip=True) if age_elem else "N/A"
            
            return {
                'app_name': name,
                'developer': developer,
                'rating': rating,
                'reviews_count': reviews,
                'price': price,
                'category': category,
                'description': description,
                'link': link,
                'size': size,
                'age_rating': age_rating,
                'store': 'Apple App Store'
            }
        except Exception as e:
            logger.error(f"Error extracting App Store data: {e}")
            return None
    
    def save_to_csv(self, filename='appstore_data.csv'):
        """Save scraped data to CSV file"""
        if not self.data:
            logger.warning("No data to save")
            return
        
        fieldnames = list(self.data[0].keys()) if self.data else []
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)
        
        logger.info(f"Saved {len(self.data)} items to {filename}")
    
    def save_to_json(self, filename='appstore_data.json'):
        """Save scraped data to JSON file"""
        if not self.data:
            logger.warning("No data to save")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.data)} items to {filename}")

def main():
    scraper = AppStoreScraper()
    
    print("App Store Scraper")
    print("1. Scrape Google Play Store")
    print("2. Scrape Apple App Store")
    print("3. Scrape Both Stores")
    
    choice = input("Enter your choice (1-3): ")
    
    try:
        if choice == "1":
            search_term = input("Enter search term (optional, press Enter to skip): ")
            search_term = search_term if search_term.strip() else None
            data = scraper.scrape_playstore_category(search_term=search_term)
            scraper.save_to_csv('playstore_apps.csv')
            scraper.save_to_json('playstore_apps.json')
            
        elif choice == "2":
            search_term = input("Enter search term (optional, press Enter to skip): ")
            search_term = search_term if search_term.strip() else None
            data = scraper.scrape_appstore_category(search_term=search_term)
            scraper.save_to_csv('appstore_apps.csv')
            scraper.save_to_json('appstore_apps.json')
            
        elif choice == "3":
            search_term = input("Enter search term (optional, press Enter to skip): ")
            search_term = search_term if search_term.strip() else None
            
            # Scrape both stores
            playstore_data = scraper.scrape_playstore_category(search_term=search_term)
            scraper.data = []  # Reset for App Store
            appstore_data = scraper.scrape_appstore_category(search_term=search_term)
            
            # Combine data
            all_data = playstore_data + appstore_data
            scraper.data = all_data
            
            scraper.save_to_csv('all_appstores.csv')
            scraper.save_to_json('all_appstores.json')
        
        else:
            print("Invalid choice!")
            return
            
        logger.info("Scraping completed successfully!")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")

if __name__ == "__main__":
    main() 