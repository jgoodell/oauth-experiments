exec 2>&1
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sleep 3
sudo make install
sleep 3
sudo apt-get install -y emacs
sleep 3
sudo pip install -r /vagrant/requirements.txt
