#!/usr/bin/env bash
# sets up my web servers for the deployment of web_static

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get install -y nginx

# Create folders if not already exists
sudo mkdir -p /data/BookHub/shared/
sudo mkdir -p /data/BookHub/releases/test/

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    BookHub Portfolio Project
  </body>
</html>" >> /data/BookHub/releases/test/index.html

# Create & recreate a symbolic link
sudo ln -sf /data/BookHub/releases/test/ /data/BookHub/current

# Give ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# update Nginx config to serve /data/BookHub/current at /hbnb_static/
sudo sed -i "26i \\\tlocation /hbnb_static/ {\n\t\talias /data/BookHub/current/;\n\t}\n" /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart
