#!/usr/bin/env bash
# Setting up my web server for the deployment of Book-Hub

#install Nginx
sudo apt-get update
sudo apt-get install -y nginx

#create folders
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# Creating a fake html file for testing
echo "<html>
  <head>
  </head>
  <body>
    BookHub Portfolio Project
  </body>
  </html>" >> /data/web_static/releases/test/index.html

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user
sudo chown -R ubuntu:ubuntu /data/

#Update nginx
sudo sed -i "261 \\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

# Restart nginx to apply chandes
sudo service nginx restart
