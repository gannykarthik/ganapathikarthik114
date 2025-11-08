

from datetime import datetime
import json

def scrape_flights(origin, destination, date):
    """
    Simulated flight scraping function.
    Returns mock flight data matching TripGain's expected format.
    """
    flights = [
        {
            "airline": "IndiGo",
            "flight_number": "6E-123",
            "departure": "06:30",
            "arrival": "09:10",
            "price": "₹5,450",
            "origin": origin,
            "destination": destination,
            "searchdatetime": datetime.utcnow().isoformat() + "Z"
        },
        {
            "airline": "Air India",
            "flight_number": "AI-504",
            "departure": "07:15",
            "arrival": "09:55",
            "price": "₹6,120",
            "origin": origin,
            "destination": destination,
            "searchdatetime": datetime.utcnow().isoformat() + "Z"
        },
        {
            "airline": "Vistara",
            "flight_number": "UK-811",
            "departure": "08:20",
            "arrival": "10:55",
            "price": "₹6,780",
            "origin": origin,
            "destination": destination,
            "searchdatetime": datetime.utcnow().isoformat() + "Z"
        },
        {
            "airline": "SpiceJet",
            "flight_number": "SG-312",
            "departure": "09:10",
            "arrival": "11:45",
            "price": "₹5,950",
            "origin": origin,
            "destination": destination,
            "searchdatetime": datetime.utcnow().isoformat() + "Z"
        },
        {
            "airline": "Akasa Air",
            "flight_number": "QP-207",
            "departure": "10:00",
            "arrival": "12:40",
            "price": "₹6,050",
            "origin": origin,
            "destination": destination,
            "searchdatetime": datetime.utcnow().isoformat() + "Z"
        }
    ]

    with open("flight_results.json", "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=2, ensure_ascii=False)

    print(f"✅ Mock scraped {len(flights)} flights successfully.")
    return flights


if __name__ == "__main__":
    results = scrape_flights("Bangalore", "Delhi", "2025-11-18")
    print(json.dumps(results, indent=2, ensure_ascii=False))

