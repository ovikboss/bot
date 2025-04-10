class Text:

    enter_name_ru: str
    enter_name_eu: str

    def not_twins(self, language):
        if str(language) == "Language.RUSSIAN":
            return """К сожалению, близнец пока не найден 😔

Мы активно ищем вашего близнеца, поэтому обязательно проверяйте бота раз в неделю ☺️👍

Будем благодарны, если вы расскажете о боте друзьям,
так быстрее наполнится база и близнецы будут находиться с первого раза 🙏😍
"""
        else:
            return """Unfortunately, the twin has not been found yet 😔

We are actively looking for your twin, check the bot once a week ☺️👍 

And we will be grateful if you tell your friends about it, so the database will fill up faster and twins will be found the first time 🙏😍"""

    def enter_date(self,language):
        if str(language) == "Language.RUSSIAN":
            return "Введите дату рождения в формате ДД-ММ-ГГГГ (например: 11-05-1990)"
        else:
            return "Please enter your date of birth in the format DD-MM-YYYY (for example 11-05-1990)"

    def enter_name(self,language):
        if str(language) == "Language.RUSSIAN":
            return "☺️ Приветствую! 🙏 Давайте найдём вашего астро-близнеца! Напишите, пожалуйста, ваше имя"
        else:
            return "Hello! Let's find your astro-twin! Please, write your name"

    def name_entered(self,language):
        if str(language) == "Language.RUSSIAN":
            return "Данные успешно сохранены! Нажмите кнопку, чтобы найти близнеца:"
        else:
            return "Data saved successfully! Click the button to find your twin:"

    def find_twin(self, language):
        if str(language) == "Language.RUSSIAN":
            return "Найти близнеца"
        else:
            return "Find twins"

    def find_twin_error(self,language):
        if str(language) == "Language.RUSSIAN":
            return "Произошла ошибка при поиске близнецов"
        else:
            return "An error occurred while searching for twins"

    def twin_find(self, language):
        if str(language) == "Language.RUSSIAN":
            return "Найден близнец"
        else:
            return "A twin has been found"

    def send_button(self, language):
        if str(language) == "Language.RUSSIAN":
            return "Нажмите кнопку, что бы написать"
        else:
            return "Click the button to write"

    def send_twin(self, language):
        if str(language) == "Language.RUSSIAN":
            return "Написать близнецу"
        else:
            return "Write to twin"

    def message_success(self, language):
        if str(language) == "Language.RUSSIAN":
            return "Сообщение отправлено!"
        else:
            return "Message is sent!"

    def send_message(self, language):
        if str(language) == "Language.RUSSIAN":
            return "Введите ваше сообщение:"
        else:
            return "Type in your message for the twin:"

    def send_error(self, language):
        if str(language) == "Language.RUSSIAN":
            return "Неверный формат telegram_id. Введите число.:"
        else:
            return "Incorrect telegram_id format. Enter a number."

    def send_error_2(self, language):
        if str(language) == "Language.RUSSIAN":
            return "Произошла ошибка при получении telegram_id."
        else:
            return "An error occurred while receiving the telegram_id."

    def set_id(self, language):
        if str(language) == "Language.RUSSIAN":
            return "Введите telegram_id пользователя, которому хотите отправить сообщение:"
        else:
            return "Enter the telegram_id of the user you want to send the message to:"

text = Text()