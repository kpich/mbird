dumb little music toy

v v experimental stay tuned

## Setup

Create conda environment (or whatever you want to use here):
```bash
conda create -n mbird python=3.13
conda activate mbird
```

Install Python dependencies:
```bash
pip install -e .[dev]
```

Install Node.js dependencies:
```bash
cd console/frontend
npm install
```

## Running the console

Quick start (uses tmux):
```bash
cd console
./run_console.sh
```

Or manually:

Backend:
```bash
cd console
pip install -e .[dev]
python -m mbird_console.main
```

Frontend (separate terminal):
```bash
cd console/frontend
npm install
npm run dev
```

Open http://localhost:5173
