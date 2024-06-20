import 'dart:ui';

import 'package:cheese/src/bloc/core_bloc/core_state.dart';
import 'package:cheese/src/model/home_data_model.dart';
import 'package:cheese/src/model/user_model.dart';
import 'dart:async';
import 'package:http/http.dart' show Client;
import 'dart:convert';
import 'package:cheese/src/resources/main_json_parser.dart';

class NoneBiasApiJsonParser extends MainJsonParser{
  final Map body = {
    'uid' : '',
    'date' : ''
  };
  Uri __url = Uri();

  NoneBiasApiJsonParser(String endpoint):super(){
    __url = Uri(
      scheme: 'http',
      host:super.host,
      port:super.port,
      path:endpoint,
    );
  }

  void makeBodyData(uid, date){
    body['uid'] = uid;
    body['date'] = date;
  }

  String getData() => super.makeSendData(this.body);

  Uri getUri() => this.__url;
}

class ImageDetailApiJsonParser extends MainJsonParser{
  final Map body = {
    'uid' : '',
    'iid' : ''
  };
  Uri __url = Uri();

  ImageDetailApiJsonParser(String endpoint):super(){
    __url = Uri(
      scheme: 'http',
      host:super.host,
      port:super.port,
      path:endpoint,
    );
  }

  void makeBodyData(uid, iid){
    body['uid'] = uid;
    body['iid'] = iid;
  }

  String getData() => super.makeSendData(this.body);

  Uri getUri() => this.__url;
}


class CoreNetworkProvider{
  final String none_bias_endpoint = '/core_system/none_bias_home_data';
  final String image_detail_endpoint = '/core_system/image_detail';
  Client client = Client();

  Future<HomeDataModel> fetchNoneBiasHome(String uid, String date) async {
    NoneBiasApiJsonParser noneBiasApiJsonParser = NoneBiasApiJsonParser(this.none_bias_endpoint);
    noneBiasApiJsonParser.setHeader(uid, none_bias_endpoint);
    noneBiasApiJsonParser.makeBodyData(uid, date);

    final response = await client.post(
        noneBiasApiJsonParser.getUri(),
        headers: {'Content-Type': 'application/json'},
        body: noneBiasApiJsonParser.getData()
    );
    print('request status: ${response.statusCode}');
    if (response.statusCode == 200) {
      return HomeDataModel.fromJson(jsonDecode(jsonDecode(utf8.decode(response.bodyBytes))));
    } else {
      throw Exception('Failed to load post');
    }
  }

  Future<DetailImageModel> fetchImageDetail(String uid, String iid) async {
    ImageDetailApiJsonParser imageDetailApiJsonParser= ImageDetailApiJsonParser(this.image_detail_endpoint);
    imageDetailApiJsonParser.setHeader(uid, image_detail_endpoint);
    imageDetailApiJsonParser.makeBodyData(uid, iid);

    final response = await client.post(
        imageDetailApiJsonParser.getUri(),
        headers: {'Content-Type': 'application/json'},
        body: imageDetailApiJsonParser.getData()
    );
    print('request status: ${response.statusCode}');
    if (response.statusCode == 200) {
      return DetailImageModel.fromJson(jsonDecode(jsonDecode(utf8.decode(response.bodyBytes))));
    } else {
      throw Exception('Failed to load post');
    }
  }
}