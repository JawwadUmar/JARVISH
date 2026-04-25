from playwright.async_api import Page
from app.utils.human import human_delay

async def openJobPage(page: Page):
    print("🤖 JARVIS: Navigating to Jobs...")
    await page.goto("https://www.naukri.com/mnjuser/recommendedjobs", wait_until="load")
    await human_delay(1, 2)