# from backend.config.settings import settings

# print(settings.APP_NAME)
# print(settings.MODEL_NAME)
# print(settings.DEBUG)


from backend.config.logger import logger

logger.info("Jarvis started successfully.")

logger.warning("This is a warning.")

logger.error("This is an error.")