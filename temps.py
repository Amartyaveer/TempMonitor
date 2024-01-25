import platform
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
system = platform.system()
max_temp = 62   #####
crit_temp = 70  #####
wtc_name = 'WTC13' #####
sender = "amartyaveer72@gmail.com"
password = "*********" ######
receivers_email = '/home1/Amartya/Temperature/receiver.txt'  #####

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
        print(f"Error while killing GPU processes: {e}")
        
        
def send_mail(temp):
    emailServer = "smtp.gmail.com:587"

    # Replace receiver with the email address where you want to send the message
    receivers = os.popen(f'cat {receivers_email}').read().splitlines() #####
    subject = "WARNING: SERVER TEMPS!"
    body = f"{wtc_name} temp have exceeded {max_temp}\nCurrent temp: {temp}\nPlease check the server immediately!"

    # Email sending code
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = " ".join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    try:
        server = smtplib.SMTP(emailServer)
        server.starttls()
        server.login(sender, password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")


if __name__ == "__main__":
    cpu_temperature = get_cpu_temperature()
    print('cpu_temperature', cpu_temperature)
    if cpu_temperature is not None and cpu_temperature > max_temp:
        send_mail(cpu_temperature)
    
    if cpu_temperature is not None and cpu_temperature > crit_temp:
        kill_gpu_processes()
