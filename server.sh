!/bin/bash

echo "Setting up system..."
sudo apt-get update
echo "Updating..."
sudo apt-get install apache2
echo "Installed apache2."
sudo apt-get install libapache2-mod-wsgi
echo "Installed wsgi module for apache2."
sudo apt-get install mysql-server
echo "Installed mySQL-server."
sudo apt-get install libmysqlclient-dev
echo "Installed libmysqlclient-dev"

sudo apt-get install python-pip
echo "Installed pip."
sudo pip install flask
echo "Installed flask."
sudo pip install MySQL-python
echo "Installed MySQL-python."
sudo pip install PyMySQL 
echo "Installed PyMySQL."
sudo pip install flask-bcrypt
echo "Installed flask-bcrypt."

SNAKE='chainsnakers'
mkdir ~/$SNAKE
echo "Made directory $SNAKE"
sudo ln -sT ~/$SNAKE /var/www/html/$SNAKE
echo "Linked dir $SNAKE to /var/www/html."
echo "Setup complete!"