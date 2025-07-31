import csv
import json
import random

def generate_sample_apps():
    """Generate sample app data for demonstration"""
    
    # Sample app data across different categories
    sample_apps = [
        {"name": "Instagram", "developer": "Meta Platforms, Inc.", "rating": "4.7"},
        {"name": "TikTok", "developer": "ByteDance Ltd.", "rating": "4.3"},
        {"name": "MyChart", "developer": "Epic Systems Corporation", "rating": "4.8"},
        {"name": "WhatsApp", "developer": "WhatsApp LLC", "rating": "4.6"},
        {"name": "Spotify", "developer": "Spotify AB", "rating": "4.5"},
        {"name": "Netflix", "developer": "Netflix, Inc.", "rating": "4.4"},
        {"name": "Uber", "developer": "Uber Technologies, Inc.", "rating": "4.2"},
        {"name": "Airbnb", "developer": "Airbnb, Inc.", "rating": "4.1"},
        {"name": "Zoom", "developer": "Zoom Video Communications, Inc.", "rating": "4.3"},
        {"name": "Slack", "developer": "Slack Technologies, Inc.", "rating": "4.4"},
        {"name": "Discord", "developer": "Discord Inc.", "rating": "4.5"},
        {"name": "Twitch", "developer": "Twitch Interactive, Inc.", "rating": "4.2"},
        {"name": "Reddit", "developer": "Reddit, Inc.", "rating": "4.0"},
        {"name": "Pinterest", "developer": "Pinterest, Inc.", "rating": "4.3"},
        {"name": "LinkedIn", "developer": "Microsoft Corporation", "rating": "4.1"},
        {"name": "Twitter", "developer": "Twitter, Inc.", "rating": "4.2"},
        {"name": "Snapchat", "developer": "Snap Inc.", "rating": "4.4"},
        {"name": "Telegram", "developer": "Telegram FZ LLC", "rating": "4.6"},
        {"name": "Signal", "developer": "Signal Foundation", "rating": "4.7"},
        {"name": "WeChat", "developer": "Tencent Technology (Shenzhen) Company Limited", "rating": "4.3"},
        {"name": "LINE", "developer": "LINE Corporation", "rating": "4.2"},
        {"name": "Viber", "developer": "Viber Media S.à r.l.", "rating": "4.1"},
        {"name": "Skype", "developer": "Microsoft Corporation", "rating": "4.0"},
        {"name": "FaceTime", "developer": "Apple Inc.", "rating": "4.5"},
        {"name": "Messages", "developer": "Apple Inc.", "rating": "4.4"},
        {"name": "Mail", "developer": "Apple Inc.", "rating": "4.2"},
        {"name": "Calendar", "developer": "Apple Inc.", "rating": "4.3"},
        {"name": "Photos", "developer": "Apple Inc.", "rating": "4.6"},
        {"name": "Camera", "developer": "Apple Inc.", "rating": "4.5"},
        {"name": "Maps", "developer": "Apple Inc.", "rating": "4.4"},
        {"name": "Safari", "developer": "Apple Inc.", "rating": "4.3"},
        {"name": "Chrome", "developer": "Google LLC", "rating": "4.2"},
        {"name": "Firefox", "developer": "Mozilla Corporation", "rating": "4.1"},
        {"name": "Edge", "developer": "Microsoft Corporation", "rating": "4.0"},
        {"name": "Opera", "developer": "Opera Software AS", "rating": "4.1"},
        {"name": "Brave", "developer": "Brave Software, Inc.", "rating": "4.3"},
        {"name": "DuckDuckGo", "developer": "DuckDuckGo, Inc.", "rating": "4.2"},
        {"name": "Tor Browser", "developer": "The Tor Project", "rating": "4.0"},
        {"name": "1Password", "developer": "1Password", "rating": "4.7"},
        {"name": "LastPass", "developer": "LogMeIn, Inc.", "rating": "4.3"},
        {"name": "Dashlane", "developer": "Dashlane", "rating": "4.4"},
        {"name": "Bitwarden", "developer": "Bitwarden", "rating": "4.6"},
        {"name": "Keeper", "developer": "Keeper Security, Inc.", "rating": "4.2"},
        {"name": "NordPass", "developer": "Nord Security", "rating": "4.3"},
        {"name": "RoboForm", "developer": "Siber Systems", "rating": "4.1"},
        {"name": "Enpass", "developer": "Sinew Software Systems", "rating": "4.4"},
        {"name": "Authy", "developer": "Twilio Inc.", "rating": "4.5"},
        {"name": "Google Authenticator", "developer": "Google LLC", "rating": "4.6"},
        {"name": "Microsoft Authenticator", "developer": "Microsoft Corporation", "rating": "4.4"},
        {"name": "Duo Mobile", "developer": "Cisco", "rating": "4.3"},
        {"name": "LastPass Authenticator", "developer": "LogMeIn, Inc.", "rating": "4.2"},
        {"name": "1Password Authenticator", "developer": "1Password", "rating": "4.5"},
        {"name": "Authy", "developer": "Twilio Inc.", "rating": "4.5"},
        {"name": "Google Authenticator", "developer": "Google LLC", "rating": "4.6"},
        {"name": "Microsoft Authenticator", "developer": "Microsoft Corporation", "rating": "4.4"},
        {"name": "Duo Mobile", "developer": "Cisco", "rating": "4.3"},
        {"name": "LastPass Authenticator", "developer": "LogMeIn, Inc.", "rating": "4.2"},
        {"name": "1Password Authenticator", "developer": "1Password", "rating": "4.5"}
    ]
    
    return sample_apps

def save_to_csv(apps, filename='apps.csv'):
    """Save apps data to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'developer', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(apps)
    
    print(f"✅ Saved {len(apps)} apps to {filename}")

def save_to_json(apps, filename='apps.json'):
    """Save apps data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(apps, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(apps)} apps to {filename}")

def main():
    print("📱 App Store Data Generator")
    print("=" * 50)
    print("Generating sample app data in CSV format")
    print("=" * 50)
    
    # Generate sample apps
    apps = generate_sample_apps()
    
    # Save to CSV
    save_to_csv(apps)
    
    # Save to JSON
    save_to_json(apps)
    
    # Show sample results
    print(f"\n📊 Sample Results:")
    for i, app in enumerate(apps[:10], 1):
        print(f"{i:2d}. {app['name']} by {app['developer']} (Rating: {app['rating']})")
    
    print(f"\n✅ Generated {len(apps)} sample apps!")
    print("📄 Files created: apps.csv, apps.json")

if __name__ == "__main__":
    main() 