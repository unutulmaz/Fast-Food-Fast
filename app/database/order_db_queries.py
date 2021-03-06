"""This module handles order queries"""
from urllib.parse import urlparse
import psycopg2
from werkzeug.security import generate_password_hash
from flask import current_app as app
from .database import Database


class OrderDbQueries(Database):
    """This class handles database transactions for the order"""

    def __init__(self):
        Database.__init__(self, app.config['DATABASE_URL'])

    def insert_order_data(self, data, username):
        """Insert a new order record into the database"""
        query = "INSERT INTO orders (item_name, quantity, username, status)\
        VALUES('{}', '{}', '{}', '{}');".format(data['item_name'], data['quantity'], username, 'New')
        self.cur.execute(query)
        self.conn.commit()

    def fetch_all_orders(self):
        """ Fetches all order records from the database"""
        self.cur.execute("SELECT * FROM orders ")
        rows = self.cur.fetchall()
        orders = []
        for row in rows:
            row = {'orderId': row[0], 'item_name': row[1],
                   'quantity': row[2],
                    "username": row[3], 'status': row[4],
                   }
            orders.append(row)
        return orders

    def fetch_specific_order_by_parameter(self, table_name, column, param):
        """Fetches a single parameter from a specific table and column"""
        query = "SELECT * FROM {} WHERE {} = '{}'".format(table_name, column, param)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        orders = []
        for row in rows:
            row = {'orderId': row[0], 'item_name': row[1], 'quantity': row[2], 'username' : row[3], 'status' : row[4]}
            orders.append(row)
        return orders

    def update_order_status(self, orderId, status):
        query = "UPDATE orders SET status = '{}' WHERE orderId = {}".format(status, orderId)
        self.cur.execute(query)