import datetime
import csv


class CSV:
    def __init__(self, file_name):
        self.file_name = f'{file_name}.csv'
        self.date = datetime.date.today()
        self.cache = {}
        self.used = False

    def export_to_csv(self):
        try:
            with open(self.file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Optionally write headers, adjust based on needs
                writer.writerow(['Ticker', 'Rate'])

                # Writing each ticker-rate pair from cache to the file
                for ticker, rate in self.cache.items():
                    writer.writerow([ticker, rate])
            print(f'Data exported successfully to {self.file_name}')
        except Exception as e:
            print(f"An error occurred while exporting: {e}")

    def import_from_csv(self):
        try:
            with open(self.file_name, mode='r', newline='') as file:
                reader = csv.reader(file)
                # Skip the header row if necessary
                next(reader)

                # Read each row and populate the cache
                for row in reader:
                    ticker, rate = row[0], row[1]
                    self.cache[ticker] = rate
            print(f'Data imported successfully from {self.file_name}')
            self.used = True
            return 1
        except FileNotFoundError:
            print(f"File {self.file_name} not found.")
        except Exception as e:
            print(f"An error occurred while importing: {e}")
        return 0

    def read_cache(self):
        if not self.used and len(self.cache.keys()) == 0: #CSV never been loaded
            print("No items has been added to watchlist yet, Go for it!")
        elif self.used and len(self.cache.keys()) == 0: # CSV has been manipulated and is now empty
            print("Watchlist is currently empty")
        else: # CSV has been manipulated and has some items, which are updated into cache
            tickers = []
            rates = []

            for ticker in self.cache.keys():
                tickers.append(ticker)
            for rate in self.cache.values():
                rates.append(rate)

            cache_listed = zip(tickers, rates)

            for index, item in enumerate(cache_listed):
                print(f'#{index+1} | {item[0]} | {item[1]}')

    def add_to_cache(self, ticker, rate):
        self.cache[ticker] = rate
        return 1

    def remove_from_cache(self, ticker):
        try:
            self.cache.pop(ticker)
            return 1
        except KeyError as e:
            if ticker not in self.cache:
                print(f"Couldn't find {ticker} in CSV")
            else:
                print(f"Error removing {ticker}: ", e)
        finally:
            return 0
