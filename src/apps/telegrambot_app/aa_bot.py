import requests
import telebot
from telebot import types

url = 'http://0.0.0.0:8002/api/v1/igla-chat/ask/'
headers = {'content-type': 'application/json', 'accept': 'application/json'}
aa_bot = telebot.TeleBot('')

@aa_bot.message_handler(commands=['start'])
def startBot(message):
  first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, Привет!\nЯ - бот сервисной поддержки и помогаю операторам искать нужную информацию в базе знаний. Хочешь начать работу?"
  markup = types.InlineKeyboardMarkup()
  button_yes = types.InlineKeyboardButton(text = 'Да', callback_data='yes')
  markup.add(button_yes)
  aa_bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)
    
@aa_bot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
    if (function_call.data == "yes")|(function_call.data == "next"):
      first_mess = "Какой у тебя вопрос?"
      aa_bot.send_message(function_call.message.chat.id, first_mess)
      aa_bot.answer_callback_query(function_call.id)
        
    if (function_call.data == "feedback"):
      second_mess = "Прошу ответить на ряд вопросов по качестве генерации. Полученный ответ содержит всю необходимую информацию, чтобы оказать сервисную поддержку?"
      markup = types.InlineKeyboardMarkup()
      buttons = []
      buttons.append(types.InlineKeyboardButton(text = "Да", callback_data='feedback_yes_q1'))
      buttons.append(types.InlineKeyboardButton(text = 'Нет', callback_data='feedback_no_q1'))
      markup.add(*buttons)
      aa_bot.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
      aa_bot.answer_callback_query(function_call.id)
        
    if (function_call.data == "feedback_yes_q1")|(function_call.data == "feedback_no_q1"):
      log = {'employeer': str(function_call.from_user.full_name)}
      log.update({'question': 'Полученный ответ содержит всю необходимую информацию, чтобы оказать сервисную поддержку?'})
      if function_call.data == "feedback_yes_q1":
        log.update({'answer': 'Да'})
      else:
        log.update({'answer': 'Нет'})
      with open('/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/references/bot_log.csv', 'a+') as f:
        f.write('\n')
        f.write(str(log))

      markup = types.InlineKeyboardMarkup()
      buttons = []
      buttons.append(types.InlineKeyboardButton(text = "Да", callback_data='feedback_yes_q2'))
      buttons.append(types.InlineKeyboardButton(text = 'Нет', callback_data='feedback_no_q2'))
      markup.add(*buttons)
      third_mess = 'Ответ содержит неточности, ложные сведения в содержании?'
      aa_bot.send_message(function_call.message.chat.id, third_mess, reply_markup=markup)
      aa_bot.answer_callback_query(function_call.id)
      
    if (function_call.data == "feedback_yes_q2")|(function_call.data == "feedback_no_q2"):
      log = {'employeer': str(function_call.from_user.full_name)}
      log.update({'question': 'Ответ содержит неточности, ложные сведения в содержании?'})
      if function_call.data == "feedback_yes_q2":
        log.update({'answer': 'Да'})
      else:
        log.update({'answer': 'Нет'})
      with open('/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/references/bot_log.csv', 'a+') as f:
        f.write('\n')
        f.write(str(log))

      markup = types.InlineKeyboardMarkup()
      buttons = []
      buttons.append(types.InlineKeyboardButton(text = "Да", callback_data='feedback_yes_q3'))
      buttons.append(types.InlineKeyboardButton(text = 'Нет', callback_data='feedback_no_q3'))
      markup.add(*buttons)
      fouth_mess = 'Содержат ли фрагменты из базы знаний всю необходимую информацию для оказания сервисной поддержки по данном вопросу?'
      aa_bot.send_message(function_call.message.chat.id, fouth_mess, reply_markup=markup)
      aa_bot.answer_callback_query(function_call.id)
      
    if (function_call.data == "feedback_yes_q3")|(function_call.data == "feedback_no_q3"):
      log = {'employeer': str(function_call.from_user.full_name)}
      log.update({'question': 'Содержат ли фрагменты из базы знаний всю необходимую информацию для оказания сервисной поддержки по данном вопросу?'})
      if function_call.data == "feedback_yes_q3":
        log.update({'answer': 'Да'})
      else:
        log.update({'answer': 'Нет'})
      with open('/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/references/bot_log.csv', 'a+') as f:
        f.write('\n')
        f.write(str(log))

      markup = types.InlineKeyboardMarkup()
      buttons = []
      buttons.append(types.InlineKeyboardButton(text = "Да", callback_data='feedback_yes_q4'))
      buttons.append(types.InlineKeyboardButton(text = 'Нет', callback_data='feedback_no_q4'))
      markup.add(*buttons)
      fifth_mess = 'Cодержат ли фрагменты нерелевантную запросу клиента информацию?'
      aa_bot.send_message(function_call.message.chat.id, fifth_mess, reply_markup=markup)
      aa_bot.answer_callback_query(function_call.id)
      
    if (function_call.data == "feedback_yes_q4")|(function_call.data == "feedback_no_q4"):
      log = {'employeer': str(function_call.from_user.full_name)}
      log.update({'question': 'Cодержат ли фрагменты нерелевантную запросу клиента информацию?'})
      if function_call.data == "feedback_yes_q4":
        log.update({'answer': 'Да'})
      else:
        log.update({'answer': 'Нет'})
      with open('/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/references/bot_log.csv', 'a+') as f:
        f.write('\n')
        f.write(str(log))

      markup = types.InlineKeyboardMarkup()
      buttons = []
      buttons.append(types.InlineKeyboardButton(text = "Да", callback_data='feedback_yes_q5'))
      buttons.append(types.InlineKeyboardButton(text = 'Нет', callback_data='feedback_no_q5'))
      markup.add(*buttons)
      sixth_mess = 'Помог бы ответ от сервиса для полноценной помощи клиенту?'
      aa_bot.send_message(function_call.message.chat.id, sixth_mess, reply_markup=markup)
      aa_bot.answer_callback_query(function_call.id)
      
    if (function_call.data == "feedback_yes_q5")|(function_call.data == "feedback_no_q5"):
      log = {'employeer': str(function_call.from_user.full_name)}
      log.update({'question': 'Помог бы ответ от сервиса для полноценной помощи клиенту?'})
      if function_call.data == "feedback_yes_q5":
        log.update({'answer': 'Да'})
      else:
        log.update({'answer': 'Нет'})
      with open('/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/references/bot_log.csv', 'a+') as f:
        f.write('\n')
        f.write(str(log))

      end_mess = 'Ваши ответы учтены. Спасибо!'
      markup = types.InlineKeyboardMarkup()
      buttons= []
      buttons.append(types.InlineKeyboardButton(text = 'Задать следующий вопрос', callback_data='next'))
      markup.add(*buttons)
      aa_bot.send_message(function_call.message.chat.id, end_mess, reply_markup=markup)
      aa_bot.answer_callback_query(function_call.id)

