from backend.core.router import router
from backend.core.executor import executor
from backend.tools.memory import memory_tool

# Register tool
executor.register_tool("memory", memory_tool)

while True:
    user = input("You: ")

    if user == "exit":
        break

    tool = router.route(user)

    print(f"Router -> {tool}")

    if tool == "memory":
        response = executor.execute(tool, user)
        print(f"Jarvis -> {response}")