# from backend.config.settings import settings

# print(settings.APP_NAME)
# print(settings.MODEL_NAME)
# print(settings.DEBUG)


# from backend.config.logger import logger

# logger.info("Jarvis started successfully.")

# logger.warning("This is a warning.")

# logger.error("This is an error.")


# from backend.ai.prompts import SYSTEM_PROMPT

# print(SYSTEM_PROMPT)



# from backend.ai.llm import llm

# while True:

#     user = input("You : ")

#     if user.lower() == "exit":
#         break

#     response = llm.generate_response(user)

#     print(f"\nJarvis : {response}\n")


# from backend.ai.conversation import conversation

# conversation.add_user_message("Hello")

# conversation.add_assistant_message("Hi Dev!")

# conversation.add_user_message("How are you?")

# print(conversation.get_history())


# from backend.core.assistant import assistant

# while True:

#     user = input("You : ")

#     if user.lower() == "exit":
#         break

#     response = assistant.process_message(user)

#     print(f"\nJarvis : {response}\n")\


from backend.core.router import router

while True:

    message = input("You : ")

    if message == "exit":
        break

    tool = router.route(message)

    print(f"\nSelected Tool : {tool}\n")