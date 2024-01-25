import platform
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, sys
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument('--max_temp', type=int, default=-1, help='set Max temp')
parser.add_argument('--crit_temp', type=int, default=-1, help='set Critical temp')
parser.add_argument('--wtc_name', type=str, default="FILL", help='set WTC name')
parser.add_argument('--sender', type=str, default="amartyaveer72@gmail.com", help='sender email')
parser.add_argument('--receiver', type=str, default=["FILL"], help='receiver email(s)')
parser.add_argument('--sendor_password', type=str, default="FILL", help='sender password')
parser.add_argument('--email_server', type=str, default="smtp.gmail.com:587", help='email server')
parser.add_argument('--log_location', type=str, default=None, help='full path to log folder')

def get_cpu_temperature():
    if system == "Linux":
        try:
            sensors = list(map(float, os.popen("sensors | grep '^Core' | awk '{print $3}' | sed 's/+//; s/°C//' | sort -rn | head -5").read().splitlines()))
            return sum(sensors)/len(sensors)
           
        except Exception as e:
            return None
        
def get_gpu_processes():
    try:
        # Run nvidia-smi command and capture its output and extract process ids
        gpu_processes = list(map(int, os.popen('nvidia-smi --query-compute-apps=pid --format=csv,noheader,nounits').read().splitlines()))
        return gpu_processes

    except Exception as e:
        return []

def kill_gpu_processes():
    try:
        # Get GPU processes
        gpu_processes = get_gpu_processes()
        # Kill all GPU processes
        for pid in gpu_processes:
            os.system(f"kill -9 {pid}")

    except Exception as e:
        logging.info(f"Error while killing GPU processes: {e}")
        
        
        
def send_mail(temp):

    subject = "WARNING: SERVER TEMPS!"
    body = f"{args.wtc_name} temp have exceeded {args.max_temp}\nCurrent temp: {temp}\nPlease check the server immediately!"

    # Email sending code
    msg = MIMEMultipart()
    msg['From'] = args.sender
    msg['To'] = " ".join(args.receiver)
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    try:
        server = smtplib.SMTP(args.email_server)
        server.starttls()
        server.login(args.sender, args.sendor_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.info(f"Failed to send email. Error: {e}")


if __name__ == "__main__":
    
    args = parser.parse_args()
    system = platform.system()

    handlers = [logging.StreamHandler()]
    
    if args.log_location is not None:
        handlers = handlers + [logging.FileHandler(os.path.join(args.log_location, "debug.log"))]
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
    logging.info("Setup 'max_temp, crit_temp, wtc_name, receiver' and remove this this line and exit after!")
    exit()

    cpu_temperature = get_cpu_temperature()
    logging.info(f'cpu_temperature: {cpu_temperature}')
    if cpu_temperature is not None and cpu_temperature > args.max_temp:
        send_mail(cpu_temperature)
    
    if cpu_temperature is not None and cpu_temperature > args.crit_temp:
       kill_gpu_processes()
