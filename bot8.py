import telebot
from telebot import types

# Initialize the bot with your token
bot_token = "7591606213:AAFyz1RC45uiP0JAf_X4y_OVSsi8y__yIJI"
bot = telebot.TeleBot(bot_token)

# Sample menus for each day and meal type
menus = {
    'Monday': {'Breakfast': 'Pancakes', 'Lunch': 'Pasta', 'Snacks': 'Cookies', 'Dinner': 'Pizza'},
    'Tuesday': {'Breakfast': 'Omelette', 'Lunch': 'Burger', 'Snacks': 'Fries', 'Dinner': 'Salad'},
    'Wednesday': {'Breakfast': 'Toast', 'Lunch': 'Biryani', 'Snacks': 'Muffins', 'Dinner': 'Soup'},
    'Thursday': {'Breakfast': 'Smoothie', 'Lunch': 'Pizza', 'Snacks': 'Chips', 'Dinner': 'Steak'},
    'Friday': {'Breakfast': 'Waffles', 'Lunch': 'Sushi', 'Snacks': 'Brownies', 'Dinner': 'Fish'},
    'Saturday': {'Breakfast': 'French Toast', 'Lunch': 'Tacos', 'Snacks': 'Ice Cream', 'Dinner': 'BBQ'},
    'Sunday': {'Breakfast': 'Cereal', 'Lunch': 'Roast Chicken', 'Snacks': 'Fruit Salad', 'Dinner': 'Pasta'}
}

# Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        markup.add(types.KeyboardButton(day))
    bot.send_message(message.chat.id, "Hello! Please choose a day of the week:", reply_markup=markup)

# Handle text responses from buttons
@bot.message_handler(func=lambda message: message.text in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
def ask_meal_type(message):
    day = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    meal_types = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']
    for meal in meal_types:
        markup.add(types.KeyboardButton(meal))
    bot.send_message(message.chat.id, f"You selected {day}. Now, choose a meal type:", reply_markup=markup)

    bot.register_next_step_handler(message, lambda m: show_menu(m, day))

def show_menu(message, day):
    meal_type = message.text
    if meal_type in ['Breakfast', 'Lunch', 'Snacks', 'Dinner']:
        menu = menus[day].get(meal_type, "No menu available")
        bot.send_message(message.chat.id, f"The menu for {meal_type} on {day} is: {menu}")
        offer_assistance(message)
    else:
        bot.send_message(message.chat.id, "Invalid meal type. Please try again.")

def offer_assistance(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Yes"), types.KeyboardButton("No"))
    bot.send_message(message.chat.id, "Do you need further assistance?", reply_markup=markup)
    
    bot.register_next_step_handler(message, handle_assistance)

def handle_assistance(message):
    if message.text == "Yes":
        bot.send_message(message.chat.id, "How can I assist you further?")
    else:
        bot.send_message(message.chat.id, "Thank you! Have a great day!")

# Polling
bot.polling()
