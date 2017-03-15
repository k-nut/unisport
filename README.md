# unisport.berlin
The goal of this project is to make the unisport classes in Berlin searchable in one central place.
It consists of three parts: the scrapers that get the data (from the unisport portals of Beuth, htw, HU, FU, TU), the backend that provides the collected data and makes it queryable, and the frontend that makes the data accessible.

IMPORTANY NOTE: When developing this I did not put very much though into making this flexible/redeployable. It might might behave weird at a lot of points but it should serve as a proof of concept. If you have any questions do not hesitate to contact me!

## Scrapers
If you want to run the scrapers you need to have scrapy installed (which is not compatible with python3 which is 
used in the rest of the project so this needs to be handled separately).

If you have it installed you can run `dotenv sh scrapers/run_all.sh`

After that you will have a file called `alle.json` in the data folder that you specified in you `.env` which contains all
the collected data. You need to import this by running `dotenv python backend/import.py`. For this you now need to be in the python3 virtualenv with the requirements as described in the next part.


## Backend
The backend development is done in python3.
The following assumes that you are in the `backend` folder.
First copy the `dotenv.example` file to `.env` and set the proper path to the `test.db` file.

The install the requirements via `pip install -r requirements.txt`. You then should be able to run `dotenv python test.py` and see that the tests pass.

## Frontend
The frontend runs completely on its own you just need to set the correct `BACKEND_URL` in the `app.js`.
Then you can for example start it by `cd`ing to the `frontend` directory and running `python3 -m http.server` which will start a local development server
