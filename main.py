import requests

# List of website URLs
websites = ['https://macro.care', 'https://datac.com', 'https://lovlov.com', 'https://pikaboom.gg',
             'https://healsy.care', 'https://zimousine.com', 'https://team.datac.com', 'https://ekkram.com',
             'https://lightlogistics-eg.com']
def check_website_status(url):
    """Checks the website status and prints appropriate messages."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{url} is working perfectly! ")
        else:
            print(f"{url} is facing some errors (status code: {response.status_code}). ⚠️")
            print("Try to fix it or raise a ticket for further investigation.")
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")


for website in websites:
    check_website_status(website)