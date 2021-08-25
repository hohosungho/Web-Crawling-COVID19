import pymysql as mysql

class CovidDataManager():    # 클래스

    def __init__( self ):
        print("##### INITIALIZING MYSQL #####")
        conn = mysql.connect(   
            host='localhost',
            user='ssac_ysh',
            password='YSH!23',
            db='covid19status',
            port=3307,
            charset='utf8'
        ) 
        self.conn = conn

    def insertIntoTotalData( self, data ):
        # data = [['서울', 23], ['경기', 32]] # crawled data
        cur = self.conn.cursor()
        sql = """INSERT INTO total_confirmed_cases ( city, n_confirmed_case ) VALUES ( %s, %s )"""

        for covid_data in data:
            cur.execute( sql, ( covid_data[0], covid_data[1] ) )
        
        self.conn.commit()

    def insertIntoDailyData( self, data ):
        cur = self.conn.cursor()
        sql = """INSERT INTO daily_confirmed_cases ( dt, city, n_confirmed_case ) VALUES ( %s, %s, %s )"""

        for covid_data in data:
            cur.execute( sql, ( covid_data[0], covid_data[1], covid_data[2] ) )
        
        self.conn.commit()

    def cleanTables( self ):
        cur = self.conn.cursor()
        truncate1 = """TRUNCATE daily_confirmed_cases"""
        truncate2 = """TRUNCATE total_confirmed_cases"""
        cur.execute( truncate1 )
        cur.execute( truncate2 )
        
        self.conn.commit()
