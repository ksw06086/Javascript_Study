import sys
import subprocess
import asyncio
from pyppeteer.errors import NetworkError
from pyppeteer.launcher import connect

class CreateBrowser:
    def __init__(self):
        self.endpoint = None

    async def get_browser_endpoint(self):
        try:
            cmd = f"node {sys.path[0]}/../vpn_browser/create_browser.js"

            js_process = await asyncio.to_thread(
                subprocess.Popen, cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8"
            )
            while True:
                output = js_process.stdout.readline()
                if output:
                    if "ws:" in output:
                        self.endpoint = output.strip()
                        break
                    elif ":" in output:
                        profile = output.strip()
        except NetworkError as e:
            pass
        except Exception as e:
            print("CP_ENTER_ERROR:", e)
            pass
        return self.endpoint

    async def get_browser(self):
        if self.endpoint is None:
            await self.get_browser_endpoint()
        browser = await connect({"browserWSEndpoint": self.endpoint})
        return browser