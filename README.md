# ayanami-bot
Your AI-powered assistant that customizes itself to automate your tasks, conveniently in a Telegram bot.


This project brings an AI (private and local or using OpenAI's GPT3/4) to be your personal assistant through a **Telegram bot**. It's capable of run automations in the host's machine using existing or custom-made *LangChain Tools*, also working as a standard chatbot like ChatGPT. And since it uses Telegram as the main interface, it can be used from anywhere, in PCs, phones, etc, as long as there is an internet connection.


Yes, the name is based on the Neon Genesis Evangelion character.


## What can it do?
It's meant to be used as an intuitive assistant to automate simple or repetitive processes even if you are not at home, and since this is a versatile project, it can be configured to meet the user's necessities without compromising privacy, Ayanami runs entirely locally, so, if the AI can access some of your raw data, it never leaves your computer, but be aware that **information can be shown in the Telegram's chat history**.


> [!CAUTION]
> Even if this project never touches your data, it uses LangChain, the Telegram API, and optionally the OpenAI API, so you need to be aware on how they handle your data. **Just be careful with sensitive data you share with it, especially when you send it to someone that is not you.**


Ayanami can use any LangChain Tool (see a list of built-in tools [Here](https://python.langchain.com/docs/integrations/tools/)), each tool is designed to be plugged into the the AI so that it can be used to do something like read a text document or execute a program.

With that, it can:
- Read and write documents
- Code in python and run it afterwards
- Run programs in your system using the shell
- Search stuff on the internet via Google, Reddit, Youtube or even ArXiv
- Tell the weather
- Generate images using DALL-E (be aware that it uses the same OpenAI API key as GPT3 or GPT4, so it uses more credits)

It can do some other cool things too...

And if you have the python skills, you can even write your own tools to do whatever you want. LangChain is well documented and widely used, and the process of creating a tool from scratch is actually pretty simple! (More info in the [LangChain Tools Documentation](https://python.langchain.com/docs/modules/tools/))


> [!WARNING]
> Also, be aware that, very unfortunately, these tools may not work properly with local (Ollama) LLMs, since they are still not stable enough


## Security Recommendations
Be aware that this project is meant to be used inside a **safe environment**, more specifically, inside a **Docker** container. 
If you don't know what Docker is, or don't know how to use it, don't worry, we got your back at the **Getting Started** section in this document to get this project up and running.


Also, any API keys or any secret of any kind should not be inside any piece of code. In this project I use mostly **Environment variables** to store them, so that they cannot leave your machine or session by accident.

## Getting Started

> [!IMPORTANT]
> This project is in its early development stages, so things can and will change, but I'll do my best to never keep this part of the guide outdated. Of course that any help or suggestion is welcome, just use the [Issues tab](https://github.com/JoaoPito/ayanami-bot/issues).


*Sorry, but this part of the guide is empty for now because there is nothing to put here yet. Please come here again in a few days. 🙃*


## Privacy
- [OpenAI API Privacy Policy](https://openai.com/policies/privacy-policy)
- [LangChain Privacy Policy](https://www.langchain.com/privacy-policy)
