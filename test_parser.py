from backend.ai.parser import parser
from backend.core.executor import executor
from backend.tools.memory import memory_tool

executor.register_tool(
    "memory",
    memory_tool
)

while True:

    user = input("You: ")

    task = parser.parse(user)

    print("\nTask ->")
    print(task)

    print("\nResponse ->")
    print(executor.execute(task))