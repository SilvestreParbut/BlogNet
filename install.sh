#!/bin/bash
set -e

echo "Installing BlogNet..."

# 1. Install system dependencies
sudo apt update
sudo apt install -y python3 python3-venv python3-tk git

# 2. Clone the repository to /opt/blognet
sudo mkdir -p /opt/blognet
sudo chown $USER /opt/blognet

if [ -d "/opt/blognet/.git" ]; then
    cd /opt/blognet && git pull
else
    git clone https://github.com/SilvestreParbut/blognet.git /opt/blognet
    cd /opt/blognet
fi

# 3. Set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install librats Pillow ebooklib

# 4. Create the executable launcher
sudo tee /usr/local/bin/blognet > /dev/null << 'EOF'
#!/bin/bash
cd /opt/blognet
source .venv/bin/activate
python3 blog_p2p_gui.py "$@"
EOF
sudo chmod +x /usr/local/bin/blognet

echo "Success! You can now run 'blognet' from anywhere."
