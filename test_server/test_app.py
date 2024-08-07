import uvicorn
from fake_database import Local_Database
from datetime import datetime
import json
import pprint
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

#HOST = '192.168.55.213'
HOST = '127.0.0.1'
PORT = 5000

class Controller:
    def __init__(self) -> None:
        self.__response = {
            'state-code' : '201',
            'body' : '',
        }

    def get_bias_data(self, database:Local_Database, requset:dict):
        self.__response = {
            'state-code' : '201',
            'body' : '',
        }

        bias_data = database.get_bias_data_with_bid(requset['bid'])

        if bias_data:
            self.__response['state-code'] = '200'
            self.__response['body'] = bias_data
        response = json.dumps(self.__response, ensure_ascii=False)
        response = response.encode()
        return response
    

    def get_none_bias_home_data(self, database:Local_Database, requset:dict):
        body = {
            'bias' : [],
            'calender_data' : [],
            'home_body_data' : []
        }
        '''
        a_bias = {
            'bid' : '',
            'bname' : '',
        }
        '''
        user_data = database.get_user_data_with_uid(requset['uid'])

        bids = user_data['bids']
        biases = []

        for bid in bids:
            bias_data = database.get_bias_data_with_bid(bid)
            biases.append(bias_data)

        body_bias = []
        for bias in biases:
            a_bias = {
                'bid' : bias['bid'],
                'bname' : bias['bname']
            }
            body_bias.append(a_bias)

        body['bias'] = body_bias

        '''
            a_calender_data = {
                'date' : '24/04/01',
                'bias' : '1001'
            }
        '''

        schedules = []
        calender_data = []

        for bias in biases:
            for sid in bias['sids']:
                schdeules_data = database.get_schedule_data_with_sid(sid)
                schedules.append(schdeules_data)
                a_calender_data = {
                    'date' : schdeules_data['date'],
                    'bias' : bias['bid']
                }
                calender_data.append(a_calender_data)

        body['calender_data'] = calender_data

        '''
        a_home_body_data = {
            'bname' : '',
            'bid' : '',
            'schedule_data' : []
        }
        a_schedule_data = {
            'scheduleName' : '',
            'type' : 'online',
            'image_url' : []
        }
        a_image_url = '/1001-01.jpg'
        '''
        
        date_format = '%Y/%m/%d'
        target_date = datetime.strptime(requset['date'], date_format)
        schedule_data = []

        pprint.pprint(schedules)

        temp_dict = {}
        for bias in biases:
            temp_dict[bias['bid']] = []

        for schedule in schedules:
            compare_time = datetime.strptime(schedule['date'], date_format)
            if target_date == compare_time:
                image_url = []
                for iid in schedule['iids']:
                    a_image_url = iid + '.jpg'
                    image_url.append(a_image_url)
                #print("schdedule : ", schedule)
                a_schedule_data = {
                    'sid' : schedule['sid'],
                    'schedule_name' : schedule['sname'],
                    'type' : schedule['type'],
                    'image_url' : image_url
                }
                temp_dict[schedule['bid']].append(a_schedule_data)


        home_body_data = []
        for bid, schdeule_data_list in temp_dict.items():
            if len(schdeule_data_list) == 0:
                continue
            for bias in biases:
                if bias['bid'] == bid:
                    bname = bias['bname']

            a_home_body_data = {
                'bname' : bname,
                'bid' : bid,
                'schedule_data' : schdeule_data_list
            }

            home_body_data.append(a_home_body_data)

        body['home_body_data'] = home_body_data

        form = {
            'header' : {
                'state-code' : '200',
            },
            'body' : body
        }
        response = json.dumps(form, ensure_ascii=False)
        #response = response.encode()
        return response

    def get_image_detail(self, database:Local_Database, request:dict):
        form = {
            'header':{
                'state-code' : '201'
            }
        }
        '''
        body = {
            'iid' :'',
            'bias_name' : '',
            'user_owner' : True,
            'upload_date' : '2024/04/01',
            'schedule' : {
                'date' : '2024/03/29',
                'name' : '',
                'location' : ''
            }
        }
        '''
        
        image_data = database.get_image_data_with_iid(iid=request['iid'])
        bias_data = database.get_bias_data_with_bid(bid=image_data['bid'])
        schedule_data = database.get_schedule_data_with_sid(sid=image_data['sid'])

        user_owner = False

        if image_data['uid'] == request['uid']:
            user_owner = True

        body = {
            'iid' : image_data['iid'],
            'bias_name' : bias_data['bname'],
            'user_name' : "테스트 업로더",
            'user_owner' : user_owner,
            'upload_date' : image_data['upload_date'],
            'image_detail' : image_data['image_detail'],
            'schedule' : {
                'date' : schedule_data['date'],
                'name' : schedule_data['sname'],
                'location' : schedule_data['location']
            }
        }

        form['header']['state-code'] = '200'
        form['body']= body
        response = json.dumps(form, ensure_ascii=False)
        response = response.encode()
        return response
    

    def get_image_list_by_bias(self, database:Local_Database, request):
        form = {
            'header':{
                'state-code' : '201'
            }
        }

        body = {
            "bid" : "",
            "bname" : "",
            "num_image" : 0,
            "first_list" : [],
            "second_list" : [],
            "third_list" : []
        }

        bias_data = database.get_bias_data_with_bid(bid = request['bid'])
        image_data = database.get_image_datas_with_bid(bid = request['bid'])

        num_image = len(image_data)
        first_list = []
        second_list = []
        third_list = []
        
        for i, item in enumerate(image_data):
            if i % 3 == 0:
                first_list.append(item)
            elif i % 3 == 1:
                second_list.append(item)
            else:
                third_list.append(item)

        body['bid'] = bias_data['bid']
        body['bname'] = bias_data['bname']
        body['num_image'] = num_image
        body['first_list'] = first_list
        body['second_list'] = second_list
        body['third_list'] = third_list

        form['header']['state-code'] = '209'
        form['body']= body
        response = json.dumps(form, ensure_ascii=False)
        response = response.encode()
        return response

    def get_image_list_by_bias_n_schedule(self, database:Local_Database, request):
        form = {
            'header':{
                'state-code' : '201'
            }
        }

        body = {
            "bid" : "",
            "bname" : "",
            "num_image" : 0,
            "first_list" : [],
            "second_list" : [],
            "third_list" : [],
            "schedule_name" : "",
            "schedule_date" : "",
        }

        bias_data = database.get_bias_data_with_bid(bid = request['bid'])
        image_data = database.get_image_datas_with_bid(bid = request['bid'])
        schedule_data = database.get_schedule_data_with_sid(sid = request['sid'])

        image_list =[]

        for image in image_data:
            iid = image['iid']
            if iid in schedule_data['iids']:
                image_list.append(image)

        num_image = len(image_list)
        first_list = []
        second_list = []
        third_list = []
        
        for i, item in enumerate(image_list):
            if i % 3 == 0:
                first_list.append(item)
            elif i % 3 == 1:
                second_list.append(item)
            else:
                third_list.append(item)

        body['bid'] = bias_data['bid']
        body['bname'] = bias_data['bname']
        body['num_image'] = num_image
        body['first_list'] = first_list
        body['second_list'] = second_list
        body['third_list'] = third_list
        body['schedule_date'] = schedule_data['date']
        body['schedule_name'] = schedule_data['sname']

        form['header']['state-code'] = '210'
        form['body']= body
        response = json.dumps(form, ensure_ascii=False)
        response = response.encode()
        return response
    

    
    def get_bias_following(self, database:Local_Database, request):
        form = {
            'header':{
                'state-code' : '201'
            }
        }

        body = {
            "bias_list" : [],
            "bias_order" : []
        }

        user_data = database.get_user_data_with_uid(request['uid'])

        bias_list = []
        
        for bid in user_data['bids']:
            bias_data = database.get_bias_data_with_bid(bid)
            bias_list.append(bias_data)

        body['bias_list'] = bias_list
        body['bias_order'] = user_data['bids']

        form['header']['state-code'] = '200'
        form['body']= body
        response = json.dumps(form, ensure_ascii=False)
        response = response.encode()

        return response 
    
    def try_upload_post(self, database:Local_Database, request):
        request_body= {
            "uid" : "",
            "bias" : "1001",
            "sname" : "비트로드",
            "date" : "2023/12/06",
            "detail" : "쵸단사진입니아요",
            "link" : "",
            "location" : "",
            "num_images" : 0,
            "image_filenames" : []
        }

        form = {
            'header':{
                'state-code' : '201'
            }
        }

        body = {
            "access_key" : "",
            "secret_token" : "",
            "bucket_name" : "",
            "iid" : ["1001-1", "1001-2"],
        }


        date_format = '%Y/%m/%d'
        target_date = datetime.today().strftime(date_format)


        #bias_data = database.get_bias_data_with_bid(bid=request['bid'])
        bias_data = database.get_bias_data_with_bname(bname=request['bname'])
        last_number = len(bias_data['iid'])

        new_iids = []
        new_images = []
        
        for i in range(request['num_images']):
            new_iid = bias_data['bid'] + "-" + str(last_number + i + 1)
            new_image = {
                "iid" : new_iid,
                "bid" : bias_data['bid'],
                "uid" : request["uid"],
                "sid" : "",
                "image_type" : "jpg",
                "image_detail" : request['detail'],
                "upload_date" : target_date,
                "location" : request['location']
            }

            new_images.append(new_image)
            new_iids.append(new_iid)
        
        schedule_data = database.get_schedule_data_with_sname(sname=request['sname'])

        bias_data['iid'].extend(new_iids)

        if schedule_data:
            schedule_data['iids'].extend(new_iids)
            database.set_schedule_data(schedule_data)
        else:
            new_sid = str(database.get_num_schedule() + 1)

            bias_data['sids'].append(new_sid)
            if request['location'] == "offline":
                schedule_type = "offline"
            else:
                schedule_type = "online"

            schedule_data = {
                "sid" : new_sid,
                "bid" : request['bid'],
                "sname" : request['sname'],
                "date" : request['date'],
                "location" : request['location'],
                "type" : schedule_type,
                "iids" : new_iids
            }
            database.add_new_schedule_data(schedule_data)

        database.set_bias_data(bias_data)

        image_file_names = []
        for image in new_images:
            image['sid'] = schedule_data['sid']
            image_file_names.append(image['iid'] + '.jpg')

        database.add_new_images(new_images)


        body['access_key'] = ""
        body['secret_token'] = ""
        body['bucket_name'] = "cheese-images"
        body['iid'] = image_file_names

        form['header']['state-code'] = '205'
        form['body']= body
        response = json.dumps(form, ensure_ascii=False)
        response = response.encode()
        return response



