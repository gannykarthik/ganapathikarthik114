

from fastapi import FastAPI
from flight_search_automation import scrape_flights

app = FastAPI(
    title="TripGain Flight Search API",
    description="FastAPI endpoint that runs Playwright (visible browser) to scrape flights.",
    version="2.0"
)

@app.get("/flight-search")
def flight_search(origin: str, destination: str, journey_date: str):
    """
    Endpoint example:
    GET /flight-search?origin=Bangalore&destination=Delhi&journey_date=2025-11-18
    """
    flights = scrape_flights(origin, destination, journey_date)
    return {
        "total_flights": len(flights),
        "flights": flights
    }
