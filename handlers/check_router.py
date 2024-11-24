import asyncio
import aiohttp
import subprocess
import platform

async def check_router(ip_address: str, log: bool) -> str:
    errors = []

    # Ping
    ping = await check_ping(ip_address, log, errors)

    # HTTP Check
    http = False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{ip_address}", timeout=5) as response:
                if response.status == 200:
                    http = True
    except Exception as e:
        if log:
            errors.append(f"HTTP помилка: {e}\n")

    # TCP Port Check
    tcp = False
    try:
        reader, writer = await asyncio.open_connection(ip_address, 80)
        tcp = True
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        if log:
            errors.append(f"TCP помилка: {e}\n")

    # Combine results
    if ping or http or tcp:
        result = "Світло є💡"
    else:
        result = "Світла немає\nДіставай ліхтар🔦"

    if log and errors:
        result += f"\nПомилки:\n" + "\n".join(errors)

    return result


async def check_ping(ip_address: str, log: bool, errors: list) -> bool:
    ping_cmd = "ping -n 1" if platform.system() == "Windows" else "ping -c 1"
    process = await asyncio.create_subprocess_shell(
        f"{ping_cmd} {ip_address}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return True
    else:
        if log:
            errors.append(f"Ping помилка: {stderr.decode().strip()}\n")
        return False
