"""
Author: Lau Chun Hin Kelvin
Version: 1.0.0 @2024
Telegram Polling Bot Framework
A robust Python framework for automated Telegram polling with vote collection
"""

import logging
import asyncio
from datetime import datetime, timedelta
import pytz
import threading
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from telegram import Bot, Update
from telegram.ext import Application, PollAnswerHandler
from enum import Enum

# Load environment variables
load_dotenv()

# Configuration
TG_BOT_API_TOKEN = os.environ.get('TG_BOT_API_TOKEN')
MONGODB_URI = os.environ.get('MONGODB_URI')
TG_CHAT_ID = int(os.environ.get('TG_CHAT_ID', 0))
DB_NAME = os.environ.get('DATABASE_NAME', 'Testing_TG_DB')

# Poll Configuration
POLL_DURATION_IN_MINS = int(os.environ.get('POLL_DURATION_IN_MINS', 60))
POLL_OPTIONS = os.environ.get('POLL_OPTIONS', 'Option A,Option B').split(',')
REMINDER_MINS = int(os.environ.get('REMINDER_MINS', 15))

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger('httpx').setLevel(logging.WARNING)

# MongoDB connection
if MONGODB_URI:
    mongo_client = MongoClient(MONGODB_URI)
    db = mongo_client[DB_NAME]
    db_votes = db.votes
    db_polls = db.polls
else:
    logger.warning("MongoDB URI not found. Database features will be disabled.")
    db_votes = db_polls = None


