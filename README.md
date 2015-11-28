#unisport.berlin

The goal of this project is to make the unisport classes in Berlin searchable in one central place.
It consists of three parts: the scrapers that get the data, the backend that provides the collected data and the frontend that can be used to make queries to the data.


##Scrapers


##Backend
The backend development is done in python3.
The following assumes that you are in the `backend` folder.
First copy the `dotenv.example` file to `.env` and set the proper path to the `test.db` file.

The install the requirements via `pip install -r requirements.txt`. You then should be able to run `dotenv python test.py` and see that the tests pass.
