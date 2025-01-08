import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import io


class SMail:
    def __init__(self, is_from, is_to, subject, password):
        self.is_form = is_from
        self.is_to = is_to
        self.subject = subject
        self.__p = password

    def text_file_handler(self, file_name):
        try:
            text = ''
            with io.open(file_name, encoding='utf-8') as file:
                for line in file:
                    text += f'{line}\n'
            return MIMEText(text)
        except Exception as e:
            return f'Ошибка в обработке текстового файла: {e}'

    def photo_file_handler(self, file_name):
        try:
            with open(file_name, 'rb') as f:
                photo = MIMEImage(f.read())
            return photo
        except Exception as e:
            return f'Ошибка в обработке изображения: {e}'

    def send_email(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.is_form, self.__p)
            msg = MIMEMultipart()
            msg['Subject'] = self.subject
            msg['To'] = self.is_to
            msg['From'] = self.is_form
            msg.image = self.photo_file_handler('photo.jpg')
            msg.text = self.text_file_handler('text.txt')
            msg.attach(msg.text)
            msg.attach(msg.image)
            server.sendmail(self.is_form, self.is_to, msg.as_string())
            return f"Message sent to email {self.is_to}"
        except Exception as _ex:
            return f"Error: {_ex}\n"


# def send_emails(emails):
#     for i in range(len(emails)):
#         email = SMail(login, list_emails[i], them, password)
#         print(email.send_email())
