from services.herd import extract_sites_and_paths
sites = extract_sites_and_paths()
target_path = "/Volumes/Sembark/url_shortner"
# exist_path = any(site['path'] == target_path for site in sites)
# print(exist_path)
print(sites)
url = next((site['url'] for site in sites if site['path'] == target_path), None)
print(url)