class PollStatus(Enum):
    """Poll status outcomes"""
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class BotManager:
    """Manages all bot operations including polling and messaging"""
    
    def __init__(self):
        self.poll_payload = {}
        self.reset_poll_payload()
    
    def reset_poll_payload(self):
        """Reset poll payload to initial state"""
        self.poll_payload = {
            "_id": None,
            "message_ids": [],
            "poll_creation_date": None,
            "poll_message_id": None,
            "total_votes": 0,
            "option_votes": [],
            "status": PollStatus.ACTIVE.value,
            "poll_question": None,
            "poll_options": [],
            "poll_start_time": None,
            "poll_end_time": None
        }
    
    def update_poll_data(self, poll_msg, current_time, poll_question):
        """Update poll payload with initial data"""
        self.poll_payload.update({
            "_id": poll_msg.poll.id,
            "poll_message_id": poll_msg.message_id,
            "poll_creation_date": current_time.date().isoformat(),
            "poll_start_time": current_time.isoformat(),
            "poll_question": poll_question,
            "poll_options": POLL_OPTIONS.copy(),
            "message_ids": [poll_msg.message_id],
            "status": PollStatus.ACTIVE.value
        })
        return self.poll_payload

    def add_message_id(self, message_id):
        """Add a message ID to tracking list"""
        if message_id:
            self.poll_payload["message_ids"].append(message_id)
    
    async def send_image(self, bot, chat_id, image_path=None, caption=""):
        """Send an image to the chat - can be a file path or URL"""
        try:
            if image_path:
                # If image_path is provided, send it
                if image_path.startswith('http'):
                    # It's a URL
                    message = await bot.send_photo(
                        chat_id=chat_id,
                        photo=image_path,
                        caption=caption,
                        parse_mode="HTML",
                        protect_content=True,
                    )
                else:
                    # It's a local file
                    with open(image_path, 'rb') as photo:
                        message = await bot.send_photo(
                            chat_id=chat_id,
                            photo=photo,
                            caption=caption,
                            parse_mode="HTML",
                            protect_content=True,
                        )
                
                logger.info("Sent image to Telegram")
                return message
            else:
                logger.info("No image path provided, skipping image send")
                return None
                
        except Exception as e:
            logger.error(f"Failed to send image: {e}")
            return None
    
    async def delete_message(self, bot, chat_id, message_id):
        """Delete a specific message"""
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f"Deleted message {message_id}")
        except Exception as e:
            logger.error(f"Failed to delete message {message_id}: {e}")

    async def _send_poll(self, bot, chat_id, poll_question):
        """Send the poll message"""
        return await bot.send_poll(
            chat_id=chat_id,
            question=poll_question,
            options=POLL_OPTIONS,
            is_anonymous=False,
            allows_multiple_answers=False,
            protect_content=True,
        )
    
    async def _send_image(self, bot, chat_id, image_path, image_caption):
        """Send optional image and track message ID"""
        if image_path:
            image_message = await self.send_image(bot, chat_id, image_path, image_caption)
            if image_message:
                self.add_message_id(image_message.message_id)
            return image_message
        return None
    
    async def _run_poll_lifecycle(self, bot, chat_id):
        """Handle the complete poll lifecycle"""
        # Wait and send reminder
        await asyncio.sleep((POLL_DURATION_IN_MINS - REMINDER_MINS) * 60)
        reminder_message = await self._send_reminder(bot, chat_id)
        
        # Wait for poll to end
        await asyncio.sleep(REMINDER_MINS * 60)
        
        # Close poll and process results
        closed_poll = await self._close_and_process_poll(bot, chat_id)
        
        # Clean up and save
        await self._cleanup_and_save(bot, chat_id, reminder_message)
        
        # Graceful shutdown
        self._shutdown()
    
    async def _send_reminder(self, bot, chat_id):
        """Send reminder message"""
        reminder_text = f"⏰ <b>Reminder!</b>\n\nPoll closes in {REMINDER_MINS} minutes!\nMake sure to cast your vote! 🗳️"
        reminder_message = await bot.send_message(
            chat_id=chat_id,
            text=reminder_text,
            parse_mode="HTML",
            protect_content=True,
        )
        logger.info(f"Sent {REMINDER_MINS}-minute reminder")
        return reminder_message
    
    async def _close_and_process_poll(self, bot, chat_id):
        """Close poll and process results"""
        # Close poll
        closed_poll = await bot.stop_poll(
            chat_id=chat_id,
            message_id=self.poll_payload["poll_message_id"],
        )
        
        logger.info("Poll closed successfully")
        
        # Process results
        total_votes = closed_poll.total_voter_count
        self.poll_payload.update({
            "total_votes": total_votes,
            "status": PollStatus.CLOSED.value,
            "poll_end_time": datetime.now(pytz.timezone('UTC')).isoformat()
        })
        
        winning_option = self._process_poll_results(closed_poll, total_votes)
        
        # Send conclusion message
        await self._send_conclusion(bot, chat_id, total_votes, winning_option)
        
        return closed_poll
    
    def _process_poll_results(self, closed_poll, total_votes):
        """Process poll results and determine winner"""
        if total_votes > 0:
            options = closed_poll.options
            option_votes = []
            max_votes = 0
            
            for option in options:
                vote_count = option.voter_count
                percentage = (vote_count / total_votes) * 100
                logger.info(f"Option '{option.text}': {vote_count} votes ({percentage:.1f}%)")
                
                option_votes.append({
                    "option_text": option.text,
                    "votes": vote_count,
                    "percentage": percentage
                })
                
                max_votes = max(max_votes, vote_count)
            
            self.poll_payload["option_votes"] = option_votes
            
            # Determine winner(s)
            winners = [opt for opt in option_votes if opt["votes"] == max_votes]
            if len(winners) > 1:
                return "Tie between: " + ", ".join([w["option_text"] for w in winners])
            else:
                return winners[0]["option_text"]
        else:
            logger.warning("No votes received")
            self.poll_payload["option_votes"] = []
            return "No votes received"
    
    async def _send_conclusion(self, bot, chat_id, total_votes, winning_option):
        """Send poll conclusion message"""
        conclusion_text = (
            "📊 <b>Poll Results</b>\n\n"
            f"Total Votes: {total_votes}\n"
        )
        
        for vote_data in self.poll_payload["option_votes"]:
            conclusion_text += f"{vote_data['option_text']}: {vote_data['votes']} votes ({vote_data['percentage']:.1f}%)\n"
        
        conclusion_text += f"\n<b>Result: {winning_option}</b>\n\n"
        
        await bot.send_message(
            chat_id=chat_id,
            text=conclusion_text,
            parse_mode="HTML",
            protect_content=True,
        )
    
    async def _cleanup_and_save(self, bot, chat_id, reminder_message):
        """Cleanup messages and save poll data"""
        # Delete tracked messages (except poll and conclusion) - use set to avoid duplicates
        unique_message_ids = set(self.poll_payload["message_ids"])
        for message_id in unique_message_ids:
            if message_id != self.poll_payload["poll_message_id"]:
                await self.delete_message(bot, chat_id, message_id)
        
        # Delete reminder message
        if reminder_message:
            await self.delete_message(bot, chat_id, reminder_message.message_id)
        
        # Save poll data to database
        if db_polls is not None:
            db_polls.insert_one(self.poll_payload)
            logger.info("Poll data saved to database")
    
    def _shutdown(self):
        """Graceful shutdown"""
        logger.info("Poll workflow completed successfully")
        asyncio.get_event_loop().stop()
        os._exit(0)

    async def post_poll(self, application, image_path=None, image_caption=""):
        """Main polling workflow"""
        try:
            bot = Bot(TG_BOT_API_TOKEN)
            chat_id = TG_CHAT_ID
            current_time = datetime.now(pytz.timezone('UTC'))
            
            logger.info("=================== Starting Poll ===================")
            
            # Create poll question
            poll_question = f"📊 Daily Poll - {current_time.strftime('%Y-%m-%d %H:%M UTC')}"
            
            # Send poll
            poll_msg = await self._send_poll(bot, chat_id, poll_question)
            
            logger.info(f"Poll posted with ID: {poll_msg.poll.id}")
            
            # Update poll payload
            self.poll_payload["_id"] = poll_msg.poll.id
            self.poll_payload["poll_message_id"] = poll_msg.message_id
            self.poll_payload["poll_creation_date"] = current_time.date().isoformat()
            self.poll_payload["poll_question"] = poll_question
            self.poll_payload["poll_options"] = POLL_OPTIONS.copy()
            self.poll_payload["message_ids"].append(poll_msg.message_id)
            
            # Send accompanying image if provided
            if image_path:
                await self._send_image(bot, chat_id, image_path, image_caption)
            
            # Handle the complete poll lifecycle
            await self._run_poll_lifecycle(bot, chat_id)
            
        except Exception as e:
            logger.error(f"Failed to execute poll workflow: {e}", exc_info=True)
            os._exit(1)

    async def receive_poll_answer(self, update: Update, context):
        """Handle incoming poll answers"""
        try:
            poll_answer = update.poll_answer
            user_id = poll_answer.user.id
            username = poll_answer.user.username or "Unknown"
            selected_option = poll_answer.option_ids[0]
            
            logger.info(f"User {username} ({user_id}) voted: {POLL_OPTIONS[selected_option]}")
            
            # Save vote to database
            if db_votes is not None:
                vote_entry = {
                    '_id': f"{user_id}-{poll_answer.poll_id}",
                    'user_id': user_id,
                    'selected_option': selected_option,
                    'poll_id': poll_answer.poll_id,
                    'poll_creation_date': self.poll_payload["poll_creation_date"],
                    'vote_timestamp': datetime.now(pytz.timezone('UTC')).isoformat(),
                    'username': username
                }
                
                db_votes.insert_one(vote_entry)
                logger.info("Vote saved to database")
        
        except Exception as e:
            logger.error(f"Error processing poll answer: {e}", exc_info=True)


