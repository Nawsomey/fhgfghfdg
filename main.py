import threading
import random
import string
import time
import requests
import sys
import os
from colorama import Fore, init
from names import get_full_name
from datetime import timedelta
from urllib.parse import urlparse, parse_qs
from timeit import default_timer as timer

init()
thread_lock = threading.Lock()
created_links = 0


class Utils:
    @staticmethod
    def get_proxy():
        proxy = random.choice(open("proxies.txt").read().splitlines())
        return {"http": "http://" + proxy, "https": "http://" + proxy}

    @staticmethod
    def get_logins():
        return {
            "username": "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(11)
            ),
            "email": get_full_name().replace(" ", ".")
            + "".join(random.choice(string.digits) for _ in range(5))
            + random.choice(["@gmail.com", "@outlook.com", "@hotmail.com"]),
            "password": "".join(
                random.choice(string.digits + string.ascii_letters) for _ in range(10)
            ),
        }


class Console:
    """Console utils"""

    @staticmethod
    def _time():
        return time.strftime("%H:%M:%S", time.gmtime())

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    # Safe print, to stop overlapping when printing in thread tasks
    @staticmethod
    def sprint(content: str, status: bool = True) -> None:
        thread_lock.acquire()
        sys.stdout.write(
            f"[{Fore.LIGHTBLUE_EX}{Console()._time()}{Fore.RESET}] {Fore.GREEN if status else Fore.RED}{content}"
            + "\n"
            + Fore.RESET
        )
        thread_lock.release()

    @staticmethod
    def update_title() -> None:
        start = timer()

        while True:
            thread_lock.acquire()
            end = timer()
            elapsed_time = timedelta(seconds=end - start)
            os.system(
                f"title Opti made this but he scammer men │ Created Links: {created_links} │ Elapsed: {elapsed_time}"
            )
            thread_lock.release()


class Promo:
    def __init__(self, proxyless: bool = True) -> None:
        self.proxyless = proxyless
        self.useragent = f"Medal-Electron/4.1674.0 (string_id_v2; no_upscale) win32/10.{random.randint(0,3)}.19042 (x64) Electron/8.5.5 Recorder/1.0.0 Node/12.13.0 Chrome/{random.randint(70,85)}.0.3987.163 Environment/production"

    def __main__(self, token: str):
        for _ in range(3):
            try:
                self.client = requests.Session()

                if not self.proxyless:
                    proxy = Utils().get_proxy()
                    self.client.proxies.update(proxy)

                init = Utils().get_logins()
                self.username, self.email, self.password = (
                    init["username"],
                    init["email"],
                    init["password"],
                )

                response = self.client.post(
                    "https://medal.tv/api/users",
                    json={
                        "email": self.email,
                        "userName": self.username,
                        "password": self.password,
                    },
                    headers={
                        "User-Agent": self.useragent,
                        "Medal-User-Agent": self.useragent,
                    },
                )

                if not (response.status_code in [201, 200, 204]):
                    Console().sprint(
                        f"Something went wrong [1], error: {response.json()}", False
                    )
                    return False

                auth = self.client.post(
                    "https://medal.tv/api/authentication",
                    json={"email": self.email, "password": self.password},
                    headers={
                        "User-Agent": self.useragent,
                        "Medal-User-Agent": self.useragent,
                    },
                )

                if not (auth.status_code in [201, 200, 204]):
                    Console().sprint(
                        f"Something went wrong [2], error: {auth.json()}", False
                    )
                    return False

                auth_response = auth.json()
                authentication = f'{auth_response["userId"]},{auth_response["key"]}'

                response = self.client.post(
                    "https://medal.tv/social-api/connections",
                    json={"provider": "discord"},
                    headers={
                        "User-Agent": self.useragent,
                        "Medal-User-Agent": self.useragent,
                        "X-Authentication": authentication,
                    },
                )

                if not (response.status_code in [201, 200, 204]):
                    Console().sprint(
                        f"Something went wrong [3], error: {response.json()}", False
                    )
                    return False

                login_url = response.json()["loginUrl"]

                login = self.client.post(
                    login_url,
                    headers={"Authorization": token},
                    json={"permissions": "0", "authorize": True},
                )

                if not (login.status_code in [201, 200, 204]):
                    Console().sprint(
                        f"Something went wrong [4], error: {login.json()}", False
                    )
                    return False

                link = login.json()["location"]

                response = self.client.get(link)

                parsed = parse_qs(urlparse(link).query)

                try:
                    if parsed["status"][0] == "error":
                        Console().sprint("Error: " + parsed["message"][0], False)
                        return False
                except:
                    pass

                response = self.client.get(
                    "https://medal.tv/api/social/discord/nitroCode",
                    headers={
                        "User-Agent": self.useragent,
                        "Medal-User-Agent": self.useragent,
                        "X-Authentication": authentication,
                    },
                )

                if not (response.status_code in [201, 200, 204]):
                    if (
                        "discord connection"
                        in str(response.json()["errorMessage"]).lower()
                    ):
                        Console().sprint(
                            f"This token has already claimed | {token}", False
                        )
                        thread_lock.acquire()
                        with open("tokens.txt", "r+") as io:
                            tokens = io.readlines()
                            io.seek(0)
                            for line in tokens:
                                if not (token in line):
                                    io.write(line)
                            io.truncate()
                        thread_lock.release()
                    else:
                        Console().sprint(
                            f"Something went wrong [5], error: {response.json()}", False
                        )
                    return False

                nitro_link = response.json()["url"]

                Console().sprint("Nitro Code: " + nitro_link)

                thread_lock.acquire()

                with open("Nitro.txt", "a") as links:
                    links.write(nitro_link + "\n")

                global created_links
                created_links += 1

                with open("tokens.txt", "r+") as io:
                    tokens = io.readlines()
                    io.seek(0)
                    for line in tokens:
                        if not (token in line):
                            io.write(line)
                    io.truncate()

                thread_lock.release()

                return True
            except:
                pass


if __name__ == "__main__":
    Console().clear()
    tokens = open("tokens.txt", "r").read().splitlines()

    if len(tokens) <= 0:
        Console().sprint("There are no tokens in tokens.txt!", False)
        time.sleep(5)
        os._exit(1)

    if len(open("proxies.txt", "r").read().splitlines()) <= 0:
        proxyless = True
    else:
        proxyless = False

    threading.Thread(target=Console().update_title).start()

    try:
        threads = []
        for token in tokens:
            if ":" in token:
                token = token.split(":")[2]
            _thread = threading.Thread(target=Promo(proxyless).__main__, args=(token,))
            threads.append(_thread)
            _thread.start()

        for thread in threads:
            thread.join()
    except:
        pass
