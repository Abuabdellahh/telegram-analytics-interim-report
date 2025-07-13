import os
import json
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramScraper:
    def __init__(self):
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.client = None
        self.target_channels = [
            'lobelia4cosmetics',
            'tikvahpharma'
            # Add more channels as needed
        ]

    async def start(self):
        """Initialize Telegram client and start scraping"""
        try:
            self.client = TelegramClient('session_name', self.api_id, self.api_hash)
            await self.client.start()
            logger.info('Telegram client started successfully')
            
            for channel in self.target_channels:
                await self.scrape_channel(channel)
                
        except Exception as e:
            logger.error(f'Error starting scraper: {str(e)}')
        finally:
            if self.client:
                await self.client.disconnect()

    async def scrape_channel(self, channel):
        """Scrape messages from a specific channel"""
        try:
            logger.info(f'Starting to scrape channel: {channel}')
            
            # Get channel entity
            entity = await self.client.get_entity(channel)
            
            # Create directory structure
            current_date = datetime.now().strftime('%Y-%m-%d')
            channel_dir = os.path.join('data', 'raw', current_date, channel)
            os.makedirs(channel_dir, exist_ok=True)
            
            # Collect messages
            messages = []
            async for message in self.client.iter_messages(entity, limit=1000):
                message_data = {
                    'id': message.id,
                    'date': str(message.date),
                    'text': message.text,
                    'sender_id': message.sender_id,
                    'channel': channel,
                    'media': None
                }
                
                # Handle media (images/documents)
                if message.media:
                    if isinstance(message.media, MessageMediaPhoto) or isinstance(message.media, MessageMediaDocument):
                        media_path = os.path.join(channel_dir, f'media_{message.id}')
                        await self.client.download_media(message, media_path)
                        message_data['media'] = media_path
                
                messages.append(message_data)
            
            # Save messages to JSON
            output_file = os.path.join(channel_dir, 'messages.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            
            logger.info(f'Successfully scraped {len(messages)} messages from {channel}')
            
        except Exception as e:
            logger.error(f'Error scraping channel {channel}: {str(e)}')

if __name__ == '__main__':
    scraper = TelegramScraper()
    scraper.start()
