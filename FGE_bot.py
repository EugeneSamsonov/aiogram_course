import telebot
import config
import speech_recognition as SRG
from pydub import AudioSegment

language='ru_RU'
bot = telebot.TeleBot(config.TOKEN)
r = SRG.Recognizer()

def recognise(filename):
    with SRG.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            return text
        except:
            return "Ошибка, попробуйте снова"

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    src = f"voice/{message.from_user.id}.ogg"
    dst = f"voice/{message.from_user.id}_result.wav"

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    sound = AudioSegment.from_ogg(src)
    sound.export(dst, format="wav")

    text = recognise(dst)
    bot.reply_to(message, text)

bot.polling()