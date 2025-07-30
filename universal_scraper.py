import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import json
import logging
from urllib.parse import urljoin, urlparse
import argparse
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UniversalScraper:
    def __init__(self, config_file=None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.data = []
        self.config = self.load_config(config_file)
        
    def load_config(self, config_file):
        """Load scraping configuration from JSON file"""
        if config_file:
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                return self.get_default_config()
        else:
            return self.get_default_config()
    
    def get_default_config(self):
        """Default configuration for common job sites"""
        return {
            "base_url": "",
            "item_selector": "div.listing-item, .job-listing, .posting",
            "fields": {
                "title": {
                    "selector": "h2, h3, .title, .job-title",
                    "attribute": "text"
                },
                "company": {
                    "selector": ".company, .employer, .organization",
                    "attribute": "text"
                },
                "location": {
                    "selector": ".location, .city, .place",
                    "attribute": "text"
                },
                "description": {
                    "selector": ".description, .summary, .details",
                    "attribute": "text"
                },
                "link": {
                    "selector": "a",
                    "attribute": "href"
                },
                "date": {
                    "selector": ".date, .posted, .timestamp",
                    "attribute": "text"
                }
            },
            "pagination": {
                "enabled": True,
                "pattern": "?page={page}",
                "max_pages": 100
            },
            "rate_limiting": {
                "delay_min": 0.5,
                "delay_max": 1.0
            },
            "max_items": 5000
        }
    
    def get_page(self, url):
        """Get a page with error handling and rate limiting"""
        try:
            delay = random.uniform(
                self.config["rate_limiting"]["delay_min"],
                self.config["rate_limiting"]["delay_max"]
            )
            time.sleep(delay)
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_field_value(self, element, field_config):
        """Extract value from element based on field configuration"""
        try:
            selector = field_config.get("selector", "")
            attribute = field_config.get("attribute", "text")
            
            if not selector:
                return "N/A"
            
            # Find element using selector
            found_element = element.select_one(selector)
            if not found_element:
                return "N/A"
            
            # Extract value based on attribute type
            if attribute == "text":
                return found_element.get_text(strip=True)
            elif attribute == "href":
                href = found_element.get("href")
                if href:
                    return urljoin(self.config["base_url"], href)
                return "N/A"
            else:
                return found_element.get(attribute, "N/A")
                
        except Exception as e:
            logger.error(f"Error extracting field: {e}")
            return "N/A"
    
    def parse_items(self, soup):
        """Parse items from the page using configured selectors"""
        items = []
        item_selector = self.config["item_selector"]
        
        elements = soup.select(item_selector)
        logger.info(f"Found {len(elements)} items on page")
        
        for element in elements:
            if len(self.data) >= self.config["max_items"]:
                break
                
            item_data = {}
            for field_name, field_config in self.config["fields"].items():
                value = self.extract_field_value(element, field_config)
                item_data[field_name] = value
            
            if item_data:
                self.data.append(item_data)
                items.append(item_data)
        
        return len(items)
    
    def scrape_page(self, page_num=1):
        """Scrape a single page"""
        if page_num == 1:
            url = self.config["base_url"]
        else:
            pagination = self.config["pagination"]
            if pagination["enabled"]:
                pattern = pagination["pattern"]
                url = self.config["base_url"] + pattern.format(page=page_num)
            else:
                return 0
        
        logger.info(f"Scraping page {page_num}: {url}")
        
        html_content = self.get_page(url)
        if not html_content:
            return 0
        
        soup = BeautifulSoup(html_content, 'html.parser')
        items_found = self.parse_items(soup)
        
        logger.info(f"Found {items_found} items on page {page_num}")
        return items_found
    
    def scrape_all(self):
        """Scrape all available pages"""
        page_num = 1
        max_pages = self.config["pagination"]["max_pages"]
        
        while len(self.data) < self.config["max_items"] and page_num <= max_pages:
            items_on_page = self.scrape_page(page_num)
            
            if items_on_page == 0:
                logger.info("No more items found, stopping pagination")
                break
            
            page_num += 1
        
        logger.info(f"Total items scraped: {len(self.data)}")
        return self.data
    
    def save_to_csv(self, filename='scraped_data.csv'):
        """Save scraped data to CSV file"""
        if not self.data:
            logger.warning("No data to save")
            return
        
        # Get field names from the first item
        fieldnames = list(self.data[0].keys()) if self.data else []
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)
        
        logger.info(f"Saved {len(self.data)} items to {filename}")
    
    def save_to_json(self, filename='scraped_data.json'):
        """Save scraped data to JSON file"""
        if not self.data:
            logger.warning("No data to save")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.data)} items to {filename}")

def create_config_template():
    """Create a template configuration file"""
    template = {
        "base_url": "https://example.com/jobs",
        "item_selector": "div.job-item, .listing",
        "fields": {
            "title": {
                "selector": "h2.title, .job-title",
                "attribute": "text"
            },
            "company": {
                "selector": ".company-name",
                "attribute": "text"
            },
            "location": {
                "selector": ".location",
                "attribute": "text"
            },
            "description": {
                "selector": ".description",
                "attribute": "text"
            },
            "link": {
                "selector": "a.title",
                "attribute": "href"
            },
            "date": {
                "selector": ".date-posted",
                "attribute": "text"
            }
        },
        "pagination": {
            "enabled": True,
            "pattern": "?page={page}",
            "max_pages": 100
        },
        "rate_limiting": {
            "delay_min": 0.5,
            "delay_max": 1.0
        },
        "max_items": 5000
    }
    
    with open('scraper_config.json', 'w') as f:
        json.dump(template, f, indent=2)
    
    print("Created scraper_config.json template file")

def main():
    parser = argparse.ArgumentParser(description='Universal Web Scraper')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--output', '-o', default='scraped_data.csv', help='Output file name')
    parser.add_argument('--format', '-f', choices=['csv', 'json'], default='csv', help='Output format')
    parser.add_argument('--template', '-t', action='store_true', help='Create config template')
    
    args = parser.parse_args()
    
    if args.template:
        create_config_template()
        return
    
    if not args.config:
        print("Error: Configuration file required. Use --template to create a template.")
        print("Usage: python3 universal_scraper.py --config scraper_config.json")
        return
    
    scraper = UniversalScraper(args.config)
    logger.info("Starting universal scraper...")
    
    try:
        data = scraper.scrape_all()
        
        if args.format == 'csv':
            scraper.save_to_csv(args.output)
        else:
            scraper.save_to_json(args.output.replace('.csv', '.json'))
        
        logger.info("Scraping completed successfully!")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")

if __name__ == "__main__":
    main() 