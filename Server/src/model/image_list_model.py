from model.sample_model import SampleModelTypeThree
from model.fake_database import Local_Database
from model.data_domain import Bias, Schedule, Image
from datetime import datetime
from others import CoreControllerLogicError

class ImageListByBiasModel(SampleModelTypeThree):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__bias = Bias()
        self.__images = []
        self.__first_list = []
        self.__second_list = []
        self.__third_list = []

    def set_bias_with_bid(self,request) -> bool: 
        try:
            bias_data = self._database.get_data_with_id(target="bid", id=request.bid)

            if not bias_data:
                return False
        
            self.__bias.make_with_dict(bias_data)

            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_bias_with_bid error | " + str(e))
    
    def set_images_with_bid(self,request) -> bool:
        try:
            if not self.__bias:
                return False
            
            iids=[]
            iids = self.__bias.iids

            for i in iids:
                image_data = self._database.get_data_with_id(target="iid", id=i)
                image = Image()
                image.make_with_dict(image_data)
                self.__images.append(image)
            self.__images = self.__images[request.num_image:]

            if len(self.__images) > 20:
                self.__images = self.__images[:20]
            
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_bias_with_bid error | " + str(e))
    
    def set_list_alignment(self,request):
        try:
            self.__images = super()._set_list_alignment(self.__images, request.ordering)

        except Exception as e:
            raise CoreControllerLogicError(error_type="_set_list_alignment error | " + str(e))

    def make_image_list(self) -> bool:
        try:
            if not self.__images:
                return False
            for i in range(len(self.__images)):
                if i % 3 == 0:
                    self.__first_list.append(self.__images[i].iid)
                elif i % 3 == 1:
                    self.__second_list.append(self.__images[i].iid)
                else:
                    self.__third_list.append(self.__images[i].iid)
                

            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="make_image_list error | " + str(e))

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'bid': self.__bias.bid,
                'bname': self.__bias.bname,
                'num_image' : len(self.__images),
                'first_list' : self.__first_list,
                'second_list' : self.__second_list,
                'third_list' : self.__third_list
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        



class ImageListByBiasNScheduleModel(SampleModelTypeThree):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__bias = Bias()
        self.__schedule = Schedule()
        self.__images = []
        self.__first_list = []
        self.__second_list = []
        self.__third_list = []

    def set_bias_with_bid(self,request) -> bool: 
        try:
            bias_data = self._database.get_data_with_id(target="bid", id=request.bid)

            if not bias_data:
                return False
        
            self.__bias.make_with_dict(bias_data)

            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_bias_with_bid error | " + str(e))
    
    
    def set_schedule_with_sid(self,request) -> bool:
        try:
            schedule_data = self._database.get_data_with_id(target="sid", id=request.sid)

            if not schedule_data:
                return False
        
            self.__schedule.make_with_dict(schedule_data)

            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_schedule_with_sid error | " + str(e))
        
    def set_images_with_sid(self,request) -> bool:
        try:
            if not self.__schedule:
                return False
            
            iids=[]
            iids = self.__schedule.iids

            for i in iids:
                image_data = self._database.get_data_with_id(target="iid", id=i)
                image = Image()
                image.make_with_dict(image_data)
                self.__images.append(image)
                
            self.__images = self.__images[request.num_image:]

            if len(self.__images) > 20:
                self.__images = self.__images[:20]
            
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_images_with_sid error | " + str(e))

    def set_list_alignment(self,request):
        try:
            self.__images = super()._set_list_alignment(self.__images, request.ordering)

        except Exception as e:
            raise CoreControllerLogicError(error_type="_set_list_alignment error | " + str(e))

    def make_image_list(self) -> bool:
        try:
            if not self.__images:
                return False
            
            for i in range(len(self.__images)):
                if i % 3 == 0:
                    self.__first_list.append(self.__images[i].iid)
                elif i % 3 == 1:
                    self.__second_list.append(self.__images[i].iid)
                else:
                    self.__third_list.append(self.__images[i].iid)
                

            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="make_image_list error | " + str(e))

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'bid': self.__bias.bid,
                'bname': self.__bias.bname,
                'num_image' :len(self.__images),
                'sid' : self.__schedule.sid,
                'schedule_date' : self.__schedule.date,
                'schedule_name' : self.__schedule.sname,
                'first_list' : self.__first_list,
                'second_list' : self.__second_list,
                'third_list' : self.__third_list
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)