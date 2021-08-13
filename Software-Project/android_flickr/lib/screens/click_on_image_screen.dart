import 'package:flutter/material.dart';
import '../providers/flickr_post.dart';
//import 'package:provider/provider.dart';

//this class is responsible for all the features and widgets that will be displayed when we click on the post image in Explore display
class ClickOnImageScreen extends StatefulWidget {
  static const routeName = '/click-on-image-screen';
  @override
  _ClickOnImageScreenState createState() => _ClickOnImageScreenState();
}

class _ClickOnImageScreenState extends State<ClickOnImageScreen> {
  bool isDetailsOfPostDisplayed = true;

  //returns a widget which tells me the which string in Text widget that will be displayed based on the favesTotalNumber
  Widget favesText(PostDetails postInformation) {
    if ((postInformation.favesDetails.favesTotalNumber > 1 ||
            postInformation.commentsTotalNumber != 0) &&
        postInformation.favesDetails.favesTotalNumber != 1) {
      return Text(
        '${postInformation.favesDetails.favesTotalNumber}' + ' faves',
        style: TextStyle(
          color: Colors.white,
        ),
        textAlign: TextAlign.right,
      );
    } else if (postInformation.favesDetails.favesTotalNumber == 1) {
      return Text(
        '${postInformation.favesDetails.favesTotalNumber}' + ' fave',
        style: TextStyle(
          color: Colors.white,
        ),
        textAlign: TextAlign.right,
      );
    } else {
      return SizedBox(
        width: MediaQuery.of(context).size.width / 5.25,
      );
    }
  }

  //returns a widget which tells me the which string in Text widget that will be displayed based on the commentsTotalNumber
  Widget commentsText(PostDetails postInformation) {
    if ((postInformation.commentsTotalNumber > 1 ||
            postInformation.favesDetails.favesTotalNumber != 0) &&
        postInformation.commentsTotalNumber != 1) {
      return Text(
        '${postInformation.commentsTotalNumber}' + ' comments',
        style: TextStyle(
          color: Colors.white,
        ),
        textAlign: TextAlign.right,
      );
    } else if (postInformation.commentsTotalNumber == 1) {
      return Text(
        '${postInformation.commentsTotalNumber}' + ' comment',
        style: TextStyle(
          color: Colors.white,
        ),
        textAlign: TextAlign.right,
      );
    } else {
      return SizedBox(
        width: MediaQuery.of(context).size.width / 5.25,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final postInformation = ModalRoute.of(context).settings.arguments
        as PostDetails; // instance of Post details that contains info about the post we are currently displaying
    //final postInformation = Provider.of<PostDetails>(context);
    return Scaffold(
      backgroundColor: Colors.black87,
      body: GestureDetector(
        onTap: () {
          setState(
            () {
              isDetailsOfPostDisplayed = !isDetailsOfPostDisplayed;
            },
          );
        },
        child: Container(
          padding: EdgeInsets.only(
            top: MediaQuery.of(context).padding.top,
          ),
          height: MediaQuery.of(context).size.height,
          child: Stack(
            //fit: StackFit.expand,
            children: [
              if (isDetailsOfPostDisplayed)
                //display listtile which includes profile pic as circular avatar and name of the pic owner as title and cancel button to return to explore screen
                ListTile(
                  leading: CircleAvatar(
                    radius: MediaQuery.of(context).size.width / 20,
                    backgroundImage: NetworkImage(postInformation.postImageUrl),
                    backgroundColor: Colors.transparent,
                  ),
                  title: Text(
                    postInformation.picPoster.name,
                    style: TextStyle(
                      color: Colors.white,
                    ),
                  ),
                  trailing: IconButton(
                    icon: Icon(Icons.cancel_outlined),
                    color: Colors.white,
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                  ),
                ),
              Center(
                //display image of the post
                child: Container(
                  constraints: BoxConstraints(
                    maxHeight: MediaQuery.of(context).size.height -
                        MediaQuery.of(context).size.height / 4,
                  ),
                  child: ClipRRect(
                    child: Image.network(
                      postInformation.postImageUrl,
                      width: double.infinity,
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
              ),
              if (isDetailsOfPostDisplayed) //so when we tap on the screen the bottom bar and top bar navigate between disappear and appear
                Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    SizedBox(
                      height: MediaQuery.of(context).size.height / 1.2,
                    ),
                    if (postInformation.caption != null)
                      Row(
                        children: [
                          SizedBox(
                              width: MediaQuery.of(context).size.width / 17),
                          Text(postInformation.caption,
                              textAlign: TextAlign.left,
                              style: TextStyle(
                                color: Colors.white,
                              )),
                        ],
                      ),
                    if (postInformation.caption == null)
                      Text(
                        "",
                        textAlign: TextAlign.left,
                        style: TextStyle(
                          color: Colors.white,
                        ),
                      ),
                    Container(
                      alignment: Alignment.center,
                      width: MediaQuery.of(context).size.width / 1.1,
                      child: Divider(
                        color: Colors.grey,
                        thickness: 1,
                      ),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: <Widget>[
                        //displays bottom bar which includes fave 0, comment button, share button, info button and faves and comments total number
                        IconButton(
                          icon: postInformation.favesDetails.isFaved
                              ? Icon(
                                  Icons.star,
                                  color: Colors.blue,
                                )
                              : Icon(
                                  Icons.star_border_outlined,
                                  color: Colors.white,
                                ),
                          onPressed: () {
                            setState(
                              () {
                                postInformation.toggleFavoriteStatus();
                              },
                            );
                          },
                        ),
                        IconButton(
                          icon: Icon(
                            Icons.comment_outlined,
                            color: Colors.white,
                          ),
                          onPressed: () {},
                        ),
                        IconButton(
                          icon: Icon(
                            Icons.share_outlined,
                            color: Colors.white,
                          ),
                          onPressed: () {},
                        ),
                        IconButton(
                          icon: Icon(
                            Icons.info_outline,
                            color: Colors.white,
                          ),
                          onPressed: () {},
                        ),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            favesText(postInformation),
                            commentsText(postInformation),
                          ],
                        ),
                      ],
                    ),
                  ],
                ),
            ],
          ),
        ),
      ),
    );
  }
}
