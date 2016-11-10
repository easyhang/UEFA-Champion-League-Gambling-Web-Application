# UEFA-Champion-League-Gambling-Web-Application
Abstract
Our project is called ‘Europe Championship Gambling Online’. We will post information about EUFA Season 2015-2016, including team match information and its odds (win:draw:lose) for the host and the visitor. User can Registrar into our website and participate in the gambling. All data created by users will be recorded. We use MySQL to implement the backend database, Django rest framework for connecting the frontend and backend, and HTML/CSS/Javascript for designing our front web pages.

Introduction
Basic functions of our system
	Users can query the information of each team and their players
	Users can have a look at the match information of those teams
	Users can wager for upcoming matches, once the result is posted into database, they can get their money or lose it. 
	Super user has the right to check any info in our system.
Use cases that is realized
1. Common user registration
2. Log in for common user
3. Common user check its own personal info.
4. Log out for common user
5. The super user’s log in and log out
6. Search for team information by key words or characters
7. Query player’s information
8. Go through the match list for games.
9. Common user’s wager
10. Super user can add money to common users’ accounts.
11. Balancing accounts based on results of corresponding matchs.
12. Super user can query all wager info of common users.

Requirements
The actors that make use of the ECGO are general user, the registration accreditation, the gambling manager, the administer, information submitter, account manager.

	Common user registration
Step-by-Step Description:
1.	A user requests that a new registration authority be admitted.
2.	The system queues the request and informs the registrar.
3.	The registrar accredits the new registration authority and grants the registrar role to the requesting user.
4.	The system notifies the user that the request was accepted.

	Log in for common user
Step-by-Step Description:
1.	A user sends a login request
2.	The system queues the request and informs the account manager.
3.	The account manager queries database to find matched records of this user.
4.	The system accepts or reject the request and show results.

	Common user check its own personal info.
Step-by-Step Description:
1.	A user sends the request
2.	The system queries the database and return personal info.

	Log out for common user
Step-by-Step Description:
1.	A user sends a log out request
2.	The system accepts the request and return to previous homepage.

	The super user’s log in and log out
The same as the login and logout for common user

	Search for team information by key words or characters
Step-by-Step Description:
1.	Any one, not just login users, type parts of teams’ key words.
2.	The system receives the info and return team information.

	Query player’s information
Step-by-Step Description:
1.	Guest (not just users) click on the super link of certain team. 
2.	The system receives the info and return player information of certain team.

	Go through the match list for games 
When anyone queries for team info on front page, game info of such team will be given. And when a user wants to wager, all match info of game will be given, which will be discussed letter.

	Common user’s wager
Step-by-Step Description:
1.	A user places stakes.
2.	The system notifies the Gamble Manager information of the stake.
3.	The Gamble Manager approves the request and save the information.
4.	The system notifies the Account Manager the amount of money the user gives
5.	The Account Manager remove the amount accordingly.

	Super user adding money to common users’ accounts.
Step-by-Step Description:
1.	The common user sends adding money request to the system.
2.	The system queues the request and sends information to super user, waits for response.
3.	Super user accepts the request and informs Account Manager.
4.	The Account Manager distributes specific amount of husky coins to the user’s account.
5.	The system notifies the user that the account is successfully recharged.

	Balancing accounts based on results of corresponding matchs.
Step-by-Step Description:
1.	The submitters got the latest match results and request to update the match table.
2.	The system updates the match results accordingly.
3.	The Gambling Manager notices the changes and notifies the system.
4.	The system get info calculates amount according to information in wager table.
5.	The system send request to Account Manager to change balances accordingly.
6.	The Account Manager change the balance of certain user.

	Super user can query all wager info of common users.
Step-by-Step Description:
1.	Super user require to check every info in database (by bunch of super links)
2.	The system accepts the request return information accordingly..

