import asyncio
import random
from playwright.async_api import Page

from app.utils.human import human_delay, human_typing, human_mouse_move
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


def should_include_resume(question):
    keywords = ["experience", "skill", "project", "technology", "linkedin", "github", "portfolio", "email", "phone", "contact"]
    return any(k in question.lower() for k in keywords)

async def handle_questionnaire(page: Page, llm: ChatGroq, resume:str, system_prompt:str, human_prompt:str):
    if not llm:
        return

    try:
        chat_container = page.locator('.chatbot_MessageContainer')
        await chat_container.wait_for(state='visible', timeout=8000)
        print("🚨 JARVIS: Questionnaire detected! Analyzing...")

        while True:
            if not await chat_container.is_visible():
                print("✅ JARVIS: Questionnaire Closed.")
                break

            await asyncio.sleep(random.uniform(2.0, 3.5))

            #Scrape the latest Naukri bot message
            naukri_bot_messages = page.locator('.botItem .botMsg span')
            count = await naukri_bot_messages.count()
            if count == 0:
                continue

            question = await naukri_bot_messages.nth(count - 1).inner_text()

            input_box = page.locator('.textArea[contenteditable="true"]')
            is_text = await input_box.is_visible()

            available_options = []
            if not is_text:
                # Targeted search inside the chat container for all button types
                options_locator = chat_container.locator('.ssrc__label, .ssrc__radio, label, button, .chip, [role="button"]')
                for i in range(await options_locator.count()):
                    txt = await options_locator.nth(i).inner_text() or await options_locator.nth(i).get_attribute("value")
                    if txt and 0 < len(txt.strip()) < 50:
                        available_options.append(txt.strip())
                available_options = list(dict.fromkeys(available_options))[-10:]
                if available_options: print(f"🔘 Options detected: {available_options}")

            # AI REASONING    
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])
            
            prompt = prompt_template.format_messages(
                resume=resume if should_include_resume(question) else "N/A",
                options=available_options,
                question=question
            )
            
            print("🧠 JARVIS: Thinking...")
            raw_response = await llm.ainvoke(prompt)
            answer = raw_response.content.strip().replace("**", "")
            print(f"✅ JARVIS Answer: {answer}")

            if is_text:
                await input_box.click()
                await page.keyboard.press('Control+A')
                await page.keyboard.press('Backspace')
                await human_typing(page.keyboard, answer)
                await human_delay(1, 2)
            elif available_options:
                matched = next((opt for opt in available_options if opt.lower() in answer.lower()), None)
                if matched:
                    target = chat_container.get_by_text(matched, exact=True).last
                    await human_mouse_move(page)
                    await target.click(force=True)
                    # Force check hidden radio button to enable 'Save'
                    radio_id = await target.get_attribute("for")
                    if radio_id:
                        try: await page.locator(f"#{radio_id}").check(force=True)
                        except: pass
                else:
                    await chat_container.get_by_text(answer).last.click(force=True)
                
            await human_delay(1, 2)

            # SUBMIT
            save_btn = page.locator('.send:not(.disabled) .sendMsg')
            if await save_btn.is_visible():
                await save_btn.click()
                print("👆 JARVIS: Clicked Save.")
                await human_delay(2, 4)
            else:
                await page.keyboard.press('Enter')

    except Exception as e:
        print(f"🤖 JARVIS Error in questionnaire: {repr(e)}")