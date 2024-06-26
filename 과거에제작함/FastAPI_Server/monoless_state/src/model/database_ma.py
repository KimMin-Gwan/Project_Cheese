import pymysql
import boto3
import requests
from PIL import Image

class Local_Database: 
    def __init__(self) -> None:
        self.conn=None
        self.cur=None
        self.__connect_db() 
    def __connect_db(self):
        print('connect local db')
        self.conn=pymysql.connect(host='localhost',user='root',password='duckfarm1234!',db='Cheese',charset='utf8')
        self.cur=self.conn.cursor()      
    def get_conn(self):
        return self.conn
    def get_cur(self):
        return self.cur
    def send_query(self,type,sql):
        pass
    def __read_data(table,sql):
        pass

    def __write_data(table,sql):
        pass

    def __modify_data(table,sql):
        pass

    def __delete_data(table,sql):
        pass

class Database:
    def __init__(self) -> None:
        self.conn=None
        self.cur=None
        self.__connect_db() 
    def __connect_db(self):
        print('__connect_db')
        self.conn=pymysql.connect(host='db-l6ul6.vpc-cdb.ntruss.com',user='test_user',password='duckfarm1234!',db='Cheese',charset='utf8')
        self.cur=self.conn.cursor()      
    def get_conn(self):
        return self.conn
    def get_cur(self):
        return self.cur
    def find_user_email(self,u_email):
        result=None
        uid=None
        self.cur.callproc('find_email',(u_email,result,uid))    
        self.cur.execute('SELECT @_find_email_1')
        result=self.cur.fetchone()[0]

        self.cur.execute('SELECT @_find_email_2')
        uid=self.cur.fetchone()[0]
        if(result):
            return True
        else:
            return False
        
    def make_user_db(self,uid,email,password,birthdate,tel,name,sex):
        sex_number=2
        if sex=='female':
            sex_number=1
        elif sex=='male':
            sex_number=2
        result=None
        try:
            self.cur.callproc('make_user', (uid,email, password, birthdate, tel, name, sex_number, result))
            self.cur.execute('SELECT @_make_user_1')
            result = self.cur.fetchone()[0]
            self.conn.commit()
        except pymysql.Error as e:
            print('SQL 오류 발생:', e)
        return result
    
    
    
    def send_query(self,type=None,sql=None):
        self.cur.execute('SELECT * FROM user')
        result=self.cur.fetchall()
        print(result)
        
        
    def __read_data(self,table,sql):
        pass

    def write_data(self,table,sql):
        self.cur.execute ('INSERT INTO user (user_name , uid) values(sun,123)')
        self.conn.commit()
        pass

    def __modify_data(self,table,sql):
        pass

    def __delete_data(self,table,sql):
        pass

class Bucket:
    def __init__(self)->None:
        self.s3=boto3.client('s3',endpoint_url='https://kr.object.ncloudstorage.com',aws_access_key_id='eeJ2HV8gE5XTjmrBCi48',aws_secret_access_key='zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv')
        
        self.response=self.s3.list_buckets()
        self.cors()
        self.img_num=0
    def cors(self):   # Cors 설정 해주는 함수 클래스 생성시 자동으로 실행되게 하고 
        bucket_name='baekhyun-test'
        cors_configuration = {
        'CORSRules': [{
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT'],
            'AllowedOrigins': ['*'],
            'MaxAgeSeconds': 3000
        }]
    }
        self.s3.put_bucket_cors(Bucket=bucket_name,
                    CORSConfiguration=cors_configuration)    
        response = self.s3.get_bucket_cors(Bucket=bucket_name)
        print(response['CORSRules'])
    def show_bucket(self):  #bucket출력해주는 함수
        
        for bucket in self.response.get('Buckets', []):
            print(bucket.get('Name'))
            
    def put_bucket(self,local_file_path):  #저장소에 올리는 함수 
        bucket_name='baekhyun-test'
        #object_name='sample-folder/'
        #self.s3.put_object(Bucket=bucket_name ,Key=object_name)
        object_name=f'sample-folder/{self.img_num}.png'
        self.img_num+=1
        self.s3.upload_fileobj(local_file_path,bucket_name,object_name)
        
    def delete_bucket_file(self):  #저장소 내 파일 삭제 하는 함수
        bucket_name='test0.1'
        object_name='test사인2'
        self.s3.delete_object(Bucket=bucket_name,Key=object_name)
    def find_file(self) :
        bucket_name='baekhyun-test'
        object_key='/sample/1.jpg'

if __name__=='__main__':
    buc=Bucket()
    buc.show_bucket()