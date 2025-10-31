dumb little music toy

v v experimental stay tuned

## Running the console

Quick start (uses tmux):
```bash
cd mbird_console
./run_console.sh
```

Or manually:

Backend:
```bash
cd mbird_console
pip install -e .[dev]
python -m mbird_console.main
```

Frontend (separate terminal):
```bash
cd mbird_console/frontend
npm install
npm run dev
```

Open http://localhost:5173
