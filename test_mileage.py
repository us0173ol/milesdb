import mileage
from mileage import MileageError
import sqlite3
from unittest import TestCase

class TestMileageDB(TestCase):

    test_db_url = 'test_miles.db'

    """
    Before running this test, create test_miles.db
    Create expected miles table
    create table miles (vehicle text, total_miles float);
    """

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('CREATE TABLE IF NOT EXISTS  MILES (vehicle text, total_miles float)')
        conn.execute('DELETE FROM MILES')
        conn.commit()
        conn.close()

    def test_upper_vehicle(self):
        new_car = mileage.upper_vehicle('black car')
        self.assertEqual("BLACK CAR", new_car)


    def test_add_new_vehicle(self):
        mileage.add_miles('Blue Car', 100)
        expected = { 'BLUE CAR': 100 }
        self.compare_db_to_expected(expected)

        mileage.add_miles('GrEeN cAr', 50)
        expected['GREEN CAR'] = 50
        self.compare_db_to_expected(expected)


    def test_increase_miles_for_vehicle(self):
        mileage.add_miles('Red Car', 100)
        expected = { 'RED CAR': 100 }
        self.compare_db_to_expected(expected)

        mileage.add_miles('Red Car', 50)
        expected['RED CAR'] = 100 + 50
        self.compare_db_to_expected(expected)


    def test_add_new_vehicle_no_vehicle(self):
        with self.assertRaises(Exception):
            mileage.addMiles(None, 100)


    def test_add_new_vehicle_invalid_new_miles(self):
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', -100)
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', 'abc')
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', '12.def')


    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        cursor = conn.cursor()
        all_data = cursor.execute('SELECT * FROM MILES').fetchall()


        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))

        for row in all_data:
            print (row)
            # Vehicle exists, and mileage is correct
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])

        conn.close()


class TestSearchDB(TestCase):

    test_db_url = 'test_miles.db'

    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('CREATE TABLE IF NOT EXISTS  MILES (vehicle text, total_miles float)')
        conn.execute('DELETE FROM MILES')
        conn.execute('INSERT INTO MILES VALUES (?,?)', ('BLACK CAR', 50))
        conn.execute('INSERT INTO MILES VALUES (?,?)', ('BROWN CAR', 150))
        conn.execute('INSERT INTO MILES VALUES (?,?)', ('BLUE CAR', 500))
        conn.commit()
        conn.close()

    def test_search(self):
        mileage.search_vehicles('black car')
        expected = { 'BLACK CAR': 50, 'BROWN CAR': 150, 'BLUE CAR': 500 }
        self.compare_db_to_expected(expected)

    def test_search(self):
        mileage.search_vehicles('brOWN car')
        expected = { 'BLACK CAR': 50, 'BROWN CAR': 150, 'BLUE CAR': 500 }
        self.compare_db_to_expected(expected)

    def test_search(self):
        mileage.search_vehicles('blue car')
        expected = { 'BLACK CAR': 50, 'BROWN CAR': 150, 'BLUE CAR': 500}
        self.compare_db_to_expected(expected)

    def test_none(self):
        
        self.assertIsNone(mileage.search_vehicles('grey car'))


    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        cursor = conn.cursor()
        all_data = cursor.execute('SELECT * FROM MILES').fetchall()

        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))
        for row in all_data:
            print ('ROW: ', row)
            print ('EXP: ', expected)
            # Vehicle exists, and mileage is correct
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])
        conn.close()
