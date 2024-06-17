<div align="center">
  <img src="https://github.com/JoaoPito/ayanami-bot/assets/54748506/04b38435-af3a-46a5-9010-b2a32c92968b" alt="ayanami-bot :)" width="452" height="400"/>
  <h1>ayanami-bot</h1> 
  <h4>Your AI-powered assistant made to be adapted to your unique needs, always accesible, built to increment your day.</h4>
</div>


This project brings AI (private and local or using OpenAI's GPT3/4/4-omni) to be your personal assistant through a **Telegram bot**. It's capable of running automations in the user's machine using existing or custom-made **Tools**, it can read and write files, interpret images, run programs and chat like ChatGPT. And since it uses Telegram as the main interface, it can be used from anywhere, in PCs, phones, etc, as long as there is an internet connection.


Yes, the name is based on the Neon Genesis Evangelion character.


## What can it do?
It's meant to be used as an intuitive assistant to automate simple or repetitive processes even if you are not at home, and since this is a versatile project, it can be configured to meet the user's necessities without compromising privacy, Ayanami can be set to run entirely locally, so, if the AI can access some of your raw data, it never leaves your computer, but be aware that **information can be shown in the Telegram's chat history**.


> [!CAUTION]
> Even if this project never touches your data, it uses LangChain, the Telegram API, and optionally the OpenAI API, so you need to be aware on how they handle your data. **Just be careful with sensitive data you share with it, especially when you send it to someone that is not you.**


Ayanami can use any LangChain Tool (see a list of built-in tools [Here](https://python.langchain.com/docs/integrations/tools/)), each tool is designed to be plugged into the the AI so that it can be used to do something like read a text document or execute a program.

With that, it can:
- Read and write documents
- Code in python and run it afterwards
- Run programs in your system using the shell
- Search stuff on the internet via Google, Reddit, Youtube or even ArXiv
- Tell the weather
- Generate images using DALL-E (be aware that it uses the same OpenAI API key as GPT3 or GPT4, so it needs credits on their platform)

It can do some other cool things too...

And if you have the python skills, you can even write your own tools to do whatever you want. LangChain is well documented and widely used, and the process of creating a tool from scratch is actually pretty simple! (More info in the [LangChain Tools Documentation](https://python.langchain.com/docs/modules/tools/))


> [!WARNING]
> Also, be aware that, very unfortunately, these tools may not work properly with some local (Ollama) LLMs, since small models tend to not perform as good as big ones.

## Project Roadmap
This project is divided into 3 development stages, **1st, 2nd and 3rd impacts**. 

The 1st impact is the minimum viable product, things that I will implement. 
2nd impact is the increment stage, things that I will very likely implement at some point. 
On the 3rd impact the project will be considered finalized, so probably I will NOT work too much on it.

On this list, I will implement things in order, but this order can change.

- **1st Impact:**
  - [x] Text-only AI chat
  - [ ] Multimodal (text and image) chat
  - [ ] Chat integrated RAG (.txt, PDFs, Markdown, Microsoft Word, locally stored files and directories)
  - [ ] Tool Calling

- **2nd Impact:**
  - [ ] Multiple AI profiles (a bit like [Fabric](https://github.com/danielmiessler/fabric))

- **3rd Impact:**
  - [ ] AI providers other than Ollama and OpenAI
  - [ ] Chat interfaces other than Telegram

## Getting Started

> [!IMPORTANT]
> This project is in its early development stages, so things can and will change, but I'll do my best to never keep this part of the guide outdated. Of course that any help or suggestion is welcome, just use the [Issues tab](https://github.com/JoaoPito/ayanami-bot/issues).

### Creating your Telegram bot

Ayanami is built to be used with a Telegram bot.

You'll need to contact [BotFather](https://t.me/botfather) to get your bot Token. BotFather is a Telegram bot that creates Telegram bots, it was created by Telegram people.

Save your bot token for later, you'll need it later.

### Python

TO run Ayanami **you need python installed on your computer** and accessible on your terminal (on your PATH).

After that, you can follow this steps in yout terminal window:
1. Go to the Ayanami-bot directory you downloaded (cd path/into/ayanami)
2. Run the command `pip install -U virtualenv`
3. Create a python virtual environment by issuing the command `python -m venv .venv`
4. Enter the virtual environment (Linux/Mac: `source .venv/bin/activate`, Windows: `venv\Scripts\activate.bat`)
5. Install the dependencies for Ayanami with `pip install -r requirements.txt`


### API Keys

Here we will be saving the credentials so that Ayanami can access resources like **your Telegram Bot**, **OpenAI models** (if you are using it) or any resource that a tool may use (the docs for the tool are going to tell which keys you'll need).

> [!CAUTION]
> **API Keys are private!** You should not share them with anyone and they should never leave your machine. Unless you know what you are doing.

In this project we will be saving API Keys in a **.env** file, located in the root of the project:
1. Go to the Ayanami-bot directory you downloaded (cd path/into/ayanami)
2. Create a new **.env** file (it does not have an extension like ".txt")
3. Save the keys you'll need in the format "NAME=VALUE" or "NAME='VALUE'", each key on its own line. There is one key you'll absolutely need so that Ayanami can use your Telegram bot, this key needs to have the name **TELEGRAM_BOT_TOKEN**.

Example .venv:
```
TELEGRAM_BOT_TOKEN="aejrgioaergioaergioIASUFDIAHSDFHjasfkaj"
OPENAI_API_KEY="fheifhOHFjahdsfjkHKJFHKJHfjshf"
OPENWEATHERMAP_API_KEY="..."
SERPAPI_API_KEY="..."
```

Ayanami will automatically load every API key when it starts up.

## Customizing Ayanami
In the root folder, there is a file named **config.py**, with this file you can parameters to create your own assistant.

This file comes pre-fabricated, you can change everything in there but **you cannot remove most stuff**, doing so will probably crash Ayanami (for now). Most of the things you can change there are commented to be self-explanatory, but I'll go through some of the most important here:
1. **default_ai_params:** Here will be defined the default AI parameters when you run Ayanami. things like:
   - **ai_provider:** Where does your LLM come from, like OpenAI or Ollama (only OpenAI for now, sorry... )
   - **ai_model:** The default LLM model that you want to use (gpt-3.5-turbo, gpt-4o, ...)
   - **system:** The system prompt. You can write, using english, things like how do you want your AI to behave, give it personality. 
2. **tools & toolkits:** The tools that Ayanami can use. They can be anywhere in the project directory, but by default they are inside the _tools_ folder.

Try experimenting with the various parameters in the config file and see what happens!

## Running Ayanami
If all the steps above went well, you are ready to run Ayanami! Just run the **main.py** file with the command `python main.py` and you are good to start chatting with your AI!

## Privacy
- [OpenAI API Privacy Policy](https://openai.com/policies/privacy-policy)
- [LangChain Privacy Policy](https://www.langchain.com/privacy-policy)
