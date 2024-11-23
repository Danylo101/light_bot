import asyncio
import aiohttp
import subprocess

async def check_router(ip_address):
    # Ping
    ping = await check_ping(ip_address)

    # HTTP Check with aiohttp
    http = False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{ip_address}", timeout=5) as response:
                if response.status == 200:
                    is_http_successful = True
    except Exception as e:
        pass

    # TCP Port Check
    is_tcp_successful = False
    try:
        reader, writer = await asyncio.open_connection(ip_address, 80)
        is_tcp_successful = True
        writer.close()
        await writer.wait_closed()
    except:
        pass

    # Combine results
    if ping or is_http_successful or is_tcp_successful:
        return "Світло є"
    else:
        return "Світла намає"


async def check_ping(ip_address):
    process = await asyncio.create_subprocess_shell(
        f"ping -n 1 {ip_address}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return True
    else:
        return False

