## Steam Level Up Service

An app designed to level up steam accounts based on crafting new badges. It is usable only through the Python console.

## Project Status

This project is under development. Users can save up their current badges and inventory now. Booster packs can be opened giving the name of a game.

Future improvements and functionalities (those are out of date):

- [ ] Analysis of the current steam user level and what badges can be created to improve it
- [ ] Badges can be crafted through the app
- [ ] Redirection to browser pages in order to buy more cards
- [ ] Better UI and easy support for other languages
- [ ] Steam login made easy (currently users have to manually set login cookies in order to make it work)

## Setup instructions

### Python 3.9

Further python packages used are visible in requirements.txt

PostgreSQL is also used to store information. To set it up, look for the table's creation file in the folder called 'db'.

## Reflection

### Project Overview

The core of the app is a web crawler that was designed to "interact" with steam web pages as a regular browser client would do. Those interactions may be an ETL pipeline used to scrap some useful information or may perform some other task. Given the initial intent of making a series of pipelines, this core is inside the 'etl_pipelines' folder, which will be renamed to a more well suited name in the future. 

Under this core layer of interactions we can find three other main components of the software, each having its own folder: 'web_crawlers', 'web_page_cleaning' and 'data_models'. The ETL pipeline design influence should be evident, but it's useful to write a few words to better understand each of those parts.

- 'web_crawlers' is where the extraction happens, it was reafactored to have only one external access point which emulates a very primitive REST api in its answer, although it's only a factory that returns web responses.

- 'web_page_cleaning' makes sense of the raw data that comes from thoses responses when needed, dealing with html or json content and returning vanilla python data types or collections.

- That data is then used to create objects defined by 'data_models', which are wrappers for pandas dataframes and methods related to the domain data contained in them. Each data_model may have a repository of its own to handle data persistence. The interaction with the dbitself and db table schemas are found in the 'db' folder. 

Above this layer we have a 'SteamUser' class that handles user related data, which must be always there since most of the interactions have to be executed by a loggedin steam user.

On top of all there's a simple presentation layer that allows one to interact with the software through the python console.

### Discussion

This is a side project developed to improve some of my software design skills. It was first thought as a series of ETL pipelines to gather some data from steam, but I realized that this data needed to fulfill some kind of well-defined task in order to be a meaningful exercise. I do not intend to make it a full-fledged app, but only a place where I can develop and work on some ideas.

I tried my best to use OOP and SOLID principles throughout my journey so far. This choice led me to slow development of new features in order to refactor what was already there to a better design, something I just reconsider at the work environment considering tight time schedules. But, as I said, it's a side project, and actively chose to do with it the best I could to learn, not just ship some code to a PR.
With that mindset, I reached some deadends and will probably continue to do so, but it's better to do it here than elsewhere. It's also notesworthy that this is my third attempt on this same project, but the first one published. The other two were victim of lack of version control (git saved me on that) and the other one lacked some basic security features that I found it best never to publish it (and create this new one instead).

When it comes to the project itself, I'm recently trying to find the time to improve it and/or add new features. The last update (a db schema migration) proved to be bigger than I thought, and now I plan to work on some small refactoring and slower feature plan/build in order to nor burn myself out. Soon I'll update this readme with a better project status that better reflects the current state of things.

