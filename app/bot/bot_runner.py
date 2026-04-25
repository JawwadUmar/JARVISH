import random
from playwright.async_api import async_playwright
from app.config.config import EMAIL, PASSWORD
from app.utils.human import human_delay, human_typing, human_mouse_move
from app.bot.handle_questions import handle_questionnaire
import re
from langchain_groq import ChatGroq

async def run_bot(llm:ChatGroq, resume:str, prompt:str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=random.randint(40, 80)
        )

        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        page = await context.new_page()

        try:
            print("🤖 JARVIS: Initiating Human Sequence...")
            await page.goto("https://www.naukri.com", wait_until="networkidle")
            await human_delay(2, 4)

            # login
            await page.click("text=Login")
            await human_delay(1, 2)

            

            await human_typing(
                page.locator("//input[@placeholder='Enter your active Email ID / Username']"),
                EMAIL
            )

            await human_typing(
                page.locator("//input[@placeholder='Enter your password']"),
                PASSWORD
            )

            await page.click("//button[@type='submit']")

            await page.wait_for_selector('.nI-gNb-header__logo', timeout=15000)
            print("✅ JARVIS: Logged in. Cooling down...")
            await human_mouse_move(page)
            await human_delay(6, 10)

            while True:
                print("🤖 JARVIS: Navigating to Jobs...")
                await page.goto("https://www.naukri.com/mnjuser/recommendedjobs", wait_until="load")
                await human_delay(4, 7)

                tabs_to_check = [None, '#similar_jobs .tab-list-item']
                
                for tab_locator in tabs_to_check:
                    if tab_locator:
                        print("🤖 JARVIS: Checking 'You might like' tab...")
                        try:
                            tab = page.locator(tab_locator)
                            if await tab.is_visible():
                                await tab.click()
                                await human_delay(3, 6)
                            else:
                                print("🤖 JARVIS: 'You might like' tab not visible.")
                                continue
                        except Exception as e:
                            print(f"🤖 JARVIS: Could not click tab: {e}")
                            continue

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
                            await handle_questionnaire(page, llm, resume, prompt)
                            print("🎉 JARVIS: Batch Operation Successful. Taking a short break before next batch.")
                            await human_delay(15, 30)
                        break
                    else:
                        print(f"🤖 JARVIS: No unapplied jobs found on current tab.")
                
                if jobs_selected == 0:
                    print("🤖 JARVIS: No unapplied jobs found on any tabs. Waiting before checking again...")
                    await human_delay(60, 120)
        except Exception as e:
            print(f"Error: {e}")
            await human_delay(60, 120)

        finally:
            print("🤖 JARVIS: Powering down...")
            await browser.close()