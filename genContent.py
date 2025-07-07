# from google import genai
# import config

# client = genai.Client(api_key = config.API_KEY)

# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="Explain how LLM works in a few words" #prompt
# )

# print(response.text)

from google import genai
import asyncio
from pyppeteer import launch
import config

client = genai.Client(api_key = config.API_KEY)

url = "https://www.google.com/maps/place/Hanoi+Old+Quarter+Vancouver/@49.2620859,-123.1673829,16.11z/data=!4m6!3m5!1s0x54867300194ca705:0xfb41b64395111797!8m2!3d49.2643913!4d-123.1741815!16s%2Fg%2F11ln_pb3sv?entry=ttu&g_ep=EgoyMDI1MDYyOS4wIKXMDSoASAFQAw%3D%3D"

async def scrape_reviews(url):
    reviews = []
    browser = await launch({"headless": True, "args" : ["--window-size = 800, 3200"]})

    page = await browser.newPage()
    await page.setViewport({"width": 800, "height": 3200})
    await page.goto(url)
    await page.waitForSelector('.jftiEf')

    elements = await page.querySelectorAll('.jftiEf')
    for element in elements:
        await page.waitForSelector('.w8nwRe')
        more_btn = await element.querySelector('.w8nwRe')
        if more_btn is not None:
            await page.evaluate("button => button.click()", more_btn)
            await page.waitFor(5000)
        await page.waitForSelector('.MyEned')
        snippet = await element.querySelector('.MyEned')
        text = await page.evaluate('selected => selected.textContent', snippet)
        reviews.append(text)

    await browser.close()
    return reviews

def summarize(reviews):
    prompt = "I've collected some reviews of a place I was consider going, can you summarize the reviews for me?\n"
    for review in reviews:
        prompt += "\n" + review
    print(prompt)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    print("\nGemini's response:")
    print(response.text)

reviews = asyncio.run(scrape_reviews(url))
summarize(reviews)
# print(reviews)