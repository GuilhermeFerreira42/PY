from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configurar o token da API do Telegram
API_TOKEN = '7308529474:AAFt4teR19mrJDAX6a1pdt4Z765cBkQD_hs'

# Função para enviar mensagens
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Olá, sou o seu bot! Como posso ajudar?')

# Função para lidar com mensagens recebidas
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

# Configurar a aplicação
application = Application.builder().token(API_TOKEN).build()

# Adicionar handlers para comandos e mensagens
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Iniciar o bot
application.run_polling()
