#!/bin/bash

echo "========================================"
echo "   Universal Web Scraper"
echo "========================================"
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt
echo ""
echo "========================================"
echo "Choose what to scrape:"
echo "1. BuiltWith Technologies"
echo "2. BuiltWith Websites"
echo "3. Job Sites (Indeed, LinkedIn)"
echo "4. App Stores (Google Play, Apple App Store)"
echo "5. Custom Website"
echo "========================================"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "Running BuiltWith Technology Scraper..."
        python3 builtwith_scraper.py
        ;;
    2)
        echo "Running BuiltWith Website Scraper..."
        python3 universal_scraper.py --config configs/builtwith_websites_config.json
        ;;
    3)
        echo "Running Job Site Scraper..."
        python3 universal_scraper.py --config configs/indeed_config.json
        ;;
    4)
        echo "Running App Store Scraper..."
        python3 appstore_scraper.py
        ;;
    5)
        echo "Running Custom Website Scraper..."
        python3 universal_scraper.py --template
        echo ""
        echo "Edit scraper_config.json with your website details"
        echo "Then run: python3 universal_scraper.py --config scraper_config.json"
        ;;
    *)
        echo "Invalid choice!"
        ;;
esac

echo ""
echo "========================================"
echo "Scraping complete! Check the CSV files."
echo "========================================" 