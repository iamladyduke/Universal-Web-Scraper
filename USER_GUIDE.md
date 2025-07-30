# 🚀 Simple User Guide - Universal Web Scraper

**For Non-Technical Team Members**

## 📥 How to Get Started (3 Easy Steps)

### Step 1: Download
1. Go to: https://github.com/iamladyduke/Universal-Web-Scraper
2. Click the **green "Code" button**
3. Click **"Download ZIP"**
4. Save to your computer

### Step 2: Extract & Install
1. **Right-click** the ZIP file → **"Extract All"**
2. Open the `Universal-Web-Scraper` folder
3. **Double-click** the appropriate file:
   - **Windows users**: `run_scraper.bat`
   - **Mac users**: `run_scraper.sh`

### Step 3: Choose What to Scrape
The program will ask you to choose:
- **1** = BuiltWith Technologies (what tech companies use)
- **2** = BuiltWith Websites (recently analyzed sites)
- **3** = Job Sites (Indeed, LinkedIn jobs)
- **4** = Custom Website (any website you want)

## 🎯 What Each Option Does

### Option 1: BuiltWith Technologies
- **What it scrapes**: Technology directory from BuiltWith
- **What you get**: CSV file with technology names, categories, usage stats
- **Use for**: Market research, competitive analysis

### Option 2: BuiltWith Websites
- **What it scrapes**: Recently analyzed websites
- **What you get**: CSV file with website URLs, tech stacks, traffic data
- **Use for**: Competitor research, industry analysis

### Option 3: Job Sites
- **What it scrapes**: Job listings from Indeed, LinkedIn, Glassdoor
- **What you get**: CSV file with job titles, companies, locations, descriptions
- **Use for**: Job market research, salary analysis

### Option 4: Custom Website
- **What it scrapes**: Any website you configure
- **What you get**: Custom data based on your configuration
- **Use for**: Specific research needs

## 📊 What You'll Get

After running the scraper, you'll find:
- **CSV files** in the same folder
- **Data you can open** in Excel or Google Sheets
- **Ready-to-use information** for your projects

## 🔧 Troubleshooting

### "Python not found" Error
1. Go to: https://www.python.org/downloads/
2. Download and install Python
3. **Important**: Check "Add Python to PATH" during installation
4. Try running the scraper again

### "Permission denied" Error (Mac)
1. Right-click on `run_scraper.sh`
2. Select "Get Info"
3. Check "Execute" permission
4. Try running again

### "pip3 not found" Error
1. Make sure Python is installed correctly
2. Try running: `python -m pip install -r requirements.txt`
3. Then run the scraper again

## 📈 Using the Data

### Opening CSV Files
1. **Excel**: Double-click the CSV file
2. **Google Sheets**: Upload the CSV file
3. **Numbers (Mac)**: Drag and drop the CSV file

### What You Can Do with the Data
- **Filter and sort** by any column
- **Create charts** and graphs
- **Export to reports**
- **Share with your team**

## 🎯 Common Use Cases

### For Marketing Team
- **BuiltWith Technologies**: See what tech competitors use
- **Job Sites**: Analyze hiring trends in your industry

### For Sales Team
- **BuiltWith Websites**: Research prospect technology stacks
- **Job Sites**: Understand client hiring patterns

### For Product Team
- **BuiltWith Technologies**: Identify popular technologies
- **Job Sites**: Research skill requirements

### For Research Team
- **Any option**: Collect data for analysis
- **Custom websites**: Scrape specific research targets

## ⚠️ Important Notes

### Legal & Ethical
- ✅ Only scrape publicly available data
- ✅ Don't overload websites
- ✅ Respect website terms of service
- ✅ Use data responsibly

### Rate Limiting
- The scraper automatically waits between requests
- This prevents overwhelming websites
- Scraping may take several minutes

### Data Quality
- Some websites may block automated access
- Data may be incomplete if website structure changes
- Always verify important data manually

## 🆘 Need Help?

### Common Issues
1. **"No data found"**: Website structure may have changed
2. **"Connection error"**: Check your internet connection
3. **"Permission error"**: Make sure you have write access to the folder

### Getting Support
1. Check this guide first
2. Look at the README.md file for technical details
3. Ask your technical team member for help

## 🚀 Advanced Usage

### Custom Website Scraping
1. Choose option 4
2. Edit the `scraper_config.json` file
3. Follow the instructions in the terminal

### Multiple Scrapes
- Run the scraper multiple times
- Each run creates new CSV files
- Files are named with timestamps

### Data Analysis
- Combine multiple CSV files
- Use Excel's data analysis tools
- Create pivot tables and charts

---

**Happy Scraping! 🕷️**

*This tool is for educational and research purposes. Please respect website terms of service.* 