```bash
git clone https://github.com/antonyesk601/simli-livekit-repro
cd simli-livekit-repro
uv venv -p 3.11
uv sync
# Create a .env file with the following variables
#SIMLI_FACE_ID
#SIMLI_API_KEY
#LIVEKIT_API_KEY
#LIVEKIT_API_SECRET
#LIVEKIT_URL
#LIVEKIT_ROOM
python main.py
```
