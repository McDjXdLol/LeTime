# LeTime

LeTime is a desktop application activity tracker, similar in functionality to applications like [ActivityWatch](https://github.com/ActivityWatch/activitywatch). It's built with a C++ backend for tracking application usage and a Python/Flask frontend for a web-based user interface to visualize the data.
>**Note:** To be fair I'm not actively maintaining this app currently 👍 At least for now. A lot of things doesn't work and a lot of things are still not added. This was supposed to be my "I want to learn C++" project, but after a while I decided I'd had enough, so I'm leaving it for now. But if you want you can add it yourself. 💀💀💀


## Screenshots
| Light Mode | Dark Mode |
|------------|-----------|
| ![light](https://github.com/user-attachments/assets/6f467c6e-a87f-40a1-b421-0ea50c9885e3) | ![dark](https://github.com/user-attachments/assets/57ba32ca-aeca-4161-ac37-9309d6f2b8cf) |



## Features

- **Application Usage Tracking:** Monitors the time spent on various applications.
- **Data Persistence:** Saves daily usage data to a CSV log file.
- **Web-Based Dashboard:** Provides a clean and interactive dashboard to visualize your activity.
- **Daily Summary & Trend Analysis:** Displays total time usage for a selected day and a trend chart for recent activity.
- **Dark Mode:** A toggle for a more comfortable viewing experience.
> **Dark Mode** doesn't fully work, text color is kinda the same as background in dark mode.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need the following installed:

- A C++ compiler (e.g., MinGW, MSVC)
- Python 3.x
- pip (Python package installer)

The project also has a `requirements.txt` file which you will need to install.

### Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/McDjXdLol/LeTime.git](https://github.com/McDjXdLol/LeTime.git)
    cd LeTime
    ```

2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### How to Run

1.  **Build the C++ backend:**
    Navigate to the directory containing `main.cpp` and compile it. The executable file **must be named `app.exe`** for the Python script to find it.

    Example using g++ (on Windows):
    ```bash
    g++ main.cpp -o app.exe
    ```

2.  **Run the Python application:**
    After building the C++ executable, start the main Python script from the project's root directory. This script will launch both the C++ tracker and the Flask web server.

    ```bash
    python main.py
    ```

3.  **Access the Dashboard:**
    Open your web browser and navigate to the local server address (usually `http://127.0.0.1:5000`) to view your activity dashboard.

## Project Structure

- `main.cpp`: The C++ backend for tracking active applications and saving data.
- `main.py`: The Python application that manages the C++ process and serves the web frontend.
- `front/main.py`: The Flask web server that handles the API and serves the dashboard.
- `front/index.html`: The web-based dashboard interface.
- `front/logs/`: Directory where the daily CSV logs are stored.
- `requirements.txt`: A list of all required Python libraries.

## License

[MIT License](LICENSE)
