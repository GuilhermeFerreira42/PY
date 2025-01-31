import requests
import time

API_TOKEN = '7308529474:AAFt4teR19mrJDAX6a1pdt4Z765cBkQD_hs'

def get_updates():
    url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'
    response = requests.get(url)
    updates = response.json()
    print(updates)
    return updates

# Adicione uma pausa de 10 segundos antes de buscar atualizações
time.sleep(10)

updates = get_updates()

for update in updates['result']:
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        print(f"Chat ID: {chat_id}")
