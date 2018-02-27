import sqlite3

db_url = 'mileage.db'   # Assumes the table miles have already been created.

"""
    Before running this test, create test_miles.db
    Create expected miles table
    create table miles (vehicle text, total_miles float);
"""

class MileageError(Exception):
    pass

def create_table_miles():
        conn = sqlite3.connect(db_url)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS  MILES (vehicle text, total_miles float)')
        conn.commit()
        conn.close()

def add_miles(vehicle, new_miles):
    '''If the vehicle is in the database, increment the number of miles by new_miles
    If the vehicle is not in the database, add the vehicle and set the number of miles to new_miles
    If the vehicle is None or new_miles is not a positive number, raise MileageError
    '''
    upperVehicle = upper_vehicle(vehicle)
    if not vehicle:
        raise MileageError('Provide a vehicle name')
    if not isinstance(new_miles, (int, float))  or new_miles < 0:
        raise MileageError('Provide a positive number for new miles')

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    rows_mod = cursor.execute('UPDATE MILES SET total_miles = total_miles + ? WHERE vehicle = ?', (new_miles, upperVehicle))
    if rows_mod.rowcount == 0:
        cursor.execute('INSERT INTO MILES VALUES (?, ?)', (upperVehicle, new_miles))
    conn.commit()
    conn.close()

def upper_vehicle(vehicle):
    upperVehicle = vehicle.upper()
    return upperVehicle

def search_vehicles(vehicle):
    upperVehicle = upper_vehicle(vehicle)
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    miles = cursor.execute('SELECT total_miles FROM MILES WHERE vehicle = (?)', (upperVehicle,)).fetchall()
    for row in miles:
        print(upperVehicle, miles)
        return miles
    search2 = cursor.execute('SELECT count(*) FROM MILES WHERE vehicle = (?)', (upperVehicle,))
    for row in search2:
        if row == (0,):
            print("No results for %s please try again... " % upperVehicle)
            return None


def main():
    create_table_miles()
    while True:
        vehicle = input('Enter vehicle name or enter to quit:')
        if not vehicle:
            break
        choice = input("Enter 's' to search, or enter 'a' to add mileage for %s: " % vehicle)
        if choice == 's':
            search_vehicles(vehicle)
        elif choice == 'a':
            miles = float(input('Enter new miles for %s: ' % vehicle)) ## TODO input validation
            add_miles(vehicle, miles)
        else:
            print("Enter either 's' or 'a'... ")



if __name__ == '__main__':
    main()
