from playwright.async_api import Page
from app.utils.human import human_delay

async def openJobPage(page: Page):
    print("🤖 JARVIS: Navigating to Jobs...")
    await page.goto("https://www.naukri.com/mnjuser/recommendedjobs", wait_until="load")
    try:
        await page.wait_for_selector('article.jobTuple', timeout=15000)
    except Exception as e:
        print(f"🤖 JARVIS: Could not find job listings, continuing anyway... {e}")
    await human_delay(4, 7)