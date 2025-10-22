import requests
import random
import time

def generate_video(prompt, api_key, endpoint, proxies):
    max_retries = 5
    for attempt in range(max_retries):
        proxy = random.choice(proxies)
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "prompt": prompt,
                "duration": 8,  # 8 seconds per scene
                "model": "veo3_fast",
                "watermark": "MyBrand",
                "aspectRatio": "16:9",
                "seeds": 12345,
                "enableFallback": False,
                "enableTranslation": True,
                "generationType": "TEXT_2_VIDEO"
            }
            response = requests.post(endpoint, json=data, headers=headers, proxies=proxy)
            if response.status_code == 200:
                return response.json().get('video_url')
            elif response.status_code == 429:  # Rate limit
                wait_time = int(response.headers.get('Retry-After', 60))
                time.sleep(wait_time * (attempt + 1))  # Exponential backoff
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Retry {attempt}: {e}")
            time.sleep(2 ** attempt)  # Backoff
    return None
