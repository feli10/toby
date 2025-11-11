Configure Launcher:
chmod +x /home/pi/Desktop/toby/launcher.py
sudo nano /etc/systemd/system/launcher.service

Paste this:
[Unit]
Description=Button toggle launcher for main.py
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/Desktop/toby/launcher.py
Restart=always
User=pi
WorkingDirectory=/home/pi/Desktop/toby

[Install]
WantedBy=multi-user.target

Enable it:
sudo systemctl daemon-reload
sudo systemctl enable launcher.service
sudo systemctl start launcher.service