# voting-on-the-blockchain
 
## About
SecureVote is a flask application, interacting with NaiveChain to host a voting platform which supports registration, verification, casting a ballot, viewing cast ballots, and viewing registered voters.

## Installation
To start using SecureVote, first navigate to “naivechain-master/” in your terminal and run the commands,

`docker-compose up`

This will start NaiveChain on a local port and let SecureVote interact with it. Next, start SecureVote by navigating to the root folder of the project and running

`python3 app.py`

You may be prompted to install some modules, in that case run

`pip3 install requests`

`pip3 install flask`

Now SecureVote is ready to be used. Navigate to the address and port which it is being run on.


## Use
If we navigate to /voters, we’ll see everyone that’s registered and is able to vote. By default, this is populated with a single person. We also see the percentage of registered voters which have voted below.
   
Say we want to add a voter, we’ll navigate to the root of the webpage (/).
And click the button in the top right corner (+). This brings us to the Add Voter page.

Where voter details can be populated. The exact details must be used again when checking your ID to vote, so make sure to remember them.

After completing registration and submitting, your profile is now added to the /voters page and grants you the access to vote.

Fill in your details again and submit.
  
Now you will be presented with the candidate selection page.

Select a candidate from the four different colours and submit to place your vote.
Your ballot is now cast and your (anonymous) vote can be seen on the /ballots page.
Each voter is given only one vote and only registered voters are able to vote.
The /voters page will also update to display the new vote which was placed.
