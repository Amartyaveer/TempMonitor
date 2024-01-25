# TempMonitor
Have to change the parameter having ##### in comments in the code. <br />
Add the email in the receiver.txt file to get the email notification. Add each email in newline.<br />
Change the sender's email with your email and the password with the app password generated from the google account. Not your gmail password.<br />

Adding crontab<br />
*/duration_in_min * * * * python_path script_path<br />
*/3 * * * * /home/wtc13/anaconda3/bin/python /home1/Amartya/Temperature/temps.py<br />
