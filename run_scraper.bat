@echo off
echo ========================================
echo    Universal Web Scraper
echo ========================================
echo.
echo Installing dependencies...
pip3 install -r requirements.txt
echo.
echo ========================================
echo Choose what to scrape:
echo 1. BuiltWith Technologies
echo 2. BuiltWith Websites  
echo 3. Job Sites (Indeed, LinkedIn)
echo 4. Custom Website
echo ========================================
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Running BuiltWith Technology Scraper...
    python3 builtwith_scraper.py
) else if "%choice%"=="2" (
    echo Running BuiltWith Website Scraper...
    python3 universal_scraper.py --config configs/builtwith_websites_config.json
) else if "%choice%"=="3" (
    echo Running Job Site Scraper...
    python3 universal_scraper.py --config configs/indeed_config.json
) else if "%choice%"=="4" (
    echo Running Custom Website Scraper...
    python3 universal_scraper.py --template
    echo.
    echo Edit scraper_config.json with your website details
    echo Then run: python3 universal_scraper.py --config scraper_config.json
) else (
    echo Invalid choice!
)

echo.
echo ========================================
echo Scraping complete! Check the CSV files.
echo ========================================
pause 