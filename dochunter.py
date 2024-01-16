# Doc Hunter
# Find and download technical documentation with Modal and Playwright
# Copyright 2024, Philipp Tsipman
# MIT License

# SETUP

import re
import datetime
from json import JSONEncoder
import modal  # type: ignore
from modal import Stub, web_endpoint  # type: ignore

stub = Stub("doc-hunter")


playwright_image = modal.Image.debian_slim(
    python_version="3.10"
).run_commands(  # Doesn't work with 3.11 yet
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "pip install playwright==1.30.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)

# Add if want to post to slack
# slack_sdk_image = modal.Image.debian_slim().pip_install("slack-sdk")

# FUNCTIONS


# Get all the links on a page
@stub.function(image=playwright_image)
async def get_page_links(url: str) -> dict[str, str, set[str]]:
    from playwright.async_api import async_playwright  # type: ignore

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        # get page title
        title = await page.title()
        links = await page.eval_on_selector_all(
            "a[href]", "elements => elements.map(element => element.href)"
        )
        await browser.close()

    return {"url": url, "title": title, "links": set(links)}


# Get the content of a page
@stub.function(image=playwright_image)
async def get_page_content(url: str) -> dict[str, str, str, str]:
    from playwright.async_api import async_playwright  # type: ignore

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        # get page title
        title = await page.title()
        # get page body text without html tags
        content = await page.inner_text("body")
        content = re.sub(r"\s", " ", content)
        await browser.close()

    return {
        "url": url,
        "title": title,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "content": content,
    }


# Add if want to post to slack
# @stub.function(
#     image=slack_sdk_image,
#     secret=modal.Secret.from_name("scraper-slack-secret"),
# )
# def bot_token_msg(channel, message):
#     import slack_sdk

#     print(f"Posting {message} to #{channel}")
#     client = slack_sdk.WebClient(token=os.environ["SLACK_BOT_TOKEN"])
#     client.chat_postMessage(channel=channel, text=message)


# Main scraper function
@stub.function()
def scrape(links_to_hunt: list[str] = ["https://modal.com/docs"]):
    # all the links found on the pages to hunt
    found_links = []

    # all documentation to gather
    documentation = []

    # find reference pages
    found_ref_pages = get_page_links.map(links_to_hunt)

    # filter out duplicate and non-reference links
    for ref_page in found_ref_pages:
        for link in ref_page["links"]:
            # if link starts with any of the links_to_hunt urls and is not already in returned_links set then add it
            if (
                any(link.startswith(l) for l in links_to_hunt)
                and link not in found_links
            ):
                found_links.append(link)

    print(found_links)

    # docs from reference pages
    # doc = {"url": url, "title": title, "content": content}
    found_docs = get_page_content.map(found_links)

    for doc in found_docs:
        documentation.append(doc)

    # Add if want to post to slack
    # bot_token_msg.remote("scraped-links", link)

    return documentation


# Add if want to run daily
# @stub.function(schedule=modal.Period(days=1))
# def daily_scrape():
#     scrape.remote()

# Add if want to run locally
# @stub.local_entrypoint()
# def run():
#     scrape.remote()


# WEB ENDPOINT


# Take a query string of urls to search
# q = https://modal.com/docs,https://modal.com/examples
@stub.function()
@web_endpoint()
def hunt(q: str):
    print(q)
    # split q into list of urls
    links_to_hunt = q.split(",")
    return scrape.remote(links_to_hunt)
