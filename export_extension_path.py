import logging
import re
import threading
import time
import asyncio
import colorlog
import extension
from file import write_line, read_line
from playwright.sync_api import sync_playwright, Page, expect, BrowserContext
from MultipleThread import CustomThread

# Set up logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s:%(levelname)s: %(message)s'
))

logger = logging.getLogger('ЧВК «Вагнер»')
logger.addHandler(handler)

# Set the log level to INFO
logger.setLevel(logging.INFO)


def export_extension_id(profile_id: int, current_thread: int) -> str:
    path_to_extension = f"D:\\Documents\\Gologin_Profile\\extensions\\ex_{profile_id}"
    if current_thread == 0:
        window_position = "0,0"
        executable_path = r"C:\Users\Nguyen Hoang Viet\.gologin\browser\orbita-browser-119\chrome.exe"
    else:
        window_position = "960,0"
        executable_path = r"C:\Users\Nguyen Hoang Viet\.gologin\browser\orbita-browser-120\chrome.exe"

    with sync_playwright() as ap:
        browser = ap.chromium.launch_persistent_context(
            user_data_dir=f"D:\\Documents\\Gologin_Profile\\profile\\profile_{profile_id}",
            headless=False,
            devtools=False,
            executable_path=executable_path,
            args=[
                '--start-maximized',
                f'-window-position={window_position}',
                f"--disable-extensions-except={path_to_extension}",
                f"--load-extension={path_to_extension}"
            ]
        )

        page = browser.new_page()
        page.goto("https://peter.sh/experiments/chromium-command-line-switches/#window-position")
        logger.info(f"Profile {profile_id} in thread {current_thread + 1} went to the page.")

        time.sleep(5)

        for page in browser.pages:
            print(page.url)

        extension_name = extension.get_extension_id(page.url)
        logger.info(f"Succeeded to get extension id {extension_name} from "
                    f"profile {profile} in thread {current_thread + 1}.")
        time.sleep(2)

        # for pg in browser.pages:
        #     pg.close()
        #     time.sleep(0.5)

        browser.close()
        logger.info(f"Profile {profile} in thread {current_thread + 1} is closed.")
        # Close browser
        time.sleep(2)

    return extension_name


if __name__ == '__main__':
    # Setting up threads
    extensions = []

    logger.info("Starting to create threads...")
    profile = 0
    while profile < 99:
        threads = []
        num_threads = 2
        # Create 2 threads
        for i in range(num_threads):
            thread = CustomThread(
                target=export_extension_id,
                args=(
                    profile + 1,
                    i
                )
            )
            logger.info(f"Thread {i + 1} created with profile {profile + 1} "
                        f"and extension path D:\\Documents\\Gologin_Profile\\extensions\\ex_{profile + 1}")
            # Append thread to threads
            threads.append(thread)
            # Increment profile
            profile += 1

        # Start and join threads
        for index, thread in enumerate(threads):
            logger.info(f"Starting profile {profile + 1} in thread {index + 1}...")
            thread.start()
        for index, thread in enumerate(threads):
            extension_id = thread.join()
            extensions.append(extension_id)
            logger.info(f"Profile {profile + 1} in thread {index + 1} is done.")

        # Clear threads
        threads.clear()

    # Write extension list into txt file
    write_line(extensions, "export.txt")
