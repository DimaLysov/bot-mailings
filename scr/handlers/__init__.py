from .get_email_hd import get_email_router
from .get_sample_hd import get_sample_router
from .select_email_hd import select_email_router
from .set_email_hd import add_email_router
from .set_sample_hd import add_sample_router
from .help_hd import help_router
from .start_hd import start_router

routers = [get_email_router,
           get_sample_router,
           select_email_router,
           add_email_router,
           add_sample_router,
           help_router,
           start_router]
