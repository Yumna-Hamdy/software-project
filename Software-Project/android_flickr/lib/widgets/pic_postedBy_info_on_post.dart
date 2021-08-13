import 'package:flutter/material.dart';
import '../providers/flickr_post.dart';
import './pop_menu_button_of_post.dart';

class PicPostedByInfoOnPost extends StatelessWidget {
  final PostDetails
      postInformation; //instance of post details that contains info about the post to set the info about faves and comments

  bool isFollowedBeforeRunning =
      true; // helps me to display diffrentiate between the users that I am following before running
  //and who I followed during running so I can display the subtitle widget accordingly since if the user follow during running from the
  //popupmenu item then I should display (followed recomended)text as subtitle

  // returns the widget that will be displayed as subtitle in the listtile below if it will be caption or Following recomended or recomended
  Widget _widgetToBeDisplayedAsSubtitle() {
    if (postInformation.picPoster.isFollowedByUser &&
        !postInformation.picPoster.followedDuringRunning &&
        postInformation.caption != null) {
      return Text(postInformation.caption);
    } else if (postInformation.picPoster.isFollowedByUser &&
        !postInformation.picPoster.followedDuringRunning &&
        postInformation.caption == null) {
      return Text("");
    } else if (postInformation.picPoster.followedDuringRunning) {
      isFollowedBeforeRunning = false;
      return Text("Following recomended");
    } else {
      isFollowedBeforeRunning = false;
      return Text("Recomended");
    }
  }

  // returns the widget that will be displayed as trailing in the listtile below whether it will be
  Widget _widgetToBeDisplayedAsTrailing(BuildContext context) {
    if (postInformation.picPoster.isFollowedByUser &&
        !postInformation.picPoster.followedDuringRunning) {
      return SizedBox(
        width: MediaQuery.of(context).size.width / 10,
        child: Text(postInformation.postedSince),
      );
    } else if (postInformation.picPoster.followedDuringRunning) {
      return Text("");
    } else {
      //returns the popupmenubutton to display as trailing in listtile if needed
      return PopupMenuButtonOfPost(postInformation);
    }
  }

  PicPostedByInfoOnPost(this.postInformation);
  @override
  //the widget returns a container where we have a listtile in it which has the profile picture as leading in circular avatar
  /*the title in the listtile is the name and the subtitle in the listtile is the caption (if available) in case 
  isFollowedByUser = true (which means the current user is following the user who posted the picture) but if isFollowedByUser = false
  then we display as subtitle the word(recomended) and if the user decides to follow the post owner by clicking the follow option
  in the pop menu button then the word (recomended) is replaced with (followed recomended) and the pop menu buttonin the trailing position disappears*/
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ListTile(
          leading: CircleAvatar(
            radius: MediaQuery.of(context).size.width / 20,
            backgroundImage: NetworkImage(
              postInformation.picPoster.profilePicUrl,
            ),
            backgroundColor: Colors.transparent,
            /* child: Image.asset(
                postInformation.url,
                alignment: Alignment.center,
                fit: BoxFit.fill,

                //height: double.infinity,
              ), */
          ),
          title: Text(
            postInformation.picPoster.name,
          ),
          subtitle: _widgetToBeDisplayedAsSubtitle(),
          trailing: _widgetToBeDisplayedAsTrailing(context),
        ),
        if (!isFollowedBeforeRunning && postInformation.caption != null)
          Row(
            children: [
              SizedBox(width: MediaQuery.of(context).size.width / 17),
              Text(
                postInformation.caption,
                textAlign: TextAlign.left,
              ),
            ],
          ),
      ],
    );
  }
}
