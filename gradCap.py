import asyncio
from seatArrangement import arrange
from serverConnect import connect

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        connect(),
        arrange(),
    )

asyncio.run(main())






