import requests
import time

def check_website(url):
    """
    Checks if a website is reachable and returns its response time.
    Args:
        url (str): The URL to check.
    Returns:
        dict: {'status': 'Online'|'Offline', 'response_code': int, 'response_time': float (ms)}
    """
    if not url.startswith('http'):
        url = 'https://' + url
        
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000 # to ms
        
        return {
            'status': 'Online' if response.status_code == 200 else f'Error ({response.status_code})',
            'response_code': response.status_code,
            'response_time': round(response_time, 2)
        }
    except requests.exceptions.Timeout:
        return {
            'status': 'Offline (Timeout)',
            'response_code': 0,
            'response_time': 0
        }
    except requests.exceptions.ConnectionError:
        return {
            'status': 'Offline (Connection Error)',
            'response_code': 0,
            'response_time': 0
        }
    except Exception as e:
        return {
            'status': f'Error: {str(e)}',
            'response_code': 0,
            'response_time': 0
        }
