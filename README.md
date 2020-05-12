# six-min
A 6 Nimmit clone for Python using client/server architecture supports up to 10 players.

# Requirements
* Pandas
* Pickles

# Installation
Due to the way the data structures are implemented, primarily Pickles, the client and server need to be run out of the same directory.

# Deployment Tips
This is a command line game without a graphic user interface.  It is old school.

To install, I suggest adding a basic AWS EC2 instance.  You will need to add a security group to open port 4200 as well as 8139 to match the port that the client/server uses in 6 Minute.

If you choose to install Ubuntu, it will already have Python3. All you'll ned to do is install Pandas.  I also recommend you install shellinabox then you can play with friends through a web browser after they log in.

One last idea, you can either use AWS CloudFormation or crontab in the EC2 instance to start the server on reboot.
