import requests
import re

RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[92m"

def read_urls_from_file(file_path):
    """Read URLs from a file and ensure they start with 'http://'."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    urls = []

    for line in lines:
        line = line.strip()
        #print(line)
        #print("\n")
        if not line:
            continue
        if not line.startswith('http://') and not line.startswith('https://'):
            line = 'http://' + line
        urls.append(line)
    return urls

def check_url_content(url, pattern, redirect_target=None):
    """Request the URL and search for the target string and redirect location."""
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        final_url = response.url
        print("\n")
        print("hitting url: "+ final_url)
        #print(response.text)

        # Use regex to search the content
        if re.search(pattern, response.text, re.IGNORECASE):
            print(f"{RED}[FOUND]{RESET} Pattern '{pattern}' found on: {url}")

        else:
            print(f"{GREEN}[OK]{RESET} No pattern match on: {url}")

        # Check for redirect
        if redirect_target and redirect_target in final_url and final_url != url:
            print(f"{RED}[REDIRECT]{RESET} {url} redirected to {final_url}")
            
        else:
            print(f"{GREEN}[OK]{RESET} url {url} stayed at {final_url}")

    except requests.RequestException as e:
        print(f"[ERROR] Could not access {url}: {e}")
        print("\n")

def process_file(file_path, pattern, redirect_target=None):
    urls = read_urls_from_file(file_path)
    for url in urls:
        check_url_content(url, pattern, redirect_target)

# Example usage
if __name__ == "__main__":
    file_path = "/path/to/sites.txt"  # Your text file with URLs
    pattern = r"patter"  # The string you're searching for
    redirect_target = "redirect.com"  # Optional: check if site redirects here

    process_file(file_path, pattern, redirect_target)