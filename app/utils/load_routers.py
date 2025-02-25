import logging
import os
import importlib
import glob
from aiogram import Router


def load_routers():
    router = Router()
    handlers_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'bot')
    logging.info("Loading routers...")

    handler_files = glob.glob(os.path.join(handlers_dir, "**", "handlers.py"), recursive=True)

    if not handler_files:
        logging.warning("No routers found.")
        return router

    for handler_path in handler_files:
        relative_path = os.path.relpath(handler_path, handlers_dir)
        module_name = f"app.bot.{relative_path.replace(os.sep, '.')[:-3]}"  # Убираем __init__.py

        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                logging.info(f"Loading router: {module_name}")
                router.include_router(module.router)
            else:
                logging.warning(f"No 'router' found in {module_name}")
        except Exception as e:
            logging.error(f"Failed to load {module_name}: {e}")

    logging.info("Routers loaded.")
    return router
