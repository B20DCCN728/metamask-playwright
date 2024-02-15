import logging, threading
import re
import time
from playwright.sync_api import sync_playwright, Page, expect, BrowserContext, BrowserType
import colorlog
import JSON
import file

# Set up logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s:%(levelname)s: %(message)s'
))

logger = logging.getLogger('ЧВК «Вагнер»')
logger.addHandler(handler)

# Set the log level to INFO
logger.setLevel(logging.INFO)


def import_metamask_phrase(
        extension_id: str,
        wallet: dict[str, str, str],
        current_profile: int,
        current_thread: int
) -> None:
    path_to_extension = f"D:\\Documents\\Gologin_Profile\\extensions\\ex_{current_profile}"

    if current_thread == 0:
        window_position = "0,0"
        executable_path = r"C:\Users\Nguyen Hoang Viet\.gologin\browser\orbita-browser-119\chrome.exe"
    else:
        window_position = "960,0"
        executable_path = r"C:\Users\Nguyen Hoang Viet\.gologin\browser\orbita-browser-120\chrome.exe"

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=f"D:\\Documents\\Gologin_Profile\\profile\\profile_{current_profile}",
            headless=False,
            devtools=False,
            executable_path=executable_path,
            args=[
                '--start-maximized',
                f'-window-position={window_position}',
                '--disable-blink-features=AutomationControlled',
                f"--disable-extensions-except={path_to_extension}",
                f"--load-extension={path_to_extension}"
            ]
        )

        page = browser.new_page()
        page.set_viewport_size({
            "width": 640,
            "height": 1080
        })

        # Link
        page.goto(
            f"chrome-extension://{extension_id}/home.html#onboarding/welcome"
        )
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} went to the page."
        )
        time.sleep(2)

        # Tick I agree to MetaMask's Terms of use
        page.locator('xpath=//*[@id="onboarding__terms-checkbox"]').click()
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} clicked ✅ I agree to MetaMask's Terms of use"
        )
        time.sleep(5)

        # Click Import an existing wallet button
        page.locator(
            'xpath=//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[3]/button'
        ).click()
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} clicked ✅ Import an existing wallet"
        )
        time.sleep(2)

        # Click ✅ I agree button
        page.locator(
            'xpath=//*[@id="app-content"]/div/div[2]/div/div/div/div/button[1]'
        ).click()
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} clicked ✅ I agree"
        )
        time.sleep(5)

        # Type Secret Recovery Phrase
        count = 0
        for key in wallet["mnemonic"].split(" "):
            page.locator(
                f'xpath=//*[@id="import-srp__srp-word-{count}"]'
            ).fill(f'{key}')
            logger.info(
                f"Profile {current_profile} in thread {current_thread + 1} typed ✅ mnemonic {count + 1}"
            )
            count += 1

        page.locator(
            'xpath=//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/button'
        ).click()
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} clicked ✅ Confirm Secret Recovery Phrase"
        )
        time.sleep(2)

        page.get_by_test_id("create-password-new").fill(
            '314159265'
        )
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} typed ✅ Password"
        )
        time.sleep(1)

        page.get_by_test_id("create-password-confirm").fill(
            '314159265'
        )
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} typed ✅ Password Confirm"
        )
        time.sleep(1)

        page.locator(
            'xpath=//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input'
        ).click()
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} clicked ✅ I understand that MetaMask cannot "
        )
        time.sleep(2)

        page.locator(
            'xpath=//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'
        ).click()
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} clicked ✅ Import my wallet button"
        )
        time.sleep(2)

        page.locator(
            'xpath=//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
        ).click()
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} clicked ✅ Import my wallet button"
        )
        time.sleep(2)

        page.locator(
            'xpath=//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
        ).click()
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} clicked ✅ Next button"
        )
        time.sleep(2)

        page.locator(
            'xpath=//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
        ).click()
        logger.info(
            f"Profile {current_profile} in thread {current_thread + 1} clicked ✅ Done button"
        )
        time.sleep(5)

        # Close page
        page.close()
        logger.info(f"Profile {current_profile} in thread {current_thread + 1} is closed")
        # Close browser
        browser.close()

        time.sleep(2)


if __name__ == '__main__':
    # Read wallets from eth.json
    wallets = JSON.read("eth.json")
    # Read extension ids from export.txt
    extension_ids = file.read_line("export.txt")

    # Setting up threads
    num_threads = 2
    profile = 0
    while profile < 99:
        threads = []
        # Create 2 threads
        for i in range(num_threads):
            thread = threading.Thread(
                target=import_metamask_phrase,
                args=(
                    extension_ids[profile],
                    wallets[profile],
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
            thread.join()
            logger.info(f"Profile {profile + 1} in thread {index + 1} is done.")

        # Clear threads
        threads.clear()
