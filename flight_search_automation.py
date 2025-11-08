from playwright.sync_api import sync_playwright
from datetime import datetime
import json


def scrape_flights(origin: str, destination: str, journey_date: str):
    """Scrape live flight data from budgetticket.in (no hardcoded data)."""
    flights = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        page.goto("https://www.budgetticket.in", timeout=60000)
        page.wait_for_load_state("networkidle")

        # --- Fill origin, destination, and date fields dynamically ---
        # Adjust selectors based on the site's actual structure.
        page.click("input[placeholder*='From']")        # open 'From' dropdown
        page.keyboard.type(origin)
        page.keyboard.press("Enter")

        page.click("input[placeholder*='To']")          # open 'To' dropdown
        page.keyboard.type(destination)
        page.keyboard.press("Enter")

        page.click("input[type='date'], input[placeholder*='Date']")  # date picker
        page.fill("input[type='date'], input[placeholder*='Date']", journey_date)
        page.keyboard.press("Enter")

        # Click the search button
        page.click("button:has-text('Search')")

        print("🔎 Waiting for flight results...")
        page.wait_for_load_state("networkidle")

        # --- Extract all visible flight results dynamically ---
        page.wait_for_selector("div.flight-item, .flight-result", timeout=60000)
        cards = page.query_selector_all("div.flight-item, .flight-result")
        print(f"✅ Found {len(cards)} flight elements.")

        for card in cards:
            try:
                airline = card.query_selector(".airline-name, .name, .carrier").inner_text()
                flight_no = card.query_selector(".flight-number, .code").inner_text()
                dep = card.query_selector(".departure-time, .depart, .time").inner_text()
                arr = card.query_selector(".arrival-time, .arrival, .arrive").inner_text()
                price = card.query_selector(".price, .fare, .amount").inner_text()

                flights.append({
                    "airline": airline,
                    "flight_number": flight_no,
                    "departure": dep,
                    "arrival": arr,
                    "price": price,
                    "origin": origin,
                    "destination": destination,
                    "searchdatetime": datetime.utcnow().isoformat() + "Z"
                })
            except Exception:
                continue

        browser.close()

    # Save results to JSON file
    with open("flight_results.json", "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=2, ensure_ascii=False)
    print(f"📝 Saved {len(flights)} flights → flight_results.json")
    return flights


if __name__ == "__main__":
    scrape_flights("Bangalore", "Delhi", "2025-11-18")
