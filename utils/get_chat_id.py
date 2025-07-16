import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TG_BOT_API_TOKEN = os.getenv('TG_BOT_API_TOKEN')

def main() -> None:
    """Get chat IDs from recent Telegram updates."""
    if not TG_BOT_API_TOKEN:
        print("TG_BOT_API_TOKEN not found in environment variables.")
        return
    
    # Get recent updates
    response = requests.get(
        f'https://api.telegram.org/bot{TG_BOT_API_TOKEN}/getUpdates'
    )
    
    if response.status_code != 200:
        print(f"Error fetching updates: {response.status_code}")
        return
    
    data = response.json()
    if not data['ok'] or not data['result']:
        print("No recent updates found.")
        print("Send a message to your bot first, then run this script.")
        return
    
    # Process updates and show chat info
    for update in data['result']:
        if 'message' in update:
            msg = update['message']
            chat = msg['chat']
            user = msg.get('from', {})
            
            print(f"Chat ID: {chat['id']}")
            print(f"Chat Type: {chat['type']}")
            print(f"Chat Title: {chat.get('title', 'N/A')}")
            print(f"From User: {user.get('first_name', '')} {user.get('last_name', '')}")
            print(f"Username: @{user.get('username', 'N/A')}")
            
        elif 'channel_post' in update:
            post = update['channel_post']
            chat = post['chat']
            
            print(f"Chat ID: {chat['id']}")
            print(f"Chat Type: {chat['type']}")
            print(f"Chat Title: {chat.get('title', 'N/A')}")
            print(f"From User: Channel Post")
            print(f"Username: @{chat.get('username', 'N/A')}")

if __name__ == '__main__':
    main()