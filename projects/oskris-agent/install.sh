#!/bin/bash
# OskrisAgent - One-click installer
# Run on VPS: chmod +x install.sh && ./install.sh

set -e

echo "🤖 OskrisAgent Installer"
echo "========================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

INSTALL_DIR="/opt/oskris-agent"

# Step 1: System dependencies
echo -e "${YELLOW}[1/5] Installing system dependencies...${NC}"
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv git > /dev/null 2>&1
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Step 2: Setup directory
echo -e "${YELLOW}[2/5] Setting up project...${NC}"
if [ ! -d "$INSTALL_DIR" ]; then
    mkdir -p "$INSTALL_DIR"
fi

# Copy files if running from a different directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ "$SCRIPT_DIR" != "$INSTALL_DIR" ]; then
    cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/.env.example "$INSTALL_DIR/" 2>/dev/null || true
fi

cd "$INSTALL_DIR"
echo -e "${GREEN}✅ Project directory ready${NC}"

# Step 3: Python virtual environment
echo -e "${YELLOW}[3/5] Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install python-telegram-bot anthropic aiohttp psutil -q
echo -e "${GREEN}✅ Python packages installed${NC}"

# Step 4: Configuration
echo -e "${YELLOW}[4/5] Configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${RED}⚠️  Please edit .env with your credentials:${NC}"
    echo "   nano $INSTALL_DIR/.env"
    echo ""
    echo "   Required:"
    echo "   - TELEGRAM_BOT_TOKEN (from @BotFather)"
    echo "   - OWNER_TELEGRAM_ID (from @userinfobot)"
    echo "   - ANTHROPIC_API_KEY"
else
    echo -e "${GREEN}✅ .env already exists${NC}"
fi

# Step 5: Systemd service
echo -e "${YELLOW}[5/5] Setting up systemd service...${NC}"

cat > /etc/systemd/system/oskris-agent.service << EOF
[Unit]
Description=OskrisAgent - Personal AI Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python bot.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable oskris-agent
echo -e "${GREEN}✅ Systemd service created${NC}"

echo ""
echo "========================"
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Edit config:     nano $INSTALL_DIR/.env"
echo "  2. Start the bot:   systemctl start oskris-agent"
echo "  3. Check status:    systemctl status oskris-agent"
echo "  4. View logs:       journalctl -u oskris-agent -f"
echo ""
echo "Quick commands:"
echo "  systemctl restart oskris-agent  # Restart"
echo "  systemctl stop oskris-agent     # Stop"
echo ""
