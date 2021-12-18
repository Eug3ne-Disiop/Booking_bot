import telebot
from telebot import types
import config
import ch_text

bot = telebot.TeleBot(config.tokenbot)

user_dict = {}
user_chats = 0


class User:
    def __init__(self, name):
        self.name = name
        self.idt = None
        self.alones = None
        self.sex = None

        keys = ['idt', 'alones', 'book_t', 'will_learn', 'share_r', 'want_a']
        for key in keys:
            self.key = None


# /start and /report placeholder
@bot.message_handler(commands=['start'])
def send_welcome(message):
    img = open('title.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    welcome_user = f'Hi!, {message.from_user.first_name} {message.from_user.last_name}' + ch_text.intro_text

    bot.send_message(message.chat.id, welcome_user)

    
@bot.message_handler(commands=['report'])
def report_message(message):
    msg = bot.send_message(message.from_user.id, ch_text.report_text)
    bot.register_next_step_handler(msg, report_to_group)
def report_to_group(message):
    report = message.text
    user_name = message.from_user.username
    user_nick = message.from_user.first_name

    bot.send_message(message.from_user.id, ch_text.report_answer)
    bot.send_message(config.groupid, user_name + '(' + user_nick + ')' + 'Sent a report: ' + report)

@bot.message_handler(commands=['return'])
def send_welcome(message):
    bot.send_message(message.from_user.id, ch_text.return_text)
    
@bot.message_handler(commands=['reg'])
def send_welcome1(message):
    try:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, ch_text.fullname_text)
        bot.register_next_step_handler(msg, process_name_step)


    except Exception as e:

        bot.reply_to(message, 'ops0')

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.send_message(chat_id, ch_text.id_text)
        bot.register_next_step_handler(msg, process_idt_step)
    except Exception as e:
        bot.reply_to(message, 'ops1')

# room booking

def process_idt_step(message):
    try:
        chat_id = message.chat.id
        idt = message.text
        if not idt.isdigit():
            msg = bot.send_message(chat_id, ch_text.wrong_id_text)
            bot.register_next_step_handler(msg, process_idt_step)
            return
        user = user_dict[chat_id]
        user.idt = idt
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(ch_text.room1t, ch_text.room2t, ch_text.room3t, ch_text.room4t, ch_text.room4t, ch_text.room5t, ch_text.room6t)
        msg = bot.send_message(chat_id, ch_text.room_ques,
                               reply_markup=markup)
        bot.register_next_step_handler(msg, process_alone_step)
    except Exception as e:
        bot.reply_to(message, 'ops')

# question

def process_alone_step(message):
    try:
        chat_id = message.chat.id
        alone = message.text
        user = user_dict[chat_id]
        user.alones = alone

        msg = bot.send_message(chat_id, ch_text.quant_ques)
        bot.register_next_step_handler(msg, process_book_t_step)
    except Exception as e:
        bot.reply_to(message, 'bugg10')

# booking time

def process_book_t_step(message):
    try:
        chat_id = message.chat.id
        book_t1 = message.text
        user = user_dict[chat_id]
        user.book_t = book_t1
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(ch_text.btime1, ch_text.btime2, ch_text.btime3, ch_text.btime4, ch_text.btime5, ch_text.btime6)
        msg = bot.send_message(chat_id, ch_text.btime_ques, reply_markup=markup)
        bot.register_next_step_handler(msg, process_what_w_step)

    except Exception as e:
        bot.reply_to(message, 'bugg1')

# qurpose question

def process_what_w_step(message):
    try:
        chat_id = message.chat.id
        will_learn = message.text
        user = user_dict[chat_id]
        user.will_learn = will_learn
        msg = bot.send_message(chat_id,
                               ch_text.purp_ques)
        bot.register_next_step_handler(msg, process_share_r_step)
    except Exception as e:
        bot.reply_to(message, 'bug 12')
        
# sharing

def process_share_r_step(message):
    try:
        chat_id = message.chat.id
        share_r = message.text
        user = user_dict[chat_id]
        user.share_r = share_r
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(ch_text.share_yes, ch_text.share_no)
        msg = bot.send_message(chat_id, ch_text.share_ques, reply_markup=markup)
        bot.register_next_step_handler(msg, process_want_a_step)
    except Exception as e:
        bot.reply_to(message, 'bug 22')

# forward message

def process_want_a_step(message):
    try:
        global user_chats

        chat_id = message.chat.id
        want_adm = message.text
        name = message.from_user.username
        name1 = message.from_user.first_name
        user = user_dict[chat_id]
        user.want_a = want_adm
        bot.send_message(message.from_user.id, f'{ch_text.fullname_forward} - {user.name} \n'
                         + f'{ch_text.id_forward}  -  {user.idt} \n'
                         + f'{ch_text.room_forward}  -  {user.alones} \n'
                         + f'{ch_text.num_forward}  -  {user.book_t} \n'
                         + f'{ch_text.book_forward}  -  {user.will_learn} \n'
                         + f'{ch_text.process_forward}  -  {user.share_r} \n'
                         + f'{ch_text.sharing_forward}  -  {user.want_a}')

        markup = types.InlineKeyboardMarkup()
        site_btn = types.InlineKeyboardButton( text='Yes',  callback_data='yes')
        site_btn1 = types.InlineKeyboardButton(text='No', callback_data='no')
        markup.add(site_btn, site_btn1)
        user_chats = message.from_user.id

        bot.send_message(config.groupid, 'from ' + name + ' (' + name1 + ') ' + '\n'
                         + f'{ch_text.fullname_forward} - {user.name} \n'
                         + f'{ch_text.id_forward}  -  {user.idt} \n'
                         + f'{ch_text.room_forward}  -  {user.alones} \n'
                         + f'{ch_text.num_forward}  -  {user.book_t} \n'
                         + f'{ch_text.book_forward}  -  {user.will_learn} \n'
                         + f'{ch_text.process_forward}  -  {user.share_r} \n'
                         + f'{ch_text.sharing_forward}  -  {user.want_a}', reply_markup=markup)


    except Exception as e:
        bot.reply_to(message, 'bug 23')

# decision

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    try:

        if call.data == 'yes':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=ch_text.emoji_yes, reply_markup=None)
            bot.send_message(call.message.chat.id,
                         call.from_user.first_name + '(' + call.from_user.username + ')' + ' said "Yes"')
            bot.send_message(user_chats, ch_text.emoji_yes_answer)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=ch_text.emoji_no, reply_markup=None)
            bot.send_message(call.message.chat.id,
                         call.from_user.first_name + '(' + call.from_user.username + ')' + ' said "No"')
            bot.send_message(user_chats, ch_text.emoji_no_answer)
    except Exception as e:
        bot.reply_to('123!')

# maybe later

# def process_sex_step(message):
#   try:
#        chat_id = message.chat.id
#        sex = message.text
#        user = user_dict[chat_id]
#
#        user.sex = sex
#
#        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n idt:' + str(user.idt) + '\n Sex:' + user.sex)
#    except Exception as e:
#        bot.reply_to(message, 'oooops')

bot.polling()
