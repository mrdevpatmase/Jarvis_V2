# In this file we define the intents for Jarvis V2

import csv

# Dataset: 30 commands per intent
dataset = {
    "get_time": [
        "What time is it?", "Can you tell me the time?", "Current time please",
        "Tell me the time", "What’s the current hour?", "Time now",
        "Could you give me the time?", "Do you know the time?", "Time check",
        "Show me the current time", "I want to know the time", "Give me the time now",
        "Tell me the exact time", "Please check the time", "Read the current time",
        "Show me what time it is", "Clock time please", "Tell me the present time",
        "What does the clock say?", "I need the time right now",
        "Can you display the time?", "Tell me the hour", "Show clock details",
        "Jarvis, what's the time?", "Report current time", "Check clock for me",
        "Give me today’s time", "How late is it now?", "What’s the time currently?",
        "Tell me the updated time"
    ],
    "search_google": [
        "Search Google for Python tutorials", "Look up machine learning", "Find AI articles on Google",
        "Google best restaurants near me", "Search Google for Jarvis projects", "Find information about space on Google",
        "Look up weather today", "Google trending news", "Search for stock prices on Google",
        "Find nearby cafes", "Google news about technology", "Search Google for recipes",
        "Find images on Google", "Search Google for sports updates", "Look up programming blogs",
        "Google latest movies", "Search Google for maps", "Find nearby hospitals on Google",
        "Google the meaning of AI", "Look up coding resources",
        "Search Google about AI research", "Google the weather forecast", "Look up news headlines on Google",
        "Find tutorials on Google", "Check Google for nearby gyms", "Search Google for travel guides",
        "Google funny memes", "Look up sports results on Google", "Search Google for famous quotes",
        "Find trending topics on Google"
    ],
    "search_youtube": [
        "Play music on YouTube", "Search YouTube for cat videos", "Find Python tutorials on YouTube",
        "Play cooking videos on YouTube", "Search YouTube for gaming videos", "Look up JavaScript tutorials on YouTube",
        "Play trending videos on YouTube", "Find motivational speeches on YouTube", "Search YouTube for workout videos",
        "Play piano tutorials on YouTube", "Look up movie trailers on YouTube", "Search YouTube for meditation videos",
        "Show YouTube comedy clips", "Find news channels on YouTube", "Search for educational videos on YouTube",
        "Play YouTube shorts", "Find football highlights on YouTube", "Show me YouTube podcasts",
        "Look for travel vlogs on YouTube", "Search YouTube for interview videos",
        "Play relaxing music on YouTube", "Search YouTube for coding lectures", "Look up stand-up comedy on YouTube",
        "Search YouTube for history documentaries", "Play live streams on YouTube", "Find yoga classes on YouTube",
        "Search YouTube for news live", "Play science experiments on YouTube", "Look up fashion vlogs on YouTube",
        "Find YouTube gaming streams"
    ],
    "open_notepad": [
        "Open Notepad", "Start Notepad", "Launch Notepad",
        "Open a new Notepad file", "I want to write something in Notepad", "Notepad please",
        "Can you open Notepad?", "Launch the Notepad app", "Start a Notepad session",
        "Open Notepad editor", "Notepad text editor", "Open Notepad program",
        "Create a Notepad document", "Open blank Notepad", "Start writing in Notepad",
        "New Notepad window", "Run Notepad", "Open Notepad software",
        "Activate Notepad", "Notepad application open",
        "Open Windows Notepad", "Create text file in Notepad", "Start new note",
        "Open Notepad immediately", "Write something in Notepad", "Jarvis, launch Notepad",
        "Open Notepad and type", "Open Notepad document", "Start a new Notepad window",
        "Notepad launch now"
    ],
    "open_calculator": [
        "Open Calculator", "Launch Calculator", "Start Calculator",
        "I want to use Calculator", "Calculator please", "Can you open Calculator?",
        "Open the Calculator app", "Start a new Calculator session", "Calculator program",
        "Launch the Calculator tool", "Open my Calculator", "Use Calculator",
        "Bring up Calculator", "Open Calculator window", "Run Calculator",
        "Calculator software please", "I need a Calculator", "Activate Calculator",
        "Calculator tool open", "Start calculation app",
        "Open Windows Calculator", "Launch math calculator", "Start basic calculator",
        "Jarvis open calculator", "Bring up my calculator", "Calculator now",
        "Open calculator application", "Start new calculation", "Show calculator",
        "Open calculator immediately"
    ],
    "open_whatsapp": [
        "Open WhatsApp", "Launch WhatsApp", "Start WhatsApp",
        "I want to check WhatsApp", "Open WhatsApp messenger", "WhatsApp please",
        "Can you open WhatsApp?", "Start the WhatsApp app", "Launch WhatsApp program",
        "Open my WhatsApp", "Open WhatsApp chat", "Start WhatsApp messenger",
        "Open WhatsApp window", "Run WhatsApp", "Check WhatsApp messages",
        "Activate WhatsApp", "WhatsApp application open", "Bring up WhatsApp",
        "Start WhatsApp session", "Access WhatsApp",
        "Open WhatsApp right now", "Check my WhatsApp", "Jarvis open WhatsApp",
        "Launch WhatsApp chat window", "WhatsApp start now", "WhatsApp launch please",
        "Open WhatsApp quickly", "Open WhatsApp conversations", "Start WhatsApp instantly",
        "Access my WhatsApp messages"
    ],
    "open_linkedin": [
        "Open LinkedIn", "Launch LinkedIn", "Start LinkedIn",
        "I want to check LinkedIn", "Open LinkedIn website", "LinkedIn please",
        "Can you open LinkedIn?", "Start the LinkedIn app", "Open my LinkedIn profile",
        "Launch LinkedIn program", "Check LinkedIn updates", "Open LinkedIn page",
        "Access LinkedIn site", "Open LinkedIn portal", "Show LinkedIn profile",
        "Open LinkedIn network", "Go to LinkedIn", "Open LinkedIn account",
        "Bring up LinkedIn", "Run LinkedIn application",
        "Open my LinkedIn dashboard", "Check LinkedIn notifications", "Start LinkedIn now",
        "Jarvis open LinkedIn", "Launch LinkedIn instantly", "LinkedIn start now",
        "Open LinkedIn homepage", "Access my LinkedIn feed", "Check LinkedIn right away",
        "Go to LinkedIn profile"
    ],
    "open_github": [
        "Open GitHub", "Launch GitHub", "Start GitHub",
        "I want to check GitHub", "Open GitHub repository", "GitHub please",
        "Can you open GitHub?", "Start the GitHub app", "Open my GitHub profile",
        "Launch GitHub program", "Check GitHub updates", "Open GitHub page",
        "Access GitHub website", "Open GitHub account", "Show GitHub repositories",
        "Run GitHub", "GitHub application open", "Check my GitHub projects",
        "Go to GitHub site", "Open GitHub dashboard",
        "Open my GitHub repos", "Jarvis open GitHub", "Launch GitHub quickly",
        "Open GitHub code", "Access my repositories", "GitHub now",
        "Check GitHub issues", "Show GitHub pull requests", "Go to my GitHub profile",
        "Start GitHub website"
    ],
    "open_spotify": [
        "Open Spotify", "Launch Spotify", "Start Spotify",
        "I want to listen on Spotify", "Play music on Spotify", "Spotify please",
        "Can you open Spotify?", "Start the Spotify app", "Open my Spotify playlists",
        "Launch Spotify program", "Play songs on Spotify", "Open Spotify music",
        "Run Spotify", "Spotify application open", "Bring up Spotify",
        "Open Spotify window", "Play Spotify album", "Activate Spotify",
        "Spotify software open", "Start Spotify session",
        "Jarvis open Spotify", "Launch Spotify right now", "Spotify launch please",
        "Play Spotify podcast", "Open Spotify quickly", "Start Spotify instantly",
        "Play Spotify playlist", "Bring up Spotify app", "Spotify now",
        "Open Spotify immediately"
    ],
    "exit": [
        "Exit", "Quit", "Stop", "Close Jarvis", "Terminate Jarvis", "Shutdown Jarvis",
        "Stop listening", "End program", "Turn off Jarvis", "Stop the assistant",
        "Shut down assistant", "Please exit", "Quit now", "I am done", "Goodbye Jarvis",
        "Exit program", "Close assistant", "Turn off", "End Jarvis", "Stop Jarvis",
        "Exit immediately", "Quit the program", "Jarvis shut down", "Close application",
        "Turn off now", "End this session", "Stop Jarvis instantly", "Exit assistant now",
        "Terminate now", "Goodbye assistant"
    ]
}

# Write CSV
with open("jarvis_intents.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["command", "intent"])
    for intent, commands in dataset.items():
        for cmd in commands:
            writer.writerow([cmd, intent])

print("CSV 'jarvis_intents.csv' created with", sum(len(v) for v in dataset.values()), "commands.")
