# Raspberry Pi Deployment Guide for MBHB

## Overview

This guide provides instructions for deploying the MBHB (Math Breakthrough Builder) system on a Raspberry Pi named **"fridge"** that is already running the AITGChatBot homework data collection system.

## Machine-Specific Configuration

**Important**: This deployment is configured for your specific Raspberry Pi setup:
- **Machine Name**: `fridge` (hostname)
- **Port**: `8050` (chosen to avoid conflicts with existing services)
- **Data Source**: `/opt/AITGChatBot/data/5289364296`
- **Access URLs**: 
  - Local: `http://localhost:8050`
  - Network: `http://fridge:8050` or `http://fridge.local:8050`

**Why Port 8050?** Port 5000 and other common ports are likely already in use by other services on fridge. Port 8050 provides a conflict-free alternative while being easy to remember.

## System Integration

The MBHB system integrates with existing homework data collection on **fridge** at:
- **Machine Name**: fridge
- **Data Location**: `/opt/AITGChatBot/data/5289364296`
- **Data Format**: Chat text files + user images (homework) + assistant images (marked corrections)
- **MBHB Port**: 8050 (avoids conflicts with other services)

### Current Data Structure

```
/opt/AITGChatBot/data/5289364296/
├── chat_2025-12-19T13-03-39.txt          # Chat log with timestamps
├── image_2025-12-19T13-03-39_user.jpg     # Student's homework image
└── image_2025-12-19T13-05-10_assistant.png # AI-marked corrections
```

## Prerequisites

### System Requirements
- Raspberry Pi 3B+ or newer (4GB RAM recommended)
- Raspbian OS (Bullseye or newer)
- Python 3.9 or higher
- Node.js 16 or higher
- 2GB free disk space
- Existing AITGChatBot installation at `/opt/AITGChatBot`

### Check Current Setup
```bash
# Verify existing data collection
ls -la /opt/AITGChatBot/data/5289364296/

# Check Python version
python3 --version

# Check Node.js version
node --version

# Check available disk space
df -h
```

## Installation Steps

### 1. Clone Repository

```bash
cd /opt
sudo git clone https://github.com/raymondclowe/MBHB.git
cd MBHB
sudo chown -R chatbotuser:chatbotuser /opt/MBHB
```

### 2. Install Python Dependencies

```bash
cd /opt/MBHB

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies

```bash
npm install
```

### 4. Configure Environment

Create configuration file:

```bash
sudo nano /opt/MBHB/.env
```

Add the following:

```bash
# OpenRouter API Key
OPENROUTER_API_KEY=your-api-key-here

# Flask Configuration
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:////opt/MBHB/mbhb.db

# Homework folder (link to existing data)
HOMEWORK_FOLDER=/opt/MBHB/homework_submissions

# Worksheet output
WORKSHEET_FOLDER=/opt/MBHB/generated_worksheets

# Port configuration (using 8050 to avoid conflicts)
PORT=8050
```

**Generate a secure secret key:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Create Symbolic Link to Existing Data

Link the existing AITGChatBot data to MBHB's homework folder:

```bash
# Create a processing script to convert existing data
sudo mkdir -p /opt/MBHB/scripts
sudo nano /opt/MBHB/scripts/process_aitg_data.py
```

Add the converter script (see below).

### 6. Initialize Database

```bash
source venv/bin/activate
python3 run.py &
sleep 5
kill %1  # Stop after database initialization

# Verify database was created
ls -la mbhb.db
```

### 7. Set Up Systemd Services

Create MBHB Flask service:

```bash
sudo nano /etc/systemd/system/mbhb-web.service
```

Add:

```ini
[Unit]
Description=MBHB Flask Web Application
After=network.target

[Service]
Type=simple
User=chatbotuser
Group=chatbotuser
WorkingDirectory=/opt/MBHB
Environment="PATH=/opt/MBHB/venv/bin"
EnvironmentFile=/opt/MBHB/.env
ExecStart=/opt/MBHB/venv/bin/python3 /opt/MBHB/run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Create MBHB File Monitor service:

```bash
sudo nano /etc/systemd/system/mbhb-monitor.service
```

Add:

```ini
[Unit]
Description=MBHB Homework File Monitor
After=network.target mbhb-web.service

[Service]
Type=simple
User=chatbotuser
Group=chatbotuser
WorkingDirectory=/opt/MBHB
Environment="PATH=/opt/MBHB/venv/bin"
EnvironmentFile=/opt/MBHB/.env
ExecStart=/opt/MBHB/venv/bin/python3 /opt/MBHB/monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start services:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mbhb-web
sudo systemctl enable mbhb-monitor
sudo systemctl start mbhb-web
sudo systemctl start mbhb-monitor
```

Check status:

```bash
sudo systemctl status mbhb-web
sudo systemctl status mbhb-monitor
```

### 8. Configure Nginx Reverse Proxy (Optional)

If you want to access MBHB on port 80:

```bash
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/mbhb
```

Add:

