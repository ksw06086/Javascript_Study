import sys
import asyncio
import subprocess

from pyppeteer.launcher import connect
from pyppeteer.errors import NetworkError


async def main(endpoint):
    try:
        browser = await connect({"browserWSEndpoint": endpoint})
        page = await browser.newPage()
        await asyncio.sleep(2)
        await page.goto("https://ip.pe.kr/")
        await asyncio.sleep(20000)
    except NetworkError as e:
        pass
    except Exception as e:
        print("CP_ENTER_ERROR ::", e)
    finally:
        await browser.close()


if __name__ == "__main__":
    cmd = f"node {sys.path[0]}/create_browser.js"
    js_process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8"
    )
    endpoint = None
    profile = None
    while True:
        output = js_process.stdout.readline()
        if output:
            if "ws:" in output:
                endpoint = output.strip()
                break
            elif ":" in output:
                profile = output.strip()
    print(endpoint)
    print(profile)
    asyncio.run(main(endpoint))
    js_process.kill()
# C:\Users\jyouk\AppData\Local\Google\Chrome\User Data\Default
# search-ms:displayname=Default의%20검색%20결과&crumb=location:C%3A%5CUsers%5Cjyouk%5CAppData%5CLocal%5CGoogle%5CChrome%5CUser%20Data%5CDefault\Extensions
