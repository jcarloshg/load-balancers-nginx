import requests
from concurrent.futures import ThreadPoolExecutor

url = "http://localhost:8080/models"
total_requests = 20000
concurrency = 10000  # How many at once

contaibility = {}


def send_request(i):
    try:
        # You can customize data here based on 'i'
        payload = {
            "name": "Starship Enterprise",
            "pieces": 1599,
            "theme": "Sci-Fi",
            "difficulty": "easy",
            "price_us": 199.99,
            "year": 2001
        }
        response = requests.post(url, json=payload)
        response_json = response.json()
        host_key = response_json.get('host')
        contaibility[host_key] = contaibility.get(host_key, 0) + 1
        # print(f"Request {i}: Status Code: {response.status_code} - host: {response_json.get('host')}")
    except Exception as e:
        print(f"Request {i} failed: {e}")


# Create a pool of workers to send requests in parallel
with ThreadPoolExecutor(max_workers=concurrency) as executor:
    executor.map(send_request, range(total_requests))

print("\n Current host distribution:")
for host, count in contaibility.items():
    print(f"    - {host}: {count}")

print("\n Load Balancer Host Distribution ")
total_requests_completed = sum(contaibility.values())
print(f"    - total request sent {total_requests}")
print(f"    - total request completed {total_requests_completed}")