```nginx
server {
    listen 80;
    server_name fridge.local fridge;

    location /mbhb {
        proxy_pass http://localhost:8050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Note**: This configuration makes MBHB available at `http://fridge/mbhb` to avoid conflicts with other services.

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/mbhb /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Data Integration Scripts

### AITGChatBot Data Processor

Create `/opt/MBHB/scripts/process_aitg_data.py`:

```python
#!/usr/bin/env python3
"""
Process AITGChatBot data and convert to MBHB format
Monitors /opt/AITGChatBot/data/5289364296 for new corrections
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

AITG_DATA_DIR = '/opt/AITGChatBot/data/5289364296'
MBHB_HOMEWORK_DIR = '/opt/MBHB/homework_submissions'

def extract_student_id_from_path():
    """Extract student ID from directory name"""
    return Path(AITG_DATA_DIR).name

def parse_chat_file(chat_file):
    """Parse chat file to extract timestamps and messages"""
    with open(chat_file, 'r') as f:
        content = f.read()
    
    # Extract date from filename
    match = re.search(r'chat_(\d{4}-\d{2}-\d{2})', chat_file)
    if match:
        date_str = match.group(1)
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    return date_str

def find_correction_image(chat_file):
    """Find the corresponding assistant correction image"""
    base_name = Path(chat_file).stem
    timestamp = base_name.replace('chat_', '')
    
    # Look for assistant image files around the same time
    data_dir = Path(chat_file).parent
    for img_file in data_dir.glob(f'image_*_assistant.png'):
        return str(img_file)
    
    return None

def convert_to_mbhb_format(chat_file, correction_image):
    """
    Convert AITGChatBot data to MBHB JSON format
    
    Note: This creates a placeholder JSON. In production, you would:
    1. Use OCR on the user image to extract questions
    2. Use Vision AI on the assistant image to extract corrections
    3. Parse the corrections to identify mistakes
    
    For now, creates a basic structure for manual review.
    """
    
    student_id = extract_student_id_from_path()
    homework_date = parse_chat_file(chat_file)
    
    # Create MBHB JSON structure
    data = {
        "student_id": student_id,
        "student_name": f"Student {student_id}",
        "homework_date": homework_date,
        "source": "AITGChatBot",
        "correction_image": correction_image,
        "questions": [
            {
                "question_number": 1,
                "topic": "Manual Review Required",
                "student_answer": "See original image",
                "correct_answer": "See correction image",
                "mistakes": [
                    {
                        "type": "manual_review",
                        "description": "Manual review required - check correction image",
                        "severity": "medium"
                    }
                ]
            }
        ],
        "notes": f"Converted from AITGChatBot. Review correction image: {correction_image}"
    }
    
    return data

def process_new_files():
    """Process new chat files and corrections"""
    
    processed_log = '/opt/MBHB/processed_aitg_files.txt'
    
    # Load already processed files
    processed = set()
    if os.path.exists(processed_log):
        with open(processed_log, 'r') as f:
            processed = set(line.strip() for line in f)
    
    # Find new chat files
    data_dir = Path(AITG_DATA_DIR)
    for chat_file in sorted(data_dir.glob('chat_*.txt')):
        chat_path = str(chat_file)
        
        if chat_path in processed:
            continue
        
        print(f"Processing: {chat_path}")
        
        # Find correction image
        correction_image = find_correction_image(chat_path)
        
        if correction_image:
            # Convert to MBHB format
            mbhb_data = convert_to_mbhb_format(chat_path, correction_image)
            
            # Save to homework_submissions
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{MBHB_HOMEWORK_DIR}/aitg_{timestamp}_{mbhb_data['student_id']}.json"
            
            os.makedirs(MBHB_HOMEWORK_DIR, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(mbhb_data, f, indent=2)
            
            print(f"  Created: {output_file}")
            print(f"  Note: Manual review required to extract actual mistakes from correction image")
            
            # Mark as processed
            with open(processed_log, 'a') as f:
                f.write(chat_path + '\n')
        else:
            print(f"  No correction image found, skipping")

if __name__ == '__main__':
    print("AITGChatBot Data Processor for MBHB")
    print("=" * 50)
    process_new_files()
    print("\nProcessing complete!")
```

Make it executable:

```bash
chmod +x /opt/MBHB/scripts/process_aitg_data.py
```

### Scheduled Processing

Add to crontab to process new data every 5 minutes:

```bash
sudo crontab -e -u chatbotuser
```

Add:

```
*/5 * * * * /opt/MBHB/venv/bin/python3 /opt/MBHB/scripts/process_aitg_data.py >> /var/log/mbhb_processor.log 2>&1
```

## Testing the Installation

### 1. Test Web Interface

```bash
# From the Raspberry Pi (fridge):
curl http://localhost:8050

# From any computer on the network:
curl http://fridge:8050
# or
curl http://fridge.local:8050

# Or open in browser:
http://fridge:8050
# or
http://fridge.local:8050
```

**Note**: Port 8050 is used to avoid conflicts with other services on fridge.

### 2. Test File Monitoring

