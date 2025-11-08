# flight_search_api.py
# -------------------------------------------------------
# FastAPI endpoint wrapping the mock flight scraper
# -------------------------------------------------------

from fastapi import FastAPI
from flight_search_automation import scrape_flights

app = FastAPI(
    title="TripGain Flight Search API",
    description="Mock FastAPI implementation returning flight search results.",
    version="1.0.0"
)

@app.get("/flight-search")
def search_flights(origin: str, destination: str, journey_date: str = "2025-11-18"):
    """
    Simulated endpoint that returns mock flight data.
    Parameters:
        origin (str): departure city
        destination (str): arrival city
        journey_date (str): YYYY-MM-DD format (default 2025-11-18)
    """
    flights = scrape_flights(origin, destination, journey_date)
    return {
        "total_flights": len(flights),
        "flights": flights
    }
