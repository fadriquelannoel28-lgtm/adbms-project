# ADBMS-project

Medical Stock Management System

## Requirements

- Python 3.8+
- MySQL Server 8.0+

## Setup Instructions

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   - Windows: `.\venv\Scripts\Activate`
   - Mac/Linux: `source venv/bin/activate`

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database (config.py)**
   - Set your MySQL username and password
   - Default: `root` / `G@rbages222`

5. **Initialize Database**
   ```bash
   python init_db.py
   ```

6. **Run Application**
   ```bash
   python app.py
   ```

Open browser at `http://localhost:5000`
