import asyncio
from app.ai.llm import init_llm
from app.utils.file_loader import get_resume, get_system_prompt, get_human_prompt
from app.bot.bot_runner import run_bot


async def main():
    llm = init_llm()
    resume = get_resume()
    system_prompt = get_system_prompt()
    human_prompt = get_human_prompt()

    if llm == None:
        print("❌ JARVIS: AI Initialization Failed.")
        return
    
    if resume == None:
        print("❌ JARVIS: Resume Not Found.")
        return
    
    if system_prompt == None or human_prompt == None:
        print("❌ JARVIS: Prompts Not Found.")
        return

    await run_bot(llm, resume, system_prompt, human_prompt)


if __name__ == "__main__":
    asyncio.run(main())