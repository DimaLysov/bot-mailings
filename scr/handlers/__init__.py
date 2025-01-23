from .start_hd import start_router
from .empty_hd import empty_router
from handlers.Email_hd.get_email_hd import get_email_router
from handlers.Email_hd.select_email_hd import select_email_router
from handlers.Email_hd.set_email_hd import add_email_router
from handlers.Sample_hd.edit_sample_info import edit_sample_router
from handlers.Sample_hd.get_sample_hd import get_sample_router
from handlers.Sample_hd.set_sample_hd import add_sample_router
from handlers.Sample_hd.select_sample_hd import select_sample_router
from handlers.Sender_hd.send_email_hd import send_email_router
from handlers.Email_hd.edit_email_info_hd import edit_router
from .help_hd import help_router

routers = [start_router,
           empty_router,
           get_email_router,
           select_email_router,
           add_email_router,
           edit_sample_router,
           get_sample_router,
           add_sample_router,
           select_sample_router,
           send_email_router,
           edit_router,
           help_router]
