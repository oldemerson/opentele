
import sys, pathlib
base_dir = pathlib.Path(__file__).parent.parent.absolute().__str__()
sys.path.insert(1, base_dir)


from src.td import TDesktop
from src.tl.telethon import TelegramClient
from src.api import API, CreateNewSession, UseCurrentSession

import asyncio
import pytest
import pytest_asyncio
from _pytest._io import TerminalWriter

async def tdata_to_telethon():
    

    api_desktop = API.TelegramDesktop.Generate("windows", "!thedemons#opentele")
    api_ios = API.TelegramIOS.Generate("!thedemons#opentele")

    tdesk = TDesktop("tests/tdata_test_profile", api_desktop, "!thedemons#opentele", "opentele#thedemons!")
    assert tdesk.isLoaded()
    

    oldClient = await tdesk.ToTelethon(flag=UseCurrentSession, api=api_desktop)
    await oldClient.connect()
    assert await oldClient.is_user_authorized()

    await oldClient.PrintSessions()

    newClient = await tdesk.ToTelethon(flag=CreateNewSession,  api=api_ios, password="!thedemons#opentele")
    await newClient.connect()
    assert await newClient.is_user_authorized()

    await newClient.PrintSessions()

    await oldClient.TerminateAllSessions()

    tdesk = await oldClient.ToTDesktop(UseCurrentSession, api=api_desktop)
    tdesk.SaveTData("tests/tdata_test_profile", "!thedemons#opentele", "opentele#thedemons!")



# Fix for "RuntimeError: Event loop is closed"
# Thanks to https://github.com/pytest-dev/pytest-asyncio/issues/30

@pytest_asyncio.fixture
def event_loop():
    writer = TerminalWriter(sys.stdout)
    writer.hasmarkup = True
    writer.write("\n\n")
    writer.sep("=", "Begin testing for opentele package", yellow=True)

    policy = asyncio.get_event_loop_policy()
    res = policy.new_event_loop()
    res._close = res.close
    res.close = lambda: None
    res.run_until_complete(tdata_to_telethon())
    
    yield res

@pytest.mark.asyncio
async def test_entry_point(event_loop):
    pass



