import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/foundation.dart';

//class PicPosterDetails describes few information about the user who posted the picture and these info are his name and whether
//he is a pro or not and if he is followed by the current user(the person using the application) as well as his profile picture url
class PicPosterDetails {
  String name;
  bool isPro;
  bool isFollowedByUser;
  bool followedDuringRunning = false;
  String profilePicUrl;
  PicPosterDetails(
    this.name,
    this.isPro,
    this.isFollowedByUser,
    this.profilePicUrl,
  );
}
//class FavedPostDetails this class describes the post fave details which is how many users faved the post as well as 
//one or two names (if there is anyone who faved) two display below the image. the class also tells us whether the current user
//faved the post or no
class FavedPostDetails {
  int favesTotalNumber;
  List<String> favedUsersNames;
  bool isFaved;
  FavedPostDetails({
    this.favesTotalNumber = 0,
    @required this.favedUsersNames,
    @required this.isFaved,
  });
}

/*class PostDetails includes complete information about the post : its id, instance of PicPosterDetails, instance of FavedPostdetails,
total number of comments on post, the image posted, caption (if available) and since when was it posted*/
class PostDetails with ChangeNotifier {
  String id;
  PicPosterDetails picPoster;
  //int favesTotalNumber;
  FavedPostDetails favesDetails;
  int commentsTotalNumber;
  Map<String, String> lastComment;
  String postImageUrl;
  String caption;
  String postedSince;

  PostDetails({
    @required this.id,
    @required this.picPoster,
    //@required this.favesTotalNumber,
    @required this.commentsTotalNumber,
    @required this.postImageUrl,
    this.lastComment,
    this.caption,
    @required this.postedSince,
    @required this.favesDetails,
  });

  //reflects the user action when he clicks the fave button on the screen as well as updates the database
  void toggleFavoriteStatus() {
    favesDetails.isFaved = !favesDetails.isFaved;
    if (favesDetails.isFaved) {
      favesDetails.favesTotalNumber += 1;
      favesDetails.favedUsersNames.insert(0, "You");
    } else {
      favesDetails.favesTotalNumber -= 1;
      favesDetails.favedUsersNames.remove("You");
    }
    notifyListeners();
    updateFavoriteStatus(favesDetails.isFaved, favesDetails.favesTotalNumber);
  }
  /*updateFavoriteStatus is called inside toggleFavoriteStatus function to reflect changes on database */
  Future<void> updateFavoriteStatus(bool isFaved, int favesTotalNumber) async {
    final url = Uri.https(
        'flickr-explore-default-rtdb.firebaseio.com', '/ExplorePosts/$id.json');
    await http.patch(
      url,
      body: json.encode(
        {
          'isFaved': favesDetails.isFaved,
          'favesTotalNumber': favesDetails.favesTotalNumber,
        },
      ),
    );
  }

  /*reflects the user action on screen as well as the data base if he chooses to follow the owner of the post 
  by clicking on the pop menu button and then follow */
  void followPicPoster() {
    picPoster.isFollowedByUser = true;
    picPoster.followedDuringRunning = true;
    notifyListeners();
    updateFollowPicPoster();
  }
  //this function is called inside followPicPoster to reflect change on database
  Future<void> updateFollowPicPoster() async {
    final url = Uri.https(
        'flickr-explore-default-rtdb.firebaseio.com', '/ExplorePosts/$id.json');
    await http.patch(
      url,
      body: json.encode(
        {
          'isFollowedByUser': true,
        },
      ),
    );
  }

  //returns the short list of the users names who faved the post to display on screem
  List<String> get favedUsersNamesCopy {
    return [...favesDetails.favedUsersNames];
  }
}
