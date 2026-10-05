# Music Time Machine

Scrapes Billboard Hot 100 for a given date and builds a private Spotify playlist.

## Setup
1. Create a Spotify Developer app; set redirect URI to match `.env`.
2. Copy `.env.example` → `.env` with client id/secret/redirect URI.
3. `pip install spotipy beautifulsoup4 requests python-dotenv`

## Run
```
python "Music time machine.py"
```
