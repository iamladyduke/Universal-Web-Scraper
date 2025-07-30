import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin, urlparse, parse_qs
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ITJobBoardScraper:
    def __init__(self):
        self.base_url = "https://www.itjobboard.co.uk/jobs/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.jobs = []
        self.max_jobs = 5000
        
    def get_page(self, url):
        """Get a page with error handling and rate limiting"""
        try:
            # Random delay between 500ms and 1000ms
            time.sleep(random.uniform(0.5, 1.0))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_job_listing(self, job_element):
        """Parse a single job listing element"""
        try:
            # Title and link
            title_element = job_element.find('a', class_='listing-item__title')
            title = title_element.get_text(strip=True) if title_element else "N/A"
            link = urljoin(self.base_url, title_element.get('href')) if title_element else "N/A"
            
            # Company
            company_element = job_element.find('div', class_='listing-item__info--item')
            company = company_element.get_text(strip=True) if company_element else "N/A"
            
            # Location (second listing-item__info--item)
            info_items = job_element.find_all('div', class_='listing-item__info--item')
            location = info_items[1].get_text(strip=True) if len(info_items) > 1 else "N/A"
            
            # Job Type
            job_type_element = job_element.find('span', class_='listing-item__employment-type')
            job_type = job_type_element.get_text(strip=True) if job_type_element else "N/A"
            
            # Date Posted
            date_element = job_element.find('span', class_='listing-item__date')
            date_posted = date_element.get_text(strip=True) if date_element else "N/A"
            
            # Description
            desc_element = job_element.find('div', class_='listing-item__desc')
            description = desc_element.get_text(strip=True) if desc_element else "N/A"
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'job_type': job_type,
                'date_posted': date_posted,
                'description': description,
                'link': link
            }
        except Exception as e:
            logger.error(f"Error parsing job listing: {e}")
            return None
    
    def scrape_page(self, page_num):
        """Scrape a single page of job listings"""
        url = f"{self.base_url}?page={page_num}" if page_num > 1 else self.base_url
        logger.info(f"Scraping page {page_num}: {url}")
        
        html_content = self.get_page(url)
        if not html_content:
            return 0
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find job listings
        job_elements = soup.find_all('div', class_='listing-item')
        
        if not job_elements:
            logger.warning(f"No job listings found on page {page_num}")
            return 0
        
        page_jobs = 0
        for job_element in job_elements:
            if len(self.jobs) >= self.max_jobs:
                logger.info(f"Reached maximum jobs limit ({self.max_jobs})")
                return page_jobs
            
            job_data = self.parse_job_listing(job_element)
            if job_data:
                self.jobs.append(job_data)
                page_jobs += 1
        
        logger.info(f"Found {page_jobs} jobs on page {page_num}")
        return page_jobs
    
    def scrape_all(self):
        """Scrape all available job listings"""
        page_num = 1
        total_jobs = 0
        
        while len(self.jobs) < self.max_jobs:
            jobs_on_page = self.scrape_page(page_num)
            
            if jobs_on_page == 0:
                logger.info("No more jobs found, stopping pagination")
                break
            
            total_jobs += jobs_on_page
            page_num += 1
            
            # Safety check to prevent infinite loops
            if page_num > 1000:
                logger.warning("Reached page limit, stopping")
                break
        
        logger.info(f"Total jobs scraped: {len(self.jobs)}")
        return self.jobs
    
    def save_to_csv(self, filename='itjobboard_5k.csv'):
        """Save scraped jobs to CSV file"""
        if not self.jobs:
            logger.warning("No jobs to save")
            return
        
        fieldnames = ['title', 'company', 'location', 'job_type', 'date_posted', 'description', 'link']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.jobs)
        
        logger.info(f"Saved {len(self.jobs)} jobs to {filename}")

def main():
    scraper = ITJobBoardScraper()
    logger.info("Starting IT Job Board scraper...")
    
    try:
        jobs = scraper.scrape_all()
        scraper.save_to_csv()
        logger.info("Scraping completed successfully!")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")

if __name__ == "__main__":
    main() 