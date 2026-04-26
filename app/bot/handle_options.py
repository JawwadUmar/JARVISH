from playwright.async_api import Locator

async def getAvailableOptions(chat_container: Locator):
    available_options: list[str] = []

     # Targeted search inside the chat container for all button types
    options_locator = chat_container.locator('.ssrc__label, .ssrc__radio, label, button, .chip, [role="button"]')
    for i in range(await options_locator.count()):
        txt = await options_locator.nth(i).inner_text() or await options_locator.nth(i).get_attribute("value")
        if txt and 0 < len(txt.strip()) < 50:
            available_options.append(txt.strip())
    available_options = list(dict.fromkeys(available_options))[-10:]
    return available_options
    if available_options: print(f"🔘 Options detected: {available_options}")