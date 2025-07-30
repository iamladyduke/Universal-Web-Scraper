# Universal Web Scraper

A powerful, configurable web scraper that can extract data from **any website** using JSON configuration files.

## 🚀 Features

- **Universal Compatibility**: Works with any website using CSS selectors
- **Configurable Fields**: Extract any data you want (text, links, attributes)
- **Pagination Support**: Automatically handles multiple pages
- **Rate Limiting**: Respectful scraping with configurable delays
- **Multiple Output Formats**: CSV and JSON export
- **Error Handling**: Robust error recovery and logging
- **Pre-built Configs**: Ready-to-use configurations for popular job sites

## 📦 Installation

```bash
pip3 install -r requirements.txt
```

## 🎯 Quick Start

### 1. Create a Configuration Template
```bash
python3 universal_scraper.py --template
```

### 2. Edit the Configuration
Open `scraper_config.json` and customize:
- `base_url`: The website URL to scrape
- `item_selector`: CSS selector for items (e.g., `div.job-item`)
- `fields`: What data to extract from each item

### 3. Run the Scraper
```bash
python3 universal_scraper.py --config scraper_config.json
```

## 📋 Usage Examples

### Scrape Indeed Jobs
```bash
python3 universal_scraper.py --config configs/indeed_config.json --output indeed_jobs.csv
```

### Scrape LinkedIn Jobs
```bash
python3 universal_scraper.py --config configs/linkedin_config.json --output linkedin_jobs.csv
```

### Scrape Glassdoor Jobs
```bash
python3 universal_scraper.py --config configs/glassdoor_config.json --output glassdoor_jobs.csv
```

### Scrape BuiltWith Technologies
```bash
python3 universal_scraper.py --config configs/builtwith_technologies_config.json --output builtwith_tech.csv
```

### Scrape BuiltWith Websites
```bash
python3 universal_scraper.py --config configs/builtwith_websites_config.json --output builtwith_sites.csv
```

### Export as JSON
```bash
python3 universal_scraper.py --config scraper_config.json --format json --output data.json
```

## ⚙️ Configuration Format

```json
{
  "base_url": "https://example.com/jobs",
  "item_selector": "div.job-item",
  "fields": {
    "title": {
      "selector": "h2.title",
      "attribute": "text"
    },
    "company": {
      "selector": ".company-name",
      "attribute": "text"
    },
    "link": {
      "selector": "a.title",
      "attribute": "href"
    }
  },
  "pagination": {
    "enabled": true,
    "pattern": "?page={page}",
    "max_pages": 100
  },
  "rate_limiting": {
    "delay_min": 0.5,
    "delay_max": 1.0
  },
  "max_items": 5000
}
```

## 🔧 Configuration Options

### Field Types
- `"text"`: Extract text content
- `"href"`: Extract link URLs
- `"src"`: Extract image sources
- `"class"`: Extract CSS classes
- Any HTML attribute: `"data-id"`, `"title"`, etc.

### Pagination Patterns
- `"?page={page}"`: Standard page parameter
- `"&start={page}"`: Start parameter
- `"/page/{page}"`: Path-based pagination
- `"&offset={page}"`: Offset-based pagination

### Rate Limiting
- `delay_min`: Minimum delay between requests (seconds)
- `delay_max`: Maximum delay between requests (seconds)

## 🌐 Supported Websites

### Job Sites (Pre-configured)
- ✅ Indeed
- ✅ LinkedIn Jobs
- ✅ Glassdoor
- ✅ IT Job Board
- ✅ Any job site with custom config

### Technology Analysis Sites
- ✅ BuiltWith (technology directory, website analysis)
- ✅ Wappalyzer (technology detection)
- ✅ Any tech analysis site with custom config

### Other Data Types
- 📰 News articles
- 🏪 E-commerce products
- 📊 Financial data
- 🏠 Real estate listings
- 📚 Educational content
- 🎬 Entertainment listings

## 🛠️ Advanced Usage

### Custom Field Extraction
```json
{
  "price": {
    "selector": ".price",
    "attribute": "text"
  },
  "image": {
    "selector": "img.product-image",
    "attribute": "src"
  },
  "rating": {
    "selector": ".rating",
    "attribute": "data-rating"
  }
}
```

### Multiple Selectors
```json
{
  "title": {
    "selector": "h1.title, h2.title, .job-title",
    "attribute": "text"
  }
}
```

### Conditional Extraction
```json
{
  "salary": {
    "selector": ".salary, .compensation",
    "attribute": "text"
  }
}
```

## 📊 Output Formats

### CSV Output
```csv
title,company,location,link,date
"Software Engineer","Tech Corp","London","https://...","2025-07-17"
"Data Scientist","AI Company","Remote","https://...","2025-07-16"
```

### JSON Output
```json
[
  {
    "title": "Software Engineer",
    "company": "Tech Corp",
    "location": "London",
    "link": "https://...",
    "date": "2025-07-17"
  }
]
```

## 🔍 Finding CSS Selectors

### Using Browser Developer Tools
1. Right-click on the element you want to extract
2. Select "Inspect Element"
3. Right-click on the highlighted HTML
4. Copy > Copy selector

### Common Selectors
- `div.class-name`: Elements with specific class
- `#id-name`: Element with specific ID
- `tag.class`: Specific tag with class
- `parent > child`: Direct child relationship
- `ancestor descendant`: Any descendant relationship

## ⚠️ Important Notes

### Legal & Ethical Considerations
- ✅ Check website's Terms of Service
- ✅ Respect robots.txt files
- ✅ Use reasonable rate limiting
- ✅ Don't overload servers
- ✅ Only scrape publicly available data

### Technical Limitations
- ❌ JavaScript-rendered content (use Selenium for this)
- ❌ CAPTCHA-protected pages
- ❌ Login-required content
- ❌ Anti-bot protected sites

## 🚀 Performance Tips

### Optimize Speed
- Reduce `delay_min` and `delay_max`
- Increase `max_pages` for more data
- Use specific CSS selectors

### Handle Large Datasets
- Increase `max_items` for more data
- Use JSON format for complex data
- Split scraping into multiple runs

## 🐛 Troubleshooting

### Common Issues

**"No items found"**
- Check if the CSS selector is correct
- Verify the website structure hasn't changed
- Try different selectors

**"Rate limited"**
- Increase delay values
- Add more random delays
- Use proxy rotation (advanced)

**"Permission denied"**
- Check file write permissions
- Run with appropriate user privileges

## 📈 Extending the Scraper

### Add New Data Sources
1. Create new config file
2. Define CSS selectors
3. Test with small sample
4. Scale up to full scraping

### Custom Output Formats
- Modify `save_to_csv()` or `save_to_json()`
- Add database integration
- Create custom exporters

## 🤝 Contributing

### Adding New Configurations
1. Create config file in `configs/` directory
2. Test with target website
3. Document any special requirements
4. Update this README

### Improving the Scraper
- Add new field types
- Implement JavaScript rendering
- Add proxy support
- Create GUI interface

## 📄 License

This project is for educational and research purposes. Please respect website terms of service and robots.txt files.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your configuration
3. Test with a simple website first
4. Check website's robots.txt

---

**Happy Scraping! 🕷️** 