```bash
# Create a test homework file
cat > /opt/MBHB/homework_submissions/test.json << 'EOF'
{
  "student_id": "TEST001",
  "homework_date": "2024-01-15",
  "questions": [{
    "question_number": 1,
    "student_answer": "x = 5",
    "correct_answer": "x = ±5",
    "mistakes": [{
      "type": "missing_negative_root",
      "description": "Forgot negative solution",
      "severity": "high"
    }]
  }]
}
EOF

# Check logs
sudo journalctl -u mbhb-monitor -f
```

### 3. Test AITGChatBot Integration

```bash
# Run the processor manually
source /opt/MBHB/venv/bin/activate
python3 /opt/MBHB/scripts/process_aitg_data.py

# Check if files were created
ls -la /opt/MBHB/homework_submissions/
```

## Maintenance

### View Logs

```bash
# Web application logs
sudo journalctl -u mbhb-web -f

# File monitor logs
sudo journalctl -u mbhb-monitor -f

# Data processor logs
tail -f /var/log/mbhb_processor.log
```

### Restart Services

```bash
sudo systemctl restart mbhb-web
sudo systemctl restart mbhb-monitor
```

### Backup Database

```bash
# Create backup
sudo cp /opt/MBHB/mbhb.db /opt/MBHB/backups/mbhb_$(date +%Y%m%d).db

# Automated daily backup (add to crontab)
0 2 * * * cp /opt/MBHB/mbhb.db /opt/MBHB/backups/mbhb_$(date +\%Y\%m\%d).db
```

### Update MBHB

```bash
cd /opt/MBHB
sudo -u chatbotuser git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
npm install
sudo systemctl restart mbhb-web mbhb-monitor
```

## Performance Optimization

### Raspberry Pi Specific

```bash
# Increase swap size for larger datasets
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Database Optimization

```bash
# For SQLite, enable WAL mode
sqlite3 /opt/MBHB/mbhb.db "PRAGMA journal_mode=WAL;"
```

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status mbhb-web

# Check for errors
sudo journalctl -u mbhb-web --no-pager

# Check permissions
ls -la /opt/MBHB/
```

### Database Locked

```bash
# Stop services
sudo systemctl stop mbhb-web mbhb-monitor

# Remove lock file
rm /opt/MBHB/mbhb.db-shm
rm /opt/MBHB/mbhb.db-wal

# Restart
sudo systemctl start mbhb-web mbhb-monitor
```

### Out of Memory

```bash
# Check memory usage
free -h

# Reduce Flask workers (edit mbhb-web.service)
# Add: Environment="FLASK_RUN_HOST=0.0.0.0"
# Add: Environment="FLASK_RUN_PORT=8050"
```

### Out of Memory

```bash
# Check memory usage
free -h

# Reduce Flask workers (edit mbhb-web.service)
# Add: Environment="FLASK_RUN_HOST=0.0.0.0"
# Add: Environment="FLASK_RUN_PORT=8050"
```

## Accessing the System

### From Local Network

```
http://fridge:8050
# or
http://fridge.local:8050
# or with IP address
http://192.168.x.x:8050
```

### From Internet (with port forwarding)

1. Configure port forwarding on router (external 8080 → internal 8050)
2. Use dynamic DNS (DuckDNS, No-IP)
3. **Important**: Add authentication before exposing to internet!

## Security Recommendations

1. **Change default passwords**
2. **Enable firewall**:
   ```bash
   sudo apt-get install ufw
   sudo ufw allow 22
   sudo ufw allow 8050
   sudo ufw enable
   ```
3. **Regular updates**:
   ```bash
   sudo apt-get update && sudo apt-get upgrade
   ```
4. **Monitor logs** for unusual activity
5. **Backup regularly**

## Support

For issues specific to:
- **MBHB**: Check GitHub issues
- **AITGChatBot integration**: Check existing setup at `/opt/AITGChatBot`
- **Raspberry Pi**: Check `/var/log/syslog`

## Next Steps

1. **Review data in admin panel**: http://fridge:8050 or http://fridge.local:8050
2. **Add students** via web interface
3. **Monitor automatic homework processing** (check logs: `sudo journalctl -u mbhb-monitor -f`)
4. **Review and manually categorize** initial mistakes
5. **Generate first worksheets** based on student performance

## Quick Reference

**Access URLs**:
- From fridge: http://localhost:8050
- From local network: http://fridge:8050 or http://fridge.local:8050
- With Nginx: http://fridge/mbhb

**Service Management**:
```bash
# Check status
sudo systemctl status mbhb-web
sudo systemctl status mbhb-monitor

# Restart
sudo systemctl restart mbhb-web mbhb-monitor

# View logs
sudo journalctl -u mbhb-web -f
sudo journalctl -u mbhb-monitor -f
```

**Important Files**:
- Configuration: `/opt/MBHB/.env`
- Database: `/opt/MBHB/mbhb.db`
- Homework data: `/opt/AITGChatBot/data/5289364296/`
- Generated worksheets: `/opt/MBHB/generated_worksheets/`
- Logs: `/var/log/mbhb_processor.log`
6. Track student progress