class ImageListModel:
    def __init__(self, database:Local_Database) -> None:
        self.__database  = database
        self.__user = None
        self.__biases = []
        self.__images = []
    

class BiasFollowingController:
    def __init__(self) -> None:
        self.__response = {
            'state-code' : '201',
            'body' : '',
        }
        return
    

import boto3

class ImageUploadController:
    def __init__(self, raw_request):
        self.__args = {
            'access_key' : 'eeJ2HV8gE5XTjmrBCi48',
            'secret_key' : 'zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv',
            'bucket_name' : 'cheese-images',
            'object_name' : 'test_upload.jpg'
        }


    def boto_upload(self, image):
        args = self.__args
        server_name = 's3'
        endpoint = 'https://kr.object.ncloudstorage.com'

        try:
            s3 = boto3.client(
                server_name,
                endpoint_url = endpoint,
                aws_access_key_id = args["access_key"],
                aws_secret_access_key = args["secret_key"]
            )
            s3.upload_file(f"{image}", args["bucket_name"], args["object_name"])

            return {"done"  : True}
        except Exception as e:
            return {"done":False, "error_message": e}



class View:
    def __init__(self):
        self.__app = FastAPI()
        self.__database = Local_Database()
        self.routes()


    def routes(self):
        @self.__app.get('/')
        def home():
            return 'hello wolrd'
        
        @self.__app.post('/test_data')
        def test_data(request:dict):
            controller = Controller()
            response = controller.get_bias_data(self.__database, request)
            return response

        @self.__app.post('/core_system/none_bias_home_data')
        def get_none_bias_home_data(request:dict):
            print(request)
            controller = Controller()
            response = controller.get_none_bias_home_data(self.__database, request['body'])
            return response

        @self.__app.post('/core_system/image_detail')
        def get_image_detail(request:dict):
            controller = Controller()
            response = controller.get_image_detail(self.__database, request['body'])
            return response

        @self.__app.post('/core_system/get_image_list_by_bias')
        def getImageListByBias(request:dict):
            #request = ImageListByBiasRequest(raw_request=request)
            controller = Controller()
            response = controller.get_image_list_by_bias(self.__database, request['body'])
            return response

        @self.__app.post('/core_system/get_image_list_by_bias_n_schedule')
        def getImageListByBiasNSchedule(request:dict):
            #request = ImageListByBiasRequest(raw_request=request)
            controller = Controller()
            response = controller.get_image_list_by_bias_n_schedule(self.__database, request['body'])
            return response

        @self.__app.post('/bias_following/get_bias_following')
        def getBiasFollowing(request:dict):
            #request = ImageListByBiasRequest(raw_request=request)
            print(request)
            controller = Controller()
            response = controller.get_bias_following(self.__database, request['body'])
            return response
        
        @self.__app.post('/core_system/upload_post')
        def getBiasFollowing(request:dict):
            #request = ImageListByBiasRequest(raw_request=request)
            controller = Controller()
            print(request)
            response = controller.try_upload_post(self.__database, request['body'])
            print(response)
            return response

        @self.__app.post('/upload_test')
        def getBiasFollowing(file: UploadFile = File(...)):
            try:
                print(file.file)
                imageUpload = ImageUploadController()
                result = imageUpload.boto_upload(image=file.file)
                
                return JSONResponse(content={"message": "이미지가 성공적으로 업로드되었습니다."})
            
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))




    def run_server(self):
        uvicorn.run(app=self.__app, host=HOST, port=PORT)


if __name__ == '__main__':
    view = View()
    view.run_server()








