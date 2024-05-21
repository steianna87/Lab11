from database.DB_connect import DBConnect
from model.product import Product
from model.sales import Sale


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllProduct():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ select * from go_products"""

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Product(**row))

        cnx.close()
        cursor.close()

        return result

    @staticmethod
    def getAllProduct_byColor(color):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ select * from go_products p where p.Product_color = %s"""

        cursor.execute(query, (color,))
        result = []
        for row in cursor:
            result.append(Product(**row))

        cnx.close()
        cursor.close()

        return result

    @staticmethod
    def getAllSales():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ select * from go_daily_sales"""

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Sale(**row))

        cnx.close()
        cursor.close()

        return result

    @staticmethod
    def get_peso(p1, p2, year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()

        query = """ select count(distinct gds.`Date`)
                    from go_daily_sales gds, go_daily_sales gds2 
                    where gds.Product_number = %s and gds2.Product_number = %s and year(gds.`Date`) = %s
                    and gds.`Date`  = gds2.`Date` """

        cursor.execute(query, (p1, p2, year))
        result = []
        for row in cursor:
            result.append(row)

        cnx.close()
        cursor.close()

        return result