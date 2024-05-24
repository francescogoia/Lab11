from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_colors():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)
        query = """select distinct Product_color 
                from go_products gp 
                    """
        cursor.execute(query)
        for row in cursor:
            result.append(row["Product_color"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_prodotti_colore(colore):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct * 
                    from go_products gp 
                    where gp.Product_color = %s
                            """
        cursor.execute(query, (colore,))
        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()

        return result


    @staticmethod
    def conta_date(num_p1, num_p2, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct gds1.`Date`)
                    from go_daily_sales gds1, go_daily_sales gds2
                    where gds1.Product_number = %s and  gds2.Product_number = %s and year (gds1.`Date`) = %s and gds2.Retailer_code = gds1.Retailer_code and gds2.`Date` = gds1.`Date`
                """
        cursor.execute(query, (num_p1, num_p2,anno, ))
        for row in cursor:
            result.append(row['count(distinct gds1.`Date`)'])

        cursor.close()
        conn.close()
        return result


if __name__== "__main__":
    d = DAO
    d.get_prodotti_colore("Brown")