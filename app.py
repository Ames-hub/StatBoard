from webui.manage import main as webui_main
from database import db
import sys
import os

class Statbot:
    @staticmethod
    def run_django():
        # Adjust the path to the webui directory
        sys.path.append(os.path.join(os.path.dirname(__file__), 'webui'))

        # Set the DJANGO_SETTINGS_MODULE environment variable
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # Adjust as necessary

        webui_main()

if __name__ == "__main__":
    # Modernize the DB
    db.modernize()

    # Run the Django server
    Statbot.run_django()
