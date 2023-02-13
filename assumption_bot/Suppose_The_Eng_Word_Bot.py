import random

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text, Command


# Вместо PUT_THE_BOT_TOKEN_HERE нужно вставить токен вашего бота 
BOT_TOKEN: str = 'PUT_THE_BOT_TOKEN_HERE'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 4

# Словарь, в котором будут храниться данные пользователя
user: dict = {'in_game': False,
              'secret_word': '',
              'attempts': None,
              'total_games': 0,
              'wins': 0}

# Функция, возвращающая случайное целое число от 0 до 1999
#Требуется для подбора носера слова в словаре
def get_random_number() -> int:
    return random.randint(0, 1999)
# Функция, возвращающее случайное слово из словаря
def get_random_word() -> str:
    with open('Dictionary.txt', 'r', encoding='utf8') as f:
        num: int = get_random_number()
        count: int = 0
        while count != num:
            f.readline()
            count +=1
        word = f.readline()
        print(word.split()[1])
        return word
# Хэндлер на команду "/start"
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай перевод"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')


# Хэндлер на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю английское слово, '
                         f'а вам нужно назвать его перевод\nУ вас есть {ATTEMPTS} '
                         f'попытки\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')


# Хэндлер на команду "/stat"
@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {user["total_games"]}\n'
                         f'Игр выиграно: {user["wins"]}\n'
                         f'Процент побед: {user["wins"]/user["total_games"]}')


# Хэндлер на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if user['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        user['in_game'] = False
    else:
        await message.answer('А мы и так с вами не играем. '
                             'Может, сыграем разок?')


# Хэндлер на согласие пользователя сыграть в игру
@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть'], ignore_case=True))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        user['secret_word'] = get_random_word()
        word_for_print = ''
        for i in range(0, len(user['secret_word'].split())):
            word_as_list = user['secret_word'].split()[i]
            for j in range(0, len(user['secret_word'].split()[i])):
                if ord(word_as_list[j]) < 1000 and ord(word_as_list[j]) != 40 and ord(word_as_list[j]) != 41:
                    flag = True
                    word_for_print += str(user['secret_word'].split()[i]) + ' '
                    break
                else:
                    flag = False
                    break
        await message.answer(f'Ура!\n\nЯ загадал английское слово: {word_for_print}, '
                             f'попробуй угадать перевод!\n'
                             f'Ответ пиши без дополнительных знаков, с маленькой буквы!')
        user['in_game'] = True
        user['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на русские слова'
                             'и команды /cancel и /stat')


# Хэндлер на отказ пользователя сыграть в игру
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, перевод слов')


# Хэндлер на отправку пользователем ответа (слова)
@dp.message()
async def process_text_answer(message: Message):
    if user['in_game']:
        possible_trans = ''
        flag = 0
        for i in range(0, len(user['secret_word'].split())):
            word_as_list = user['secret_word'].split()[i]
            for j in range(0, len(user['secret_word'].split()[i])):
                if ord(word_as_list[j]) >= 1000 or ord(word_as_list[j]) == 40 or ord(word_as_list[j]) == 41:
                    flag = True
                    possible_trans += str(user['secret_word'].split()[i]) + ' '
                    break
                else:
                    flag = False
                    break
        print(possible_trans)
        for i in range(0,len(possible_trans.split())):
            if str(message.text) == possible_trans.split()[i]:
                print(str(message.text))
                await message.answer('Ура!!! Вы верно назвали перевод!\n\n'
                                 'Может, сыграем еще?')
                user['in_game'] = False
                user['total_games'] += 1
                user['wins'] += 1
                flag = 0
                break
            else:
                flag = 1

        if flag == 1:
            await message.answer('So sad, your option is incorrect( Try again!')
            user['attempts'] -= 1
        if user['attempts'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nПеревод слова '
                                 f'был - {user["secret_word"]}\n\nДавайте '
                                 f'сыграем еще?')
            user['in_game'] = False
            user['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')

if __name__ == '__main__':
    dp.run_polling(bot)
