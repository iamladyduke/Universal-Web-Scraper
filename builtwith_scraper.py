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

class BuiltWithScraper:
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
            # BuiltWith is sensitive to scraping, so use longer delays
            time.sleep(random.uniform(3.0, 5.0))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def scrape_technology_directory(self, category=None):
        """Scrape BuiltWith technology directory"""
        base_url = "https://builtwith.com/technologies"
        if category:
            base_url += f"/{category}"
        
        logger.info(f"Scraping technology directory: {base_url}")
        
        html_content = self.get_page(base_url)
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for technology cards/items
        tech_items = soup.find_all(['div', 'article'], class_=re.compile(r'tech|technology|card|item'))
        
        for item in tech_items:
            if len(self.data) >= self.max_items:
                break
                
            tech_data = self.extract_technology_data(item)
            if tech_data:
                self.data.append(tech_data)
        
        return self.data
    
    def scrape_recent_websites(self):
        """Scrape recently analyzed websites"""
        url = "https://builtwith.com/recent"
        logger.info(f"Scraping recent websites: {url}")
        
        html_content = self.get_page(url)
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for website cards/items
        site_items = soup.find_all(['div', 'article'], class_=re.compile(r'site|website|card|item'))
        
        for item in site_items:
            if len(self.data) >= self.max_items:
                break
                
            site_data = self.extract_website_data(item)
            if site_data:
                self.data.append(site_data)
        
        return self.data
    
    def scrape_technology_details(self, tech_url):
        """Scrape detailed information about a specific technology"""
        logger.info(f"Scraping technology details: {tech_url}")
        
        html_content = self.get_page(tech_url)
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract detailed technology information
        tech_data = {
            'technology_name': self.extract_text(soup, ['h1', '.tech-title', '.technology-name']),
            'description': self.extract_text(soup, ['.description', '.tech-description', '.summary']),
            'category': self.extract_text(soup, ['.category', '.tech-category', '.type']),
            'usage_percentage': self.extract_text(soup, ['.usage-percentage', '.percentage', '.stats']),
            'websites_using': self.extract_text(soup, ['.websites-count', '.usage-count', '.sites-using']),
            'last_updated': self.extract_text(soup, ['.last-updated', '.update-date', '.timestamp']),
            'url': tech_url
        }
        
        return tech_data
    
    def extract_technology_data(self, item):
        """Extract technology data from an item element"""
        try:
            # Find technology name
            name_elem = item.find(['h2', 'h3', 'h4'], class_=re.compile(r'title|name|tech'))
            name = name_elem.get_text(strip=True) if name_elem else "N/A"
            
            # Find link
            link_elem = item.find('a')
            link = urljoin("https://builtwith.com", link_elem.get('href')) if link_elem else "N/A"
            
            # Find description
            desc_elem = item.find(['p', 'div'], class_=re.compile(r'description|summary|details'))
            description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            # Find category
            cat_elem = item.find(['span', 'div'], class_=re.compile(r'category|type|tech-type'))
            category = cat_elem.get_text(strip=True) if cat_elem else "N/A"
            
            # Find usage stats
            usage_elem = item.find(['span', 'div'], class_=re.compile(r'usage|percentage|stats'))
            usage = usage_elem.get_text(strip=True) if usage_elem else "N/A"
            
            return {
                'technology_name': name,
                'category': category,
                'description': description,
                'usage_stats': usage,
                'link': link
            }
        except Exception as e:
            logger.error(f"Error extracting technology data: {e}")
            return None
    
    def extract_website_data(self, item):
        """Extract website data from an item element"""
        try:
            # Find website URL
            url_elem = item.find(['h3', 'h4', 'a'], class_=re.compile(r'url|site|website'))
            website_url = url_elem.get_text(strip=True) if url_elem else "N/A"
            
            # Find technologies
            tech_elem = item.find(['div', 'span'], class_=re.compile(r'tech|technology'))
            technologies = tech_elem.get_text(strip=True) if tech_elem else "N/A"
            
            # Find traffic rank
            rank_elem = item.find(['span', 'div'], class_=re.compile(r'rank|traffic|alexa'))
            traffic_rank = rank_elem.get_text(strip=True) if rank_elem else "N/A"
            
            # Find country
            country_elem = item.find(['span', 'div'], class_=re.compile(r'country|location'))
            country = country_elem.get_text(strip=True) if country_elem else "N/A"
            
            # Find link
            link_elem = item.find('a')
            link = urljoin("https://builtwith.com", link_elem.get('href')) if link_elem else "N/A"
            
            return {
                'website_url': website_url,
                'technologies': technologies,
                'traffic_rank': traffic_rank,
                'country': country,
                'link': link
            }
        except Exception as e:
            logger.error(f"Error extracting website data: {e}")
            return None
    
    def extract_text(self, soup, selectors):
        """Extract text using multiple possible selectors"""
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return "N/A"
    
    def save_to_csv(self, filename='builtwith_data.csv'):
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
    
    def save_to_json(self, filename='builtwith_data.json'):
        """Save scraped data to JSON file"""
        if not self.data:
            logger.warning("No data to save")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.data)} items to {filename}")

def main():
    scraper = BuiltWithScraper()
    
    print("BuiltWith Scraper")
    print("1. Scrape Technology Directory")
    print("2. Scrape Recent Websites")
    print("3. Scrape Specific Technology")
    
    choice = input("Enter your choice (1-3): ")
    
    try:
        if choice == "1":
            category = input("Enter technology category (optional, press Enter to skip): ")
            category = category if category.strip() else None
            data = scraper.scrape_technology_directory(category)
            scraper.save_to_csv('builtwith_technologies.csv')
            scraper.save_to_json('builtwith_technologies.json')
            
        elif choice == "2":
            data = scraper.scrape_recent_websites()
            scraper.save_to_csv('builtwith_websites.csv')
            scraper.save_to_json('builtwith_websites.json')
            
        elif choice == "3":
            tech_url = input("Enter BuiltWith technology URL: ")
            data = scraper.scrape_technology_details(tech_url)
            if data:
                scraper.data = [data]
                scraper.save_to_csv('builtwith_technology_details.csv')
                scraper.save_to_json('builtwith_technology_details.json')
        
        else:
            print("Invalid choice!")
            return
            
        logger.info("Scraping completed successfully!")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")

if __name__ == "__main__":
    main() 