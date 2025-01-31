import tkinter as tk
import requests
import threading
import asyncio

API_TOKEN = '7308529474:AAFt4teR19mrJDAX6a1pdt4Z765cBkQD_hs'
CHAT_ID = '682702052'  # Seu Chat ID

def send_message(text):
    if not text:
        print("Message text is empty. Not sending.")
        return
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text}
    response = requests.post(url, data=data)
    print(f'Send message response: {response.json()}')
    return response.json()

async def get_updates(update_id=None):
    url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'
    params = {'timeout': 100, 'offset': update_id}
    response = requests.get(url, params=params)
    updates = response.json()
    print(f'Get updates response: {updates}')
    return updates

async def poll_updates():
    update_id = None
    while True:
        updates = await get_updates(update_id)
        if 'result' in updates and updates['result']:
            for update in updates['result']:
                update_id = update['update_id'] + 1
                if 'message' in update:
                    message = update['message']
                    if 'text' in message:
                        text = message['text']
                        listbox.insert(tk.END, f"Recebido: {text}")
                    else:
                        listbox.insert(tk.END, f"Recebido: [tipo de mensagem não suportado]")
        await asyncio.sleep(1)

def start_polling():
    asyncio.run(poll_updates())

def send_and_receive():
    message_text = entry.get()
    if not message_text:
        print("No message to send.")
        return

    send_message(message_text)
    listbox.insert(tk.END, f"Enviado: {message_text}")
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Chat com @GPT4Telegrambot")

frame = tk.Frame(root)
scrollbar = tk.Scrollbar(frame)
listbox = tk.Listbox(frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)
frame.pack()

entry = tk.Entry(root, width=50)
entry.pack()

send_button = tk.Button(root, text="Enviar", command=lambda: threading.Thread(target=send_and_receive).start())
send_button.pack()

threading.Thread(target=start_polling).start()

root.mainloop()