def run_in_new_loop(coroutine):
    """Run coroutine in a new event loop"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coroutine)


def main():
    """Main entry point"""
    if not TG_BOT_API_TOKEN:
        logger.error("TG_BOT_API_TOKEN not found in environment variables")
        return
    
    if not TG_CHAT_ID:
        logger.error("TG_CHAT_ID not found in environment variables")
        return
    
    logger.info("Starting Telegram Polling Bot...")
    
    # Create application
    application = Application.builder().token(TG_BOT_API_TOKEN).build()
    bot_manager = BotManager()
    
    # Add handlers
    application.add_handler(PollAnswerHandler(bot_manager.receive_poll_answer))
    
    # Get optional image settings from environment
    image_path = os.environ.get('DEFAULT_IMAGE_PATH')
    image_caption = os.environ.get('DEFAULT_IMAGE_CAPTION', '')
    enable_image = os.environ.get('ENABLE_IMAGE_SENDING', 'false').lower() == 'true'
    
    # Start poll in separate thread
    if enable_image and image_path:
        threading.Thread(
            target=run_in_new_loop, 
            args=(bot_manager.post_poll(application, image_path, image_caption),)
        ).start()
    else:
        threading.Thread(
            target=run_in_new_loop, 
            args=(bot_manager.post_poll(application),)
        ).start()
    
    # Start polling for updates
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
