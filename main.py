import handlers
from storage import CSV


def get_user_selection():
    return input("I want to...\n"
                   "1. Get all available assets\n"
                   "2. Get specific asset rate\n"
                   "3. Load CSV \n"
                   "4. Print watchlist \n"
                   "5. Exit\n"
                   "Please insert your selection: ")


def get_all_available_assets():
    print("Getting info of all assets...")
    assets = handlers.get_all_assets()
    if assets:
        print(assets)  # Print all assets information.
    else:
        print("Failed to fetch assets.")


def get_specific_asset_rate(storage):
    type_of_coin = input("Please insert wanted ticker: ").strip().upper()
    rate_data = handlers.fetch_specific_rate(type_of_coin)
    if rate_data:
        print(rate_data)  # Print specific rate information.
        save = input("Would you like to add this ticker to your watchlist? \nyes/no: ").strip().upper()
        if save == "YES":
            if storage is None:
                file_name = input("You currently do not have a file, write desired name: ")
                storage = CSV(file_name)
            storage.add_to_cache(rate_data.get("asset_id_base"), rate_data.get("rate"))
            print(f"{type_of_coin} has been added to the watchlist.")
            return storage
        else:
            pass
    else:
        print(f"Failed to fetch rate for {type_of_coin}.")
        return storage


def load_csv(storage):
    file_name = input("Pick a filename to import from: ")
    storage = CSV(file_name)
    storage.import_from_csv()
    print("Imported the following CSV info:")
    storage.read_cache()
    return storage


def print_watchlist(storage):
    file_name = ""
    if storage is None:
        file_name = input("You currently do not have a file, write desired name: ")
        storage = CSV(file_name)
    else:
        storage.read_cache()
    return storage


def end_game(storage, is_alive):
    if storage is not None:
        storage.export_to_csv()
    print("Goodbye!")
    is_alive = False
    exit(0)


def main():
    is_alive = True
    storage = None

    while is_alive:
        if handlers.check_api_status() == 1:
            choice = get_user_selection()

            if choice == "1":
                get_all_available_assets()

            elif choice == "2":
                storage = get_specific_asset_rate(storage)

            elif choice == "3":
                storage = load_csv(storage)

            elif choice == "4":
                storage = print_watchlist(storage)

            elif choice == "5":
                end_game(storage, is_alive)

            else:
                print("Invalid option. Please try again.")
        else:
            print("Sorry, the API service is currently unavailable. Please try again later.")


if __name__ == '__main__':
    main()
