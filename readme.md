# Udacity FSND Project 2: Swiss Pairing Tournament

This is the second major project in Udacity's Full Stack Nanodegree Course which features lessons in psql and python.The aim is to create a database that keeps track of players, matches in a game tournament. A Swiss tournament system has a pairing system where players are not eliminated.  Everyone gets to play in each round, and players with the same or close to the same record (number of wins) are paired against each other to ensure competitiveness. 

---

## Getting Started

To run the SQL database server, you'll use a virtual machine (VM) which is a Linux system server that runs on top of your own machine. You can fork and clone the VM configuration from the repository <https://github.com/alanbarretto/swiss-tournament/tree/master/FSND-Virtual-Machine>

Next, you will have to download Virtual Box from this link <https://www.virtualbox.org/wiki/Downloads>.  Virtual Box is the software the runs the virtual machine (VM). 
>Ubuntu users: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu >Software Center instead. Due to a reported bug, installing VirtualBox from the 
>site may uninstall other software you need.</small>

After that, you need to download Vagrant, which is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.<https://www.vagrantup.com/downloads.html> 

>Windows users: The Installer may ask you to grant network permissions to Vagrant 
>or make a firewall exception. Be sure to allow this.</small>

---

## How to Use

Using the terminal, cd to the directory containing the VM files.  Then, cd to the vagrant subdirectory.  From there, run the command `vagrant up`.  This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When it is done, you will get your shell prompt back.  This time, type `vagrant ssh` to log in to your newly installed Linux VM!

Once you get vagrant up, you need to navigate to the tournament directory by typing `cd /vagrant/tournament`

## Running the Tournament

Type `psql tournament` on the command line.  Then type `\i tournament.sql` to run the scripts in that file and create the tables.  

Exit the psql server by typing `\q`

Then, run the test by typing `python tournament_test.py`

---


## Expected Outcome

All the functions in the tournament.py are tested by the tournament_test.py.  If everything passes, the terminal will display the following:

1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.

- Success! All tests pass!