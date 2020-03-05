import os

# Database Settings
DB_NAME=os.getenv('DB_NAME', 'yacs')
DB_USER=os.getenv('DB_USER', 'postgres')
DB_HOST=os.getenv('DB_HOST', '172.17.0.2')
DB_PASSWORD=os.getenv('DB_PASSWORD', 'yacs@rpi')

# App Settings
APP_DEBUG_MODE=os.getenv('APP_DEBUG_MODE', True)
APP_HOST="0.0.0.0"

# Email SMTP Settings (Currently not in use)
mail_host="smtp.XXX.com"
mail_user="XXXX"
mail_pass="XXXXXX"
