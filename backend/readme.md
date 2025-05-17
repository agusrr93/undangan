# Project Setup

This project uses **Python 3.10.13** managed via `pyenv`, along with a virtual environment.

---

## ⚙️ Requirements

- [pyenv](https://github.com/pyenv/pyenv)
- Python build dependencies (`xcode-select --install` on macOS, `build-essential libpq-dev` on Linux)

---

## 🚀 Setup Instructions

Run the following commands step by step:

```bash
# Install the required Python version
pyenv install 3.10.13

# Set the Python version for this project
pyenv local 3.10.13

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip (recommended)
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt


🐘 Running PostgreSQL with Docker

To run a local PostgreSQL database container:
docker run --name my-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=comments_db -p 5432:5432 -d postgres:15