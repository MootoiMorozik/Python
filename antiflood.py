import time
from collections import defaultdict, deque
import telebot

TOKEN = "7233027521:AAGIxnIi_zpU2fFLjL6_djhWxL_zC56ueLE"
bot = telebot.TeleBot(TOKEN)

MAX_MSG = 5
TIME_WINDOW = 2
COOLDOWN = 1.6

ALLOWED_CHAT_ID = -1002609669932

user_messages = defaultdict(lambda: defaultdict(lambda: deque()))
flooding_users = defaultdict(dict)
exited_chats = set()

@bot.my_chat_member_handler()
def handle_chat_member_update(update):
    chat_id = update.chat.id
    new_status = update.new_chat_member.status
    
    if new_status in ['member', 'administrator'] and chat_id != ALLOWED_CHAT_ID:
        if chat_id not in exited_chats:
            try:
                bot.send_message(chat_id, "🚫 Этот бот предназначен только для определенной группы. Я покидаю этот чат.")
                time.sleep(0.5)
            except:
                pass
            
            try:
                bot.leave_chat(chat_id)
                exited_chats.add(chat_id)
            except Exception:
                pass

@bot.message_handler(content_types=[
    'text', 'photo', 'sticker', 'animation', 
    'video', 'document', 'audio', 'voice'
])
def handle_all(message):
    chat_id = message.chat.id
    
    if chat_id != ALLOWED_CHAT_ID:
        if chat_id not in exited_chats:
            try:
                bot.send_message(chat_id, "🚫 Этот бот не предназначен для работы в данной группе. Я покидаю чат.")
                time.sleep(0.5)
            except:
                pass
            try:
                bot.leave_chat(chat_id)
                exited_chats.add(chat_id)
            except Exception:
                pass
        return

    user_id = message.from_user.id
    msg_id = message.message_id
    now = time.time()

    if user_id in flooding_users and chat_id in flooding_users[user_id]:
        if now < flooding_users[user_id][chat_id]:
            try:
                bot.delete_message(chat_id, msg_id)
            except Exception:
                pass
            return
        else:
            del flooding_users[user_id][chat_id]
            if not flooding_users[user_id]:
                del flooding_users[user_id]

    chat_queue = user_messages[user_id][chat_id]
    chat_queue.append((now, msg_id))
    
    while chat_queue and now - chat_queue[0][0] > 60:
        chat_queue.popleft()

    recent_count = 0
    for i in range(len(chat_queue)-1, -1, -1):
        if now - chat_queue[i][0] <= TIME_WINDOW:
            recent_count += 1
        else:
            break

    if recent_count >= MAX_MSG:
        flooding_users.setdefault(user_id, {})[chat_id] = now + COOLDOWN
        
        for _, mid in list(chat_queue):
            try:
                bot.delete_message(chat_id, mid)
            except Exception:
                pass
        
        chat_queue.clear()

bot.polling(none_stop=True)