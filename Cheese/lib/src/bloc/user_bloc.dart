import 'dart:async';
import 'package:cheese/src/models/user_model.dart';
import 'package:cheese/src/resources/repository.dart';
import 'package:rxdart/rxdart.dart';

class SignInBloC {
  final _repository = SignInRepository();
  final _signFetcher = PublishSubject<SignInModel>();

  // 로그인 시도
  String _email = "";
  RegExp _regex = RegExp(r'@[A-Za-z0-9_]{5,}.*\.[A-Za-z]{2,}');
  String _password = "";

  Stream<SignInModel> get signInModel => _signFetcher.stream;
  // 로그인 시도 결과
  String message = "";

  // Email 세팅
  // return 1이면 정상, return 0 이면 비정상
  setEmail(String email) {
    if (_regex.hasMatch(email)){
      _email = email;
      return 1;
    } else{
      return 0;
    }
  }

  // Email 세팅
  setPassword(String password) {
    if (_regex.hasMatch(password)) {
      _password = password;
      return 1;
    } else{
      return 0;
    }
  }

  // 서버에 로그인을 시도
  fetchSignIn() async {
    _repository.setEmailPassword(_email, _password);
    SignInModel signInModel = await _repository.fetchSign();
    _signFetcher.sink.add(signInModel);
  }

  // 삭제전용 함수
  dispose() {
    _signFetcher.close();
  }
}

class SignUpBloC{
  final _repository = SignUpRepository();

  // 로그인 정규식
  RegExp _regex = RegExp(r'@[A-Za-z0-9_]{5,}.*\.[A-Za-z]{2,}');


  Future<SignUpModel> fetchEmail() async{
    SignUpModel signUpModel = await _repository.fetchEmailSign();
    return signUpModel;
  }

  Future<SignUpModel> fetchOTP() async {
    SignUpModel signUpModel = await _repository.fetchOtpData();
    return signUpModel;
  }


  // Email 세팅
  // return 1이면 정상, return 0 이면 비정상
  setEmail(String email) {
    if (_regex.hasMatch(email)){
      _repository.setEmail(email);
      return 1;
    } else{
      return 0;
    }
  }

  // Password 세팅
  setPassword(String password) {
    if (password != null) {
      _repository.setPassword(password);
      return 1;
    } else{
      return 0;
    }
  }

  // OTP 세팅
  setOTP(String otp) {
    if (otp!= null) {
      _repository.setOtp(otp);
      return 1;
    } else{
      return 0;
    }
  }


  // Year받기
  String _sYear = "";
  setYear(String year){
    _sYear = year.toString();
  }

  // Month 받기
  String _sMonth= "";
  setMonth(String month){
    _sMonth= month.toString();
  }

  // Day 받기
  String _sDay= "";
  setDay(String day){
    _sDay = day.toString();
  }

  // birthday 세팅
  setBirthday() {
    String birthday = _sYear + "/" + _sMonth + "/" + _sDay;
      _repository.setBirthday(birthday);
      return 1;
  }

  // sex 세팅
  setSex(String sex) {
    if (sex != null) {
      _repository.setSex(sex);
      return 1;
    } else{
      return 0;
    }
  }

  // 삭제전용 함수
  dispose() {
  }
}



