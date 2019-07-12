# GITHUB ISSUES THERMAL PRINTER 

This project will allow  your raspberry pi with a thermal printer to print ,independently, a little receipt for every new issue open in one of your github's repository. The recepit will contain  title, repository, qrcode of the web page and number of the new issue open.
My set up is a Mini Thermal Receipt Printer and a raspberry pi 3 with raspbian.

# Connect and configure the thermal printer 

The first things to do is to connect and configure the thermal printer with the raspberry 3. So download and  install the latest version of raspbian on your raspberry. Now we have to change some setting, working from therminal run :
```
sudo raspi-config
```
In the configuration menu go to  "Interfacing Options” select “Serial ”. Turn OFF the login hell over serial, and ENABLE the hardware serial port (No and yes respectively). Then reboot(type ' sudo reboot ')
Now with  F-M jumper wires connect the thermal printer with the raspberry, the first GND to the pin  number 14, VH to the pin 02 ,now the green light on the thermal printer should flash. The other GND to the pin 06 and respectively the  RX and the TX to the pin number 08 and 10 (RX on the printer to TXD on the Pi, the TX pin on the printer connects to RXD on the Pi).
Now if you have done everythings in the right way it's enought to type on the terminal of the raspberry:
```
stty -F /dev/serial0 19200
echo -e "This is a test.\\n\\n\\n" > /dev/serial0
```
This should print 'This is a test.'
Now that the printer work, you have to install some packages and to change some settings then can start ther real work.
Install several packages ...
```
sudo apt-get update
sudo apt-get install libcups2-dev libcupsimage2-dev git build-essential cups system-config-printer
```
This might take a few minutes.
When it's done, download and install this thermal printer's filter of CUPS:
```
git clone https://github.com/adafruit/zj-58
cd zj-58
make
sudo ./install
```
Now in order to link the  printer with your raspberry type :
```
sudo usermod -a -G lpadmin pi
```
and change the file /etc/cups/cupsd.conf with :
```
sudo nano /etc/cups/cupsd.conf
```
inside the file, in the section 
```
# Only listen for connections from the local machine
Listen localhost:631
```
with the '#' comment out Liste localhost:631 and add:
```
# Only listen for connections from the local machine
# Listen localhost:631
Port 631
```
now scroll down  until reach 'location ' then in this section add the lines that miss in your file
```
    < Location / >
    # Restrict access to the server...
    Order allow,deny
    Allow @local
    < /Location >

    < Location /admin >
    # Restrict access to the admin pages...
    Order allow,deny
    Allow @local
    < /Location >

    < Location /admin/conf >
    AuthType Default
    Require user @SYSTEM

    # Restrict access to the configuration files...
    Order allow,deny
    Allow @local
    < /Location >
```
 You’ll need to restart the CUPS server. Type the command:
 ```
 sudo /etc/init.d/cups restart
 ```
 Once that you have restarted cups , by any computer you should access to the administration panel by going with the browser to  http://[the Pi’s IP or hostname]:631
When the page is open click on 'Administration'.
In the Administration panel click on 'add printer', then should appear a windows that ask to enter username and password.
Once loggin a list of discovered printers will be presented , select your, probably is the first, and click 'continue'.
Now you can edit the name, location and desccription of the printer,as name use 'thermalprinter', and let 'share this printer' unchecked.
Then you'll be prompt to select the specific driver you want to use for your printer, it's the last name select it , and click to 'add printer', the last configuration are some general print setting , click on 'set default option', and you'll be present to the administration page. Click on maintenance and select print test, now the thermal printer should print a test page with a logo.

For more information see: 
https://learn.adafruit.com/networked-thermal-printer-using-cups-and-raspberry-pi/connect-and-configure-printer
https://www.howtogeek.com/169679/how-to-add-a-printer-to-your-raspberry-pi-or-other-linux-computer/ 

# Python script
To access to your github account and print the issue's information you'll need a python code, so first of all install python 3.7.0 or higher and set it as default, now you'll need your git-hub api token for the API , do  the same thing for the bitly API so create an account if you haven't one yet and copy your personal  token.
Clone this github repository using git :
```
git clone https://github.com/filippofiocchi/github-issue-thermal-printer.git
```
Now before create the database, you have to set an environment variable with the name of your database, to do that run :
```
export DATABASE_NAME='the name of your database'
 ```
To set it permanently for all future bash sessions add such line to your .bashrc file in your $HOME directory.
Use "cd github-issue-thermal-printer directory"  and here run :
 ```
 sudo python database.py    
```
Always in this direcotry modify the run.sh file with nano, you have to set some variable , 2 with the tokens of the github and bitly API and one again with the name of your database.
 ```
export TOKEN_GITHUB='your github token'
export TOKEN_BITLY='your bitlytoken'
export DATABASE_NAME='the name of your database'
 ```
Install a library of python :
 ```
pip3 install subprocess.run
 ```
Then run the run.sh file
 ```
./run.sh
 ```
and if you have some open issues in your repository it will print the receipt with the informations. If everythings work, make the program automatic by using crontab (usually yet installed in raspbian) :
```
crontab -e
```
and at the end of the file add the line :
 ```
 */10 * * * * /home/pi/github-issue-thermal-printer/run.sh
 
 ```
remember to leave a new line at the end and save, now the raspberry will run the python script printer.py every 10  minutes.