@aa_bot.message_handler(func=lambda message: True)
def handle_message(message):
  json_data = {"question":message.html_text}
  responce =requests.post(url, json=json_data, headers=headers)
  aa_bot.reply_to(message, responce.text)
  log = {'employeer': str(message.from_user.first_name)+'_'+str(message.from_user.last_name)}
  log.update({'question': message.html_text})
  log.update({'responce': responce.text})
  log.update({'responce_date': responce.headers['date']})
  with open('/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/references/bot_log_ift.csv', 'a+') as f:
    f.write('\n')
    f.write(str(log))

  markup = types.InlineKeyboardMarkup()
  buttons=[]
  buttons.append(types.InlineKeyboardButton("Перейти", url="https://disk.yandex.ru/i/qBEPAFH2uUhkNA"))
  buttons.append(types.InlineKeyboardButton(text = 'Оценить качество генерации', callback_data='feedback'))
  markup.add(*buttons)
  aa_bot.send_message(message.chat.id, "Исходный источник:", reply_markup=markup)
  
  if message.text =='Прошу ответить на ряд вопросов по качестве генерации. Полученный ответ содержит всю необходимую информацию, чтобы оказать сервисную поддержку?':
    buttons=[]
    print(message[-1].message_id)
    buttons.append(types.InlineKeyboardButton(text = "Да", callback_data='feedback_yes'))
    buttons.append(types.InlineKeyboardButton(text = 'Нет', callback_data='feedback_no'))
    markup.add(*buttons)
     


aa_bot.polling()
