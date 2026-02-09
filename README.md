# Python File Archival & Categorization System 🗄️

An automated Python-based file management tool that monitors a source directory, categorizes files by type, moves them to organized folders, and compresses them into daily date-based ZIP archives. Designed for reliability, modularity, and production environments.

## 🚀 Features

- **Automated Categorization**: Detects file types (Images, Music, Videos, Documents) and sorts them automatically.
- **Daily Archiving**: Compresses processed files into dated ZIP archives (`images_09022026.zip`) to save space.
- **Data Integrity**: 
  - **Checksum Validation**: Verifies file integrity before and after moving.
  - **Stability Checks**: Ensures files are fully copied/written before processing.
  - **File Locking**: Skips files currently in use by other processes.
- **Safe Operations**:
  - **Collision Handling**: Automatically renames duplicate files with timestamps.
  - **Idempotency**: Safe to re-run multiple times without data duplication or loss.
- **Observability**:
  - **Structured Logging**: detailed logs with daily rotation.
  - **Dry-Run Mode**: Preview actions without making any changes.
- **Configurable**: All paths, extensions, and settings are managed via `.env`.

## 📂 Directory Structure

```plaintext
project/
├── config/             # Configuration management
│   └── settings.py     # Loads environment variables
├── services/           # Core business logic
│   ├── file_scanner.py # Scans & validates files
│   ├── categorizer.py  # Determines file categories
│   ├── mover.py        # Handles file moves & checksums
│   └── zipper.py       # Manages ZIP archiving
├── utils/              # Helper utilities
│   ├── logger.py       # Logging configuration
│   └── helpers.py      # Common functions (checksums, etc.)
├── tests/              # Unit and integration tests
├── main.py             # CLI entry point
├── requirements.txt    # Project dependencies
└── .env.example        # Configuration template
```

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/file-archival-bot.git
    cd file-archival-bot
    ```

2.  **Set up a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r project/requirements.txt
    ```

## ⚙️ Configuration

1.  **Create the `.env` file**:
    Copy the example configuration file to create your local config.
    ```bash
    cp project/.env.example project/.env
    # On Windows PowerShell:
    Copy-Item project/.env.example project/.env
    ```

2.  **Edit `.env`**:
    Open `project/.env` and update the paths and settings as needed.
    ```ini
    SOURCE_DIR=./data/incoming
    TARGET_DIR=./data/processed
    ARCHIVE_DIR=./data/archive
    
    # Customize extensions
    EXT_IMAGES=.jpg,.jpeg,.png
    EXT_DOCUMENTS=.pdf,.docx,.txt
    
    # Validation settings
    ENABLE_CHECKSUM=True
    ```

## 🏃 Usage

**Run the archival process:**
```bash
python project/main.py
```

**Run in Dry-Run Mode (Simulation):**
See what *would* happen without moving any files.
```bash
python project/main.py --dry-run
```

**Running Tests:**
```bash
# Run unit tests
pytest project/tests/

# Run integration test (end-to-end verification)
python project/tests/integration_test.py
```

## 🤖 Scheduling

### Windows Task Scheduler
Create a basic task to run `python project/main.py` daily. Ensure the "Start in" folder is set to the project root.

### Cron (Linux)
Add a crontab entry for daily execution at 11 PM:
```bash
0 23 * * * /path/to/venv/bin/python /path/to/project/main.py >> /var/log/archival_bot.log 2>&1
```

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a Pull Request.

1.  Fork the repo
2.  Create your feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add some amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
