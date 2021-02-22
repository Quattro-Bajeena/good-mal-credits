# ONGOING
- ~~hiding columns~~
- ~~squashing staffposition with the same person into one~~
- ~~figure out rate limiting when this will be on more than one threads on a server~~

- long term: pull data from other sites

- making sure logs from celery nginx and others are allright, logrotate is working corecntly
- clean up git more
- writing more unit tests, for database, celery and stuff

- use some kind of better css (sass?)
- page "about me"
- OOPS bug, the qick search only shows anime even though people or studios option is selected


# DONE:
- creator page
- loading page bar -> callbacks from update function
- good looks
- sorting
- better handling of checking if the data is in the database
- fix people searching
- good mechanism to save when the staff/person page was visited, and try to refresh the data after some time, and saves it every some time
- draw pages layouts
- update bar doesnt work so well fcking javascript
- watch out, there may be character listed in person roles, but the character page wont exist, wtf. this one is taken care of but there is a chace that this may happen to other stuff, maybe proof that
- redis set password later, security or sth
- ADD CHARCTER TABLE TO ANIME PAGE QUICKLY you have to redwoanlod all info about anime great you moron
- clear filters
- format number of members on pages
- filtering
- drop down filters for language, studio
- make tables not changes size when filtering (works for now, maybe will have to tweak it)
- add studio page
- footer with contact info
- rate limitng that is long, but doesnt limit single requsts like when searching
- dynamic searching
- hadnling exceptions and 404 erros
- database is locked can't visit other page while it's updating, becasue visitngf other page writes to it to register new page
- mysql database on server
- celery on server
- well, stuff just works on server, so nginx and uwsgi and redis
- connecting to databse through unix socket, quick
- when other error diferent than API error occurs task doesnt do cleanup? now everytig inside task in it try catch block
- duplicate quick search results, if there are less than max number of matches
- drop down dynamic search options are below progrss bar
- celery config (and app too) through JSON/YAML file, not .env
- set up your own logging system (not using app.logger, or celery loggers)
- weird stuttering of download progress bar at the beggining
- configuring logging to work well on server on flask itself
- inforamtion what anime is downalding right now
- like a admin panel to see what's in the que what's downlading right now, what percantge of all anime is downloaded
- do the main page so the searchbar will be in the centre