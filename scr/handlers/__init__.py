from handlers.Sample_hd.get_sample_hd import get_sample_router
from handlers.Sample_hd.set_sample_hd import add_sample_router
from handlers.Sample_hd.select_sample_hd import select_sample_router
from .get_email_hd import get_email_router
from .select_email_hd import select_email_router
from .set_email_hd import add_email_router
from .help_hd import help_router
from .start_hd import start_router

routers = [get_sample_router,
           add_sample_router,
           select_sample_router,
           get_email_router,
           select_email_router,
           add_email_router,
           help_router,
           start_router]
