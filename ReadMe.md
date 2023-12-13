# Hyperchat Api

Hyperchat is a real-time chat application developed using Django and WebSocket technology, allowing users to engage in instant messaging and create chatrooms.

## Getting Started

### Prerequisites

- Python 3.x
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/hudeh/hyperchat.git
    cd hyperchat
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    virtualenv venv
    ```

3. **Activate the virtual environment:**

    - **Windows**

        ```bash
        venv\Scripts\activate
        ```

    - **Linux/macOS**

        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Database Setup

1. **Run migrations to set up the database:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Running the Server

Start the development server:

```bash
python manage.py runserver
