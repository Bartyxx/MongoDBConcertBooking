from pymongo import MongoClient

       
class Mongo:
   
    def __init__(self):
        try:
            self.client = MongoClient('mongodb+srv://TheMongoProject:AlfaBetaGamma@cluster0.xbnt0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

        self.db_users = self.client.exam.users
        self.db_tickets = self.client.exam.tickets
        self.db_concerts = self.client.exam.concerts
        self.db_services = self.client.exam.services
        self.singers = {artist["singer_name"] for artist in self.db_concerts.find(projection={"_id": 0, "singer_name": 1})}
        
        self.concert_names = {concert.get("concert_name") for concert in 
                               self.db_concerts.find(projection={"_id": 0, "concert_name": 1}) if concert.get("concert_name")}
       
        self.singers = {artist.get("singer_name") for artist in 
                         self.db_concerts.find(projection={"_id": 0, "singer_name": 1}) if artist.get("singer_name")}
         
        self.cities = {city.get("location", {}).get("city") for city in 
                        self.db_concerts.find(projection={"_id": 0, "location.city": 1}) if city.get("location", {}).get("city")}

        self.dates = {datum["date"][:11].rstrip() for datum in 
                      self.db_concerts.find(projection={"_id":0,"date":1})}
    

    def home(self):
        '''
        Users Log In
        
        Users Insert:
        - first name
        - last name
        - gender
        - tax code
        
        The subscription is registered using the "tax code," so the same tax
        code cannot be used in two different subscriptions.
        '''
        while True:
                self.first_name = input('Enter your first name -> ').title()
                if any(char.isdigit() for char in self.first_name):
                    print("Insert a valid name. Names cannot contain numbers.")
                else:
                    break
        print(50*"-")
        while True:
                self.last_name = input('Enter your last name -> ').title()
                if any(char.isdigit() for char in self.last_name):
                    print("Insert a valid name. Surname cannot contain numbers.")
                else:
                    break
        print(50*"-")
        while True:
                self.tax_code = input('Enter your tax code-> ').upper()
                if len(self.tax_code) != 16:
                    print('The tax code must be 16 characters long.')
                else:
                    break
        print(50*"-")
        while True:
                self.gender = input('Enter "m", "f", or "other": -> ').upper()
                if self.gender not in ["M", "F", "OTHER"]:
                    print('Invalid gender, choose between "M", "F", or "OTHER".')
                else:
                    break
        print(50*"-")
        
        self.insert_user(self.first_name, self.last_name, self.tax_code, self.gender)
    
        filters = {
            "a": "artist",
            "b": "date",
            "c": "city",
            "d": "concert name"
        }
        print('*' * 90)
        print("Find the concert you're interested in, filter by:")
        for k, v in filters.items():
            print(f"{k}: by {v}")
        print('*' * 90)
    
        while True:
            choice = input("Choose how to filter\n")
            if choice in filters:
                break
            else:
                print('Choose one of the available options.')
    
        if choice == "a":
            self.filter_options(self.singers, "artist", self.filter_by_artist)
    
        elif choice == "b":
            self.filter_options(self.dates, "date", self.filter_by_date)
    
        elif choice == "c":
            self.filter_options(self.cities, "city", self.filter_by_city)
    
        elif choice == "d":
            self.filter_options(self.concert_names, "concert", self.filter_by_concert_name)

    
    def filter_options(self, options, type, callback):
        sorted_list = sorted(list(options))
        print('*' * 90)
        print(f"Choose one of the available {type}s:")
        for i, option in enumerate(sorted_list, 1):
            print(f"{i}: {option}")
        print('*' * 90)
        while True:
            try:
                choice = int(input(f"Enter an integer number between 1 and {len(sorted_list)} to choose the {type}\n"))
                if 1 <= choice <= len(sorted_list):
                    callback(sorted_list[choice - 1])
                    break
                else:
                    print(f"Invalid number, choose a {type} between 1 and {len(sorted_list)}.")
            except ValueError:
                print('Enter an integer number.')


    def insert_user(self, first_name, last_name, tax_code, gender):
        '''
        Adds a user to the "users" collection.
        
        Parameters:
        - first_name (str): The user’s first name.
        - last_name (str): The user’s last name.
        - tax_code (str): The user’s tax code.
        - gender (str): The user’s gender.
        '''
        registration = {
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "tax_code": tax_code
        }
    
        # Check if the tax code already exists
        if self.db_users.find_one({"tax_code": tax_code}):
            print('The entered tax code already exists.\n')
        else:
            try:
                self.db_users.insert_one(registration)
                print('User successfully added.\n')
            except Exception as e:
                print(f"Error during user insertion: {e}\n")


    def filter_by_artist(self, artist_name):
        '''
        Filters and displays concerts for a specific artist.
        
        Parameters:
        - artist_name (str): The name of the artist for whom to filter the concerts.
        '''

        while True:
            try:
                # Find concerts for the artist
                # Sto cambiando la chiave di ricerca da artist_name in singer name.
                concerts_data = list(self.db_concerts.find(
                    filter={"singer_name": artist_name},
                    projection={"_id": 0, "concert_name": 1, "date": 1}
                ))
    
                # Retrieve ticket details for each concert
                venue_data = []
                for concert in concerts_data:
                    tickets = self.db_tickets.find_one(
                        filter={"concert_name": concert["concert_name"]},
                        projection={"_id": 0, "ticket_count": 1, "location": 1}
                    )
                                        
                    venue_data.append(tickets)
    
                # Display the found concerts
                print(f"Found concerts: {len(concerts_data)}")
                print('*' * 90)
                for n, concert in enumerate(concerts_data):
                    ticket = venue_data[n]
                    print(f"{n + 1}: {concert['concert_name']}, {concert['date']}, "
                          f"Available tickets: {ticket['ticket_count']}, "
                          f"City: {ticket['location']['city']}, Venue: {ticket['location']['stadium']}")

                print('*' * 90)
    
                # Select the concert
                choice = int(input(f"Choose one of the {len(concerts_data)} available concerts: \n"))
                if choice <= 0 or choice > len(concerts_data):
                    print("Invalid number, try again.")
                    continue

                selected_concert = concerts_data[choice - 1]
                selected_ticket = venue_data[choice - 1]
    
                if selected_ticket["ticket_count"] in [0, 'sold-out']:
                    print(f"Sorry, tickets for the concert {selected_concert['concert_name']} are sold-out.")
                    continue
    
                # Show available sectors
                print("These are the available tickets for each sector:")
                sectors_data = self.db_tickets.find_one(
                    filter={"concert_name": selected_concert["concert_name"]},
                    projection={"_id": 0, "sectors": 1}
                )
                sectors = sectors_data["sectors"]
    
                print('*' * 90)
                for i, sector in enumerate(sectors.keys(), 1):
                    print(f"{i}: {sector} -> Available: {sectors[sector]['available']}, Price: {sectors[sector]['price']}")
                print('*' * 90)

                # Select the sector
                ticket_choice = int(input("Choose which sector you want to buy the ticket for (1-4): \n"))
                if ticket_choice not in range(1, 5):
                    print('Enter a number between 1 and 4.')
                    continue
    
                selected_sector = list(sectors.keys())[ticket_choice - 1]
                available = sectors[selected_sector]['available']
                price = sectors[selected_sector]['price']
                
                purchase = int(input("How many tickets do you want to buy: \n"))
                
                if available == "sold-out":
                    print('Tickets for this sector are sold-out.')
                elif purchase > available:
                    print('You are trying to buy more tickets than available.')
                else:
                    # Update the number of available tickets
                    new_available = available - purchase
                    self.db_tickets.update_one(
                        {"concert_name": selected_concert["concert_name"]},
                        {"$set": {f"sector.{selected_sector}.available": new_available, 
                                   "ticket_count": self.db_tickets.find_one({"concert_name": selected_concert["concert_name"]})["ticket_count"] - purchase}}
                    )
                    
                    print(f"Thank you, your total cost is: {price * purchase} €")
                    print(f"Available tickets for {selected_sector}: {new_available}")
    
                    # Show available services
                    city = selected_ticket['location']['city']
                    service = self.db_services.find_one({"place": city})
    
                    display_service_info(service)
                    break
    
            except (IndexError, ValueError) as e:
                print(f"Error: {e}. Enter a correct value.")


    def filter_by_city(self, city_name):
        '''
        Filters and displays concerts for a specific city.
        
        Parameters:
        - city_name (str): The name of the city for which to filter the concerts.
        '''
        while True:
            try:
                # Retrieve concerts in the specified city
                concerts_data = list(self.db_tickets.find(
                    filter={"location.city": city_name},
                    projection={"_id": 0}
                ))
    
                if not concerts_data:
                    print("No concerts found for this city.")
                    break
    
                # Display the found concerts
                for i, concert in enumerate(concerts_data):
                    print(f'Option {i + 1}')
                    print('*' * 90)
                    print(f"Concert: {concert['concert_name']} \nDate and Time: {concert['date']} \n"
                          f"Available tickets: {concert['ticket_count']}\nCity: {concert['location']['city']}\n"
                          f"Venue: {concert['location']['stadium']}")
                    print('*' * 90)
    
                # Select the concert
                option = int(input(f'Choose one of the {len(concerts_data)} options: \n'))
                if not (1 <= option <= len(concerts_data)):
                    print("Invalid number, try again.")
                    continue
    
                selected_concert = concerts_data[option - 1]
    
                if selected_concert["ticket_count"] in [0, 'sold-out']:
                    print(f"Sorry, tickets for the concert {selected_concert['concert_name']} are sold-out.")
                    continue
    
                # Show available sectors
                sectors = self.db_tickets.find_one(
                    filter={"concert_name": selected_concert['concert_name']},
                    projection={"_id": 0, "sectors": 1}
                )["sectors"]
    
                print("Available sectors:")
                print('*' * 90)
                for i, (sector, details) in enumerate(sectors.items(), 1):
                    print(f"{i}: {sector} -> Available: {details['available']}, Price: {details['price']}")
                print('*' * 90)
                # Select the sector
                ticket_choice = int(input("Choose which sector you want to buy the ticket for (1-4): \n"))
                if ticket_choice not in range(1, 5):
                    print('Enter a number between 1 and 4.')
                    continue
    
                selected_sector = list(sectors.keys())[ticket_choice - 1]
                available = sectors[selected_sector]['available']
                price = sectors[selected_sector]['price']
    
                # Select the number of tickets
                purchase = int(input("How many tickets do you want to buy: \n"))
                if available == "sold-out" or available == 0:
                    print('Tickets for this sector are sold-out.')
                elif purchase > available:
                    print('You are trying to buy more tickets than available.')
                else:
                    # Update the number of available tickets
                    new_available = available - purchase
                    self.db_tickets.update_one(
                        {"concert_name": selected_concert["concert_name"]},
                        {"$set": {f"sector.{selected_sector}.available": new_available,
                                   "ticket_count": self.db_tickets.find_one({"concert_name": selected_concert["concert_name"]})["ticket_count"] - purchase}}
                    )
                    
                    print(f"Thank you, your total cost is: {price * purchase} €")
                    print(f"Available tickets in sector {selected_sector}: {new_available}")
    
                    # Show available services in the city
                    service = self.db_services.find_one({"place": city_name})
                    display_service_info(service)
                    break
    
            except (IndexError, ValueError) as e:
                print(f"Error: {e}. Enter a correct value.")


    def filter_by_concert_name(self, concert_name):
        '''
        Filters and displays concert details based on the concert name.
        
        Parameters:
        - concert_name (str): The name of the concert to filter.
        '''
        while True:
            try:
                # Retrieve concert details
                concert = self.db_tickets.find_one(
                    filter={"concert_name": concert_name},
                    projection={"_id": 0}
                )
    
                if not concert:
                    print("Concert not found.")
                    break
    
                if concert["ticket_count"] in [0, 'sold-out']:
                    print(f"Sorry, tickets for the concert {concert['concert_name']} are sold-out.")
                    break
    
                # Show concert details
                print('*' * 90)
                print(f"Concert: {concert['concert_name']} \nDate and Time: {concert['date']} \n"
                      f"Available tickets: {concert['ticket_count']}\nCity: {concert['location']['city']}\n"
                      f"Venue: {concert['location']['stadium']}")
                print('*' * 90)
                print("These are the available tickets for each sector")
    
                # Retrieve sector details
                sectors = concert['sectors']
    
                # Show available sectors
                print('*' * 90)
                for i, (sector, details) in enumerate(sectors.items(), 1):
                    print(f"{i}: {sector} -> Available: {details['available']}, Price: {details['price']}")
                print('*' * 90)
                # Select the sector
                ticket_choice = int(input("Choose which sector you want to buy the ticket for (1-4): \n"))
                if ticket_choice not in range(1, 5):
                    print('Error: Enter a number between 1 and 4.')
                    continue
    
                selected_sector = list(sectors.keys())[ticket_choice - 1]
                available = sectors[selected_sector]['available']
                price = sectors[selected_sector]['price']
    
                # Select the number of tickets
                purchase = int(input("How many tickets do you want to buy: \n"))
                if isinstance(available, str) and available == "sold-out":
                    print('Tickets for this sector are sold-out.')
                elif purchase > available:
                    print('You are trying to buy more tickets than available.')
                else:
                    # Update the number of available tickets
                    new_available = available - purchase
                    if new_available <= 0:
                        new_available = "sold-out"
                    self.db_tickets.update_one(
                        {"concert_name": concert_name},
                        {"$set": {f"sector.{selected_sector}.available": new_available,
                                   "ticket_count": concert["ticket_count"] - purchase}}
                    )
                    
                    print(f"Thank you, your total cost is: {price * purchase} €")
                    print(f"Available tickets in sector {selected_sector}: {new_available}")
    
                    # Show available services in the city
                    city = concert['location']['city']
                    service = self.db_services.find_one({"place": city})
    
                    display_service_info(service)
                    break
    
            except ValueError:
                print('Error: Enter an integer value.')


    def filter_by_date(self, date):
        '''
        Filters and displays concert details based on the date.
        
        Parameters:
        - date (str): The date of the concert to filter.
        '''
        while True:
            try:
                # Retrieve concert details
                concert = self.db_tickets.find_one(
                    filter={"date": {"$regex": date}},
                    projection={"_id": 0}
                )
    
                if not concert:
                    print("No concert found for the specified date.")
                    break
    
                # Show concert details
                print('*' * 90)
                print(f"Concert: {concert['concert_name']} \nDate and Time: {concert['date']} \n"
                      f"Available tickets: {concert['ticket_count']}\nCity: {concert['location']['city']}\n"
                      f"Venue: {concert['location']['stadium']}")
                print('*' * 90)
                print("These are the available tickets for each sector")
    
                # Retrieve sector details
                sectors = concert['sectors']
    
                # Show available sectors
                print('*' * 90)
                for i, (sector, details) in enumerate(sectors.items(), 1):
                    print(f"{i}: {sector} -> Available: {details['available']}, Price: {details['price']}")
                print('*' * 90)
                # Select the sector
                try:
                    ticket_choice = int(input("Choose which sector you want to buy the ticket for (1-4): \n"))
                    if ticket_choice not in range(1, 5):
                        print('Error: Enter a number between 1 and 4.')
                        continue
                except ValueError:
                    print('Error: Enter an integer value.')
                    continue
    
                selected_sector = list(sectors.keys())[ticket_choice - 1]
                available = sectors[selected_sector]['available']
                price = sectors[selected_sector]['price']
    
                # Select the number of tickets
                try:
                    purchase = int(input("How many tickets do you want to buy: \n"))
                except ValueError:
                    print('Error: Enter an integer value.')
                    continue
    
                if isinstance(available, str) and available == "sold-out":
                    print('Tickets for this sector are sold-out.')
                elif purchase > available:
                    print('You are trying to buy more tickets than available.')
                else:
                    # Update the number of available tickets
                    new_available = available - purchase
                    if new_available <= 0:
                        new_available = "sold-out"
                    
                    self.db_tickets.update_one(
                        {"date": {"$regex": date}},
                        {"$set": {f"sector.{selected_sector}.available": new_available,
                                   "ticket_count": concert["ticket_count"] - purchase}}
                    )
    
                    print(f"Thank you, your total cost is: {price * purchase} €")
                    print(f"Available tickets in sector {selected_sector}: {new_available}")
    
                    # Show available services in the city
                    city = concert['location']['city']
                    service = self.db_services.find_one({"place": city})
    
                    display_service_info(service)
                    break
    
            except IndexError:
                print('Error: Check the entered data and try again.')
            except Exception as e:
                print(f'Unexpected error: {e}')


def display_service_info(service):
    if service:
        print('*' * 90)
        print(f"Services:\n"
              f"Name: {service['name']}\n"
              f"City: {service['place']}\n"
              f"Public transport: {service['services']['metro']['name']}\n"
              f"Walking distance: {service['services']['metro']['travel']['on_foot']}\n"
              f"Driving distance: {service['services']['metro']['travel']['by_car']}\n"
              f"Bar Name: {service['services']['bar']['name']}\n"
              f"Distance: {service['services']['bar']['distance']}\n"
              f"Walking distance to Bar: {service['services']['bar']['travel']['on_foot']}\n"
              f"Driving distance to Bar: {service['services']['bar']['travel']['by_car']}\n")
        print('*' * 90)
    else:
        print('No services found for this city.')
                
if __name__ == '__main__':
    print("-" * 90)
    print("Welcome to the concert booking application in MongoDB!\n"
          "You can register with name, surname, tax code, and gender to access "
          "the application and buy tickets for concerts."
          "It's possible to filter the concerts in a variety of ways to "
          "improve the selection.\n"
          "Thank you and have fun!")
    print("-" * 90)

    a = Mongo()
    a.home()