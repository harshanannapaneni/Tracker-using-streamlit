# Shift Tracker

**Shift Tracker** is a web application built with **Streamlit** and **PostgreSQL** to help users track their work shifts, calculate total worked hours, and compute earnings.

## Features

- Add and store shift details (date, start time, end time, break time, daily rate, problems encountered).
- Automatically calculate total hours worked and earnings.
- View stored shifts in a structured table.
- Get summary statistics for total hours worked and total amount earned.
- PostgreSQL database integration for persistent data storage.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: PostgreSQL (configured using Streamlit secrets)

## Installation & Setup

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/shift-tracker.git
cd shift-tracker
```

### 2. Create a Virtual Environment (Optional but Recommended)

```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate      # For Windows
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure Database Credentials

Create a `.streamlit/secrets.toml` file and add your PostgreSQL credentials:

```toml
[postgresql]
host = "your-db-host"
port = 5432
database = "your-db-name"
user = "your-db-username"
password = "your-db-password"
```

### 5. Run the Application

```sh
streamlit run shift_tracker.py
```

## Deployment

You can deploy this app on **Streamlit Community Cloud** by adding the repository to Streamlit and configuring the database credentials in the `secrets.toml` file.

## License

This project is licensed under the MIT License.

---

**Author**: Harsha Nannapaneni
**GitHub**: [your-username](https://github.com/harshanannapaneni)
