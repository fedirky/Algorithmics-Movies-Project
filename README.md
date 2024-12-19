## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/fedirky/Algorithmics-Movies-Project.git
    cd Algorithmics-Movies-Project
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate #On Linux use source ./.venv/bin/activate
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
    .\.venv\Scripts\activate
    python manage.py runserver
    ```

5. **Create admin account and login:**
    ```
    TODO: explain in details.
    ```

## Usage

**Access the application:**
    Open your browser and go to `http://127.0.0.1:8000`.