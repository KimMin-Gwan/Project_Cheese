from model.sample_model import SampleModelTypeOne
from model.fake_database import Local_Database
from model.data_domain import Bias, Schedule
from datetime import datetime
from others import CoreControllerLogicError

class NoneBiasHomeDataModel(SampleModelTypeOne):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._biases = []
        self._schedules = []
        self._home_body_data = []
        self._response_schedule = {}

    
    def set_biases_with_bids(self) -> bool:
        try:
            if len(self._user.bids) == 0:
                return False
            bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=self._user.bids)

            for bias_data in bias_datas:
                bias = Bias()
                bias.make_with_dict(bias_data)
                self._biases.append(bias)
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_bias_with_bid error | " + str(e))

    
    def set_schedules_with_sids(self) -> bool:
        try:
            sids = set()
            for bias in self._biases:
                for sid in bias.sids:
                    sids.add(sid)
            schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=sids)

            # 스케줄 데이터가 하나도 없다면 그냥 반환
            if not schedule_datas:
                return False

            for schedule_data in schedule_datas:
                schedule = Schedule()
                schedule.make_with_dict(schedule_data)
                self._schedules.append(schedule)

            for schedule in self._schedules:
                date = schedule.date
                if not date in self._response_schedule:
                    set_data = set()
                    set_data.update(schedule.bids)
                    self._response_schedule[date] = set_data
                else:
                    self._response_schedule[date].update(schedule.bids)

            for key in self._response_schedule.keys():
                self._response_schedule[key] = list(self._response_schedule[key])


            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_schedules_with_sid error | " + str(e))
    
    def set_home_body_data_with_target_date(self, request) -> bool:
        try:
            date_format = "%Y/%m/%d"
            target_date = datetime.strptime(request.date, date_format)
            filtered_schedules = []

            for schedule in self._schedules:
                compare_date = datetime.strptime(schedule.date, date_format)
                if target_date == compare_date:
                    filtered_schedules.append(schedule)
            
            if len(filtered_schedules) == 0:
                return False

            # 스케줄들 중 선택한 날짜의 스케줄을 필터링하고
            # 내가 구독중인 bias의 스케줄 중에 필터링된 스케줄이 몇개나 포함되었는지 확인할것
            # 스케줄들을 모아서 리스트로 만들어 하나의 homebodydata로 만들것
            # 단, homebodydata 에 포함되는 스케줄이 가지고있는 iid는 해당 bias의 iid와 동일해야함

            for bias in self._biases:
                target_schedules = []
                for schedule in filtered_schedules:
                    if schedule.sid in bias.sids:
                        # 찾았으면 해당 바이어스 이미지만 가지는 스케줄로 재구성
                        target_iids = [item for item in bias.iids if item in schedule.iids]
                        target_schedule = Schedule(sid=schedule.sid, sname=schedule.sname,
                                            date=schedule.date, location=schedule.location,
                                            type=schedule.type, bids=bias.bid, iids = target_iids)
                        target_schedules.append(target_schedule)

                # 찾아낸 스케줄이 하나라도 있다면 데이터로 인스턴스화
                if len(target_schedules) != 0:
                    single_home_body_data = SingleHomeBodyData(bid=bias.bid, bname=bias.bname, 
                                                            schedule_data = target_schedules)
                    self._home_body_data.append(single_home_body_data)
            return True

        except Exception as e:
            raise CoreControllerLogicError(error_type="set_home_body_data_with_target_data error | " + str(e))


    # json 타입의 데이터로 반환
    def get_response_form_data(self, head_parser):
        try:
            body = {
                "bias" : self._make_dict_list_data(list_data=self._biases),
                "calender" : self._response_schedule,
                "home_body_data" : self._make_dict_list_data(list_data=self._home_body_data)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError(error_type="response making error | " + str(e))


class SingleHomeBodyData:
    def __init__(self, bid = "", bname = "", schedule_data = []) -> None:
        self.bid = bid
        self.bname = bname
        self.schedule_data = schedule_data # List<SingleScheduleData>

    # dict 타입의 데이터로 반환
    def get_dict_form_data(self):
        try:
            dict_schedule_data = []
            for data in self.schedule_data:
                dict_schedule_data.append(data.get_dict_form_data())

            return {
                "bid" : self.bid,
                "bname" : self.bname,
                "schedule_data" : dict_schedule_data
            }
        except Exception as e:
            raise CoreControllerLogicError(error_type="response making error | " + str(e))


class BiasHomeDataModel(NoneBiasHomeDataModel):
    def __init__(self, database) -> None:
        super().__init__(database)
        self.__target_bias = Bias()

    def set_schedules_with_sids(self, request) -> bool:
        try:
            for bias in self._biases:
                if bias.bid == request.bid:
                    self.__target_bias = bias

            schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self.__target_bias.sids)

            # 스케줄 데이터가 하나도 없다면 그냥 반환
            if not schedule_datas:
                return False

            for schedule_data in schedule_datas:
                schedule = Schedule()
                schedule.make_with_dict(schedule_data)
                self._schedules.append(schedule)

            for schedule in self._schedules:
                date = schedule.date
                if not date in self._response_schedule:
                    self._response_schedule[date] = [schedule.type]
                else:
                    self._response_schedule[date].append(schedule.type)

            print(self._response_schedule)

            return True
        except Exception as e:
            print(e)
            raise CoreControllerLogicError(error_type="set_schedules_with_sid error | ")
        
    def filtering_home_body_data(self):
        temp_list = []

        for data in self._home_body_data:
            if self.__target_bias.bid == data.bid:
                temp_list.append(data)

        self._home_body_data = temp_list

    # json 타입의 데이터로 반환
    def get_response_form_data(self, head_parser):
        try:
            body = {
                "bias" : self._make_dict_list_data(list_data=self._biases),
                "calender" : self._response_schedule,
                "home_body_data" : self._make_dict_list_data(list_data=self._home_body_data)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError(error_type="response making error | " + str(e))
