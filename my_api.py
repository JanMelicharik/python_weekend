from fastapi import FastAPI
from src.modules import regiojet

app = FastAPI()


@app.get("/search_rj/")
def flights(origin, destination, date):
    rj = regiojet.Scraper(origin, destination, date)
    return rj.get_results()
