import requests
from datetime import datetime
import pytz

class EconomicCalendarScraper:
    def __init__(self, url, local_timezone='Africa/Johannesburg'):
        self.url = url
        self.local_timezone = local_timezone

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch data from the URL")

    def filter_events(self, data):
        us_high_impact_events = []
        for event in data:
            if event['country'] == 'USD' and event['impact'] == 'High':
                us_high_impact_events.append({
                    'title': event['title'],
                    'date': event['date'],
                    'impact': event['impact'],
                    'previous': event.get('previous', 'N/A'),
                    'forecast': event.get('forecast', 'N/A')
                })
        return us_high_impact_events

    def convert_to_local_time(self, date_str):
        utc_time = datetime.fromisoformat(date_str.replace('Z', '+02:00'))
        local_timezone = pytz.timezone(self.local_timezone)
        local_time = utc_time.astimezone(local_timezone)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')

    def display_events(self, events):
        current_time = datetime.now(pytz.timezone(self.local_timezone)).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Current Time: {current_time}\n")
        for event in events:
            event_time = self.convert_to_local_time(event['date'])
            print(f"Event: {event['title']}, Date and Time: {event_time}, Impact: {event['impact']}")
            print(f"Previous: {event['previous']}, Forecast: {event['forecast']}\n")

    def run(self):
        data = self.fetch_data()
        us_high_impact_events = self.filter_events(data)
        self.display_events(us_high_impact_events)

if __name__ == "__main__":
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    scraper = EconomicCalendarScraper(url, local_timezone='Africa/Johannesburg')
    scraper.run()
