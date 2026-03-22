import asyncio
import os
import random
import re
from dotenv import load_dotenv
from playwright.async_api import async_playwright, Page

# Import LangChain components
from langchain_groq import ChatGroq
try:
    from langchain_core.globals import set_llm_cache
except ImportError:
    from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

# Load environment variables
load_dotenv()

# --- 1. SECURE CREDENTIALS ---
EMAIL = os.getenv("NAUKRI_EMAIL") 
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    raise ValueError("⚠️ Credentials missing! Check your .env file.")

# --- 2. INITIALIZE AI BRAIN ---
try:
    # Using the massive 120B model for high-IQ reasoning
    local_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)
    
    # Enable SQLite Caching to save tokens on repeated questions
    set_llm_cache(SQLiteCache(database_path="jarvis_memory.db"))
    print("✅ JARVIS: AI Brain & Memory Cache Online.")
except Exception as e:
    print(f"⚠️ AI Initialization Error: {str(e)}")
    local_llm = None

# --- 3. HUMAN SIMULATION UTILITIES ---

def get_resume_text(filepath="resume.txt"):
    """Reads the resume content for AI context."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"⚠️ Warning: {filepath} not found. AI will make professional assumptions.")
        return ""

async def human_delay(min_sec=2.0, max_sec=5.0):
    """Randomized pauses."""
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def human_typing(element, text: str):
    """Types like a human with variable speed."""
    for char in text:
        await element.type(char, delay=random.randint(40, 120))
        if random.random() < 0.07: # Slight human hesitation
            await asyncio.sleep(random.uniform(0.1, 0.3))

async def human_mouse_move(page: Page):
    """Simulates organic mouse movement."""
    await page.mouse.move(random.randint(100, 800), random.randint(100, 600), steps=15)

# --- 4. THE QUESTIONNAIRE ENGINE ---

async def handle_questionnaire(page: Page, resume_text: str):
    """The core engine that handles recruiter chats."""
    if not local_llm: return
    
    try:
        chat_container = page.locator('.chatbot_MessageContainer')
        # Wait for the chat box with a human-like delay
        await chat_container.wait_for(state='visible', timeout=8000)
        print("🚨 JARVIS: Questionnaire detected! Analyzing...")
        
        last_question = ""
        while True:
            if not await chat_container.is_visible():
                print("✅ JARVIS: Chat finished.")
                break

            await asyncio.sleep(random.uniform(2.0, 3.5))
            
            # Scrape the latest bot message
            bot_messages = page.locator('.botItem .botMsg span')
            count = await bot_messages.count()
            if count == 0: continue
            
            latest_question = await bot_messages.nth(count - 1).inner_text()
            if latest_question == last_question: continue
            
            print(f"📝 Recruiter: {latest_question}")
            last_question = latest_question
            
            # DETECT INPUTS
            input_box = page.locator('.textArea[contenteditable="true"]')
            is_text_input = await input_box.is_visible()
            
            available_options = []
            if not is_text_input:
                # Targeted search inside the chat container for all button types
                options_locator = chat_container.locator('.ssrc__label, .ssrc__radio, label, button, .chip, [role="button"]')
                for i in range(await options_locator.count()):
                    txt = await options_locator.nth(i).inner_text() or await options_locator.nth(i).get_attribute("value")
                    if txt and 0 < len(txt.strip()) < 50:
                        available_options.append(txt.strip())
                available_options = list(dict.fromkeys(available_options))[-10:]
                if available_options: print(f"🔘 Options detected: {available_options}")

            # AI REASONING
            prompt_template = """
            Resume: {resume}
            Options: {options}
            Question: {question}
            
            RULES: 
            1. ALWAYS POSITIVE: Say 'Yes' to relocation/shifts/learning.
            2. EXACT MATCH: If options exist, reply ONLY with the choice text.
            3. SCALES: If 1-7, reply '7'. 
            4. BRIEF: Text answers MUST be under 80 chars.
            """
            prompt = prompt_template.format(resume=resume_text, options=available_options, question=latest_question)
            
            print("🧠 JARVIS: Thinking...")
            raw_response = await local_llm.ainvoke(prompt)
            answer = raw_response.content.strip().replace("**", "")
            print(f"✅ JARVIS Answer: {answer}")
            
            # EXECUTE ACTION
            if is_text_input:
                await input_box.click()
                await page.keyboard.press('Control+A')
                await page.keyboard.press('Backspace')
                await human_typing(page.keyboard, answer)
                await human_delay(1, 2)
            elif available_options:
                # Fuzzy matching the AI's choice to the on-screen buttons
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
                    # Blind click fallback
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
        print(f"🤖 JARVIS: Questionnaire loop finished. (Log: {str(e)})")

# --- 5. THE MAIN BOT FLOW ---

async def run_naukri_bot():
    resume_content = get_resume_text()

    async with async_playwright() as p:
        # Launch with slow_mo to bypass fast-action triggers
        browser = await p.chromium.launch(headless=False, slow_mo=random.randint(40, 80))
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            print("🤖 JARVIS: Initiating Human Sequence...")
            await page.goto("https://www.naukri.com", wait_until="networkidle")
            await human_delay(2, 4)

            # LOGIN
            await page.click("text=Login")
            await human_delay(1, 2)
            
            await human_typing(page.locator("//input[@placeholder='Enter your active Email ID / Username']"), EMAIL)
            await human_typing(page.locator("//input[@placeholder='Enter your password']"), PASSWORD)
            await page.click("//button[@type='submit']")

            # Wait for Dashboard (Critical for avoiding ERR_ABORTED)
            await page.wait_for_selector('.nI-gNb-header__logo', timeout=25000)
            print("✅ JARVIS: Logged in. Cooling down...")
            await human_mouse_move(page)
            await human_delay(6, 10) 

            # JOBS PAGE
            print("🤖 JARVIS: Navigating to Jobs...")
            await page.goto("https://www.naukri.com/mnjuser/recommendedjobs", wait_until="load")
            await human_delay(4, 7)

            # BATCH SELECTION
            checkboxes = page.locator('article.jobTuple .tuple-check-box')
            total = await checkboxes.count()
            
            jobs_selected = 0
            for i in range(total):
                if jobs_selected >= 5: break
                cb = checkboxes.nth(i)
                if await cb.is_visible():
                    # Random scroll simulation
                    if random.random() > 0.6: await page.mouse.wheel(0, random.randint(200, 400))
                    
                    is_checked = await cb.locator('.naukicon-ot-Checked').count() > 0
                    if not is_checked:
                        await cb.click()
                        jobs_selected += 1
                        print(f"✅ Selected job {jobs_selected}/5")
                        await human_delay(1.5, 3.0)

            if jobs_selected > 0:
                print(f"🤖 JARVIS: Applying to batch...")
                apply_btn = page.get_by_role("button", name=re.compile(r"^Apply", re.IGNORECASE))
                if await apply_btn.count() > 0:
                    await apply_btn.first.click()
                    await handle_questionnaire(page, resume_content)
                    print("🎉 JARVIS: Operation Successful. Mission Accomplished.")
                    await human_delay(5, 10)

        except Exception as e:
            print(f"❌ JARVIS Total Failure: {str(e)}")
        finally:
            print("🤖 JARVIS: Powering down...")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_naukri_bot())