import telebot
import tkinter

___version___ = "1.0"
___name___ = "Reimagined Bot"
root= tkinter.Tk()
name= tkinter.Label(root,text="aribosdikek")
name.pack()
root.mainloop()

bot = telebot.TeleBot("1440525329:AAFXSLKOADNCpLsL5KpAKTCrBcqAvOYAMkY")


@bot.message_handler(regexp="\\+1([^\\w]|$)")
def plus_one(message):
    if message.chat.type == "group":
        text_to_send = f"Message ID: {message.id}\nOriginal Message ID: {message.reply_to_message.id}"
        bot.reply_to(message, text_to_send)


def main():
    print(f"{___name___} Started, version {___version___}")
    print(f"Bot username: @{bot.get_me().username}")
    bot.polling()


if __name__ == "__main__":
    main()