import os
from dotenv import load_dotenv
load_dotenv()

from api import create_app


print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)