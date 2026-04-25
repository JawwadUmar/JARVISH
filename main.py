import asyncio
from app.llm import init_llm
from app.utils.file_loader import get_resume, get_prompt
from app.bot.bot_runner import run_bot


async def main():
    llm = init_llm()
    resume = get_resume()
    prompt = get_prompt()

    if llm == None:
        print("❌ JARVIS: AI Initialization Failed.")
        return
    
    if resume == None:
        print("❌ JARVIS: Resume Not Found.")
        return
    
    if prompt == None:
        print("❌ JARVIS: Prompt Not Found.")
        return

    await run_bot(llm, resume, prompt)


if __name__ == "__main__":
    asyncio.run(main())