import requests
import time

api_url = 'https://api.telegram.org/bot'
api_cats_url = 'https://aws.random.cat/meow'
bot_token = '5766895641:AAEIO8KcbbNU-jpOsHcjduDN3k04IzBZn1I'
text: str = 'Новый апдейт!'
error_text: str = 'Что-то пошло не так, и котов сегодня не будет'

offset: int = -2
chat_id: int
counter: int = 0

cat_response: requests.Response
cat_link: str

while True:
    print('attempt: ', counter + 1)

    updates = requests.get(f'{api_url}{bot_token}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(api_cats_url)
            requests.get(f'{api_url}{bot_token}/sendMessage?chat_id={chat_id}&text={text}')

            if cat_response.status_code == 200:
                cat_link = cat_response.json()['file']
                requests.get(f'{api_url}{bot_token}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{api_url}{bot_token}/sendMessage?chat_id={chat_id}&text={error_text}')

    time.sleep(1)
    counter += 1
