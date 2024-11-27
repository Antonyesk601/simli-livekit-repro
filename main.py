import asyncio
from simli import SimliClient, SimliConfig

from simli.livekit_renderer import LivekitRenderer
from livekit import rtc, api

import os
from dotenv import load_dotenv

load_dotenv(".env", override=True)

with open("test_audio.raw", "rb") as f:
    audio = f.read()


async def main():
    async with SimliClient(
        SimliConfig(
            os.getenv("SIMLI_API_KEY", ""),  # API Key https://app.simli.com
            os.getenv(
                "SIMLI_FACE_ID", ""
            ),  # Face ID https://docs.simli.com/api-reference/available-faces
            maxSessionLength=60,
            maxIdleTime=15,
        ),
    ) as connection:
        livekitURL = os.getenv("LIVEKIT_URL", "")
        livekitToken = (
            api.AccessToken(
                os.getenv("LIVEKIT_API_KEY", ""),
                os.getenv("LIVEKIT_API_SECRET", ""),
            )
            .with_identity("python-publisher")
            .with_name("Python Publisher")
            .with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=os.getenv("LIVEKIT_ROOM", ""),
                )
            )
            .to_jwt()
        )
        renderTask = asyncio.create_task(
            LivekitRenderer(
                connection,
                livekitURL,
                livekitToken,
                rtc.Room(loop=asyncio.get_running_loop()),
            ).render()
        )
        for i in range(5):
            await connection.send(audio)
            await asyncio.sleep(10)
        # await connection.sendSilence()
        print("Done")
        await renderTask
        await connection.stop()


asyncio.run(main())
