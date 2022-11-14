import asyncio
from playwright.async_api import Playwright, async_playwright, expect

GLOBAL_TIMEOUT = 300000


async def run(playwright: Playwright, worker_id: int) -> None:
    print(f'{worker_id} operational!')
    # browser = await playwright.chromium.launch(headless=False)
    browser = await playwright.chromium.launch(timeout=GLOBAL_TIMEOUT)
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto("https://alenka.ru/", timeout=GLOBAL_TIMEOUT)
    print(f'Worker {worker_id} https://alenka.ru/ loaded')
    await page.get_by_role("button", name="Хорошо").click(timeout=GLOBAL_TIMEOUT)
    await page.goto("https://alenka.ru/catalog/tolko_v_alenke/", timeout=GLOBAL_TIMEOUT)
    print(f'Worker {worker_id} https://alenka.ru/catalog/tolko_v_alenke/ loaded')

    for i in range(1, 20):
        await page.locator(f"div:nth-child({i}) > .s-card > .s-card-body > .sCalculator > .sCalculator__cart").click(timeout=GLOBAL_TIMEOUT)

    await page.goto("https://alenka.ru/personal/cart/", timeout=GLOBAL_TIMEOUT)
    print(f'Worker {worker_id} https://alenka.ru/personal/cart/ loaded')

    for i in range(1, 40):
        await page.get_by_role("cell", name="шт").locator("span").nth(i).click(click_count=9, timeout=GLOBAL_TIMEOUT)

    # ---------------------
    await context.close()
    await browser.close()


async def main(worker_id) -> None:
    async with async_playwright() as playwright:
        await run(playwright, worker_id)


async def multiple():
    await asyncio.gather(*[main(worker_id) for worker_id in range(15)])


loop = asyncio.get_event_loop()
loop.run_until_complete(multiple())

