IoT Phase One .README

How to run it:
1. Extract the project files from the ZIP archive.
2. Open a terminal or command prompt and navigate to the project directory. If for example you unzipped the folder in Downloads move it to Desktop and do ‘ls’ to view where you are and then ‘cd Desktop’ to get there and then ‘ls’ again, then ‘cd iot-project-phase1/’ or just type iot then TAB.
3. Install Flask if you haven't already: `pip install Flask`
4. Run the Flask application: `python app.py`
5. Open a web browser and go to `http://127.0.0.1:5000/` to view the dashboard.

Project Structure:
- `app.py`: Contains the Flask application code.
- `static/`: Contains static files such as CSS and JavaScript.
- `views/`: Contains the HTML template for the dashboard (`index.html`).

Notes:
- The `app.py` file contains a basic Flask application with routes for serving the HTML template and static files.
- The `index.html` file in the `views/` folder is the main dashboard template.
