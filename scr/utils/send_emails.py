import os.path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import io
from config import PHOTO_SAVE_PATH, TEXT_SAVE_PATH
from utils.check_data import is_valid_email


def photo_file_handler(file_name):
    try:
        with open(file_name, 'rb') as f:
            photo = MIMEImage(f.read())
        return photo
    except Exception as e:
        return f'Ошибка в обработке изображения: {e}'


def text_file_handler(file_name):
    try:
        text = ''
        with io.open(file_name, encoding='utf-8') as file:
            for line in file:
                text += f'{line}\n'
        return MIMEText(text)
    except Exception as e:
        return f'Ошибка в обработке текстового файла: {e}'


class SMail:
    def __init__(self, sending_mail, password, theme, text_name, list_photo_names, list_emails):
        self.sending_mail = sending_mail
        self.__p = password
        self.theme = theme
        self.text_name = text_name
        self.list_photo_names = list_photo_names
        self.list_emails = list_emails

    def send_email(self):
        try:
            err_emails = []
            server = smtplib.SMTP('smtp.yandex.ru', 587)
            server.starttls()
            server.login(self.sending_mail, self.__p)
            for email_receive in self.list_emails:
                if is_valid_email(email_receive):
                    msg = MIMEMultipart()
                    msg['Subject'] = self.theme
                    msg['To'] = email_receive
                    msg['From'] = self.sending_mail
                    text_path = os.path.join(TEXT_SAVE_PATH, self.text_name)
                    msg.text = text_file_handler(text_path)
                    msg.attach(msg.text)
                    for name_photo in self.list_photo_names:
                        photo_path = os.path.join(PHOTO_SAVE_PATH, name_photo)
                        msg.image = photo_file_handler(photo_path)
                        msg.attach(msg.image)
                    server.sendmail(self.sending_mail, email_receive, msg.as_string())
                    print(f"Message sent to email {email_receive}")
                else:
                    err_emails.append(email_receive)
            return err_emails
        except Exception as _ex:
            print(f"Error: {_ex}\n")
