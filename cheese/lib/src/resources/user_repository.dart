import 'package:cheese/src/model/user_model.dart';
import 'package:cheese/src/resources/user_network_provider.dart';

class UserRepository{
  final UserNetworkProvider userNetworkProvider = UserNetworkProvider();
  UserModel __userModel = UserModel();

  void setUserModel(UserModel userModel) {
    this.__userModel = userModel;
  }

  getUserModel() => this.__userModel;
  Future<UserModel> fetchUserData() => userNetworkProvider.fetchUserData(__userModel.get_user().getUid());

}