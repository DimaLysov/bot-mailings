from db.requests.Samples.get_selected_sample_db import get_selected_sample
from db.requests.Users_Emails.get_selected_email_db import get_selected_email
from db.requests.Users_Emails.get_selected_password import get_selected_password
from utils.send_emails import SMail


async def create_info(chat_id, emails) -> SMail:
    sending_mail = await get_selected_email(chat_id)
    password = await get_selected_password(chat_id)
    sample = await get_selected_sample(chat_id)
    info = SMail(sending_mail=sending_mail,
                 password=password,
                 theme=sample.theme,
                 text_name=sample.text_name,
                 name_photo=sample.photo_name,
                 list_emails=emails)
    return info

