import './few_details_of_faves_comments.dart';
import 'package:flutter/material.dart';
import '../providers/flickr_post.dart';
import 'package:provider/provider.dart';
import 'pic_postedBy_info_on_post.dart';
import '../screens/click_on_image_screen.dart';

//explore post describes how the post will be displayed and the widgets it will use
class ExplorePost extends StatelessWidget {
  //navigator is used here to navigate to the click_on_image_screen widget when we click on the image
  void clickOnImageScreen(BuildContext ctx, PostDetails postInformation) {
    Navigator.of(ctx).pushNamed(
      ClickOnImageScreen.routeName,
      arguments: postInformation,
    );
  }

  /* we set up a listener here to class Posts using provider.of<PostDetails>(context)*/
  
  @override
  Widget build(BuildContext context) {
    final postInformation = Provider.of<PostDetails>(context);
    return ChangeNotifierProvider(
      create: (context) => postInformation,
      child: Container(
        //we return container that includes details of widgets inside the container and their configurations
        alignment: Alignment.topLeft,
        decoration: BoxDecoration(color: Colors.white),
        padding: EdgeInsets.all(5),
        margin: EdgeInsets.all(8),
        child: Column(
          children: <Widget>[
            /* we wrap the container that contains the posted image usinG with gesture detector so when the user presses on the image,
              we go to ClickOnImagesscreen widget*/
            GestureDetector(
              onTap: () {
                clickOnImageScreen(context, postInformation);
              },
              child: Container(
                constraints: BoxConstraints(
                  maxHeight: MediaQuery.of(context).size.height -
                      MediaQuery.of(context).size.height / 4,
                ),
                child: ClipRRect(
                  child: FadeInImage(
                    placeholder: AssetImage("assets/images/placeholder.png"),
                    image: NetworkImage(
                      postInformation.postImageUrl,
                    ),
                    fit: BoxFit.cover,
                    width: double.infinity,
                    /* child: Image.network(
                      postInformation.postImageUrl,
                      //height: 250,

                      /* height: MediaQuery.of(context).size.height -
                            MediaQuery.of(context).size.height / 4, */
                      width: double.infinity,
                      fit: BoxFit.cover,
                    ), */
                  ),
                ),
              ),
            ),
            //we provied it with the instaince of PostDetails class that is postImformation so it can display the widgets below post Image
            PicPostedByInfoOnPost(postInformation),
            //configurations and widgets choosen for the three buttons, fave , comments and share
            Container(
              width: MediaQuery.of(context).size.width / 1.1,
              child: Divider(
                thickness: 2,
              ),
            ),
            Padding(
              padding: EdgeInsets.all(5),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  Row(
                    children: <Widget>[
                      IconButton(
                        icon: postInformation.favesDetails.isFaved
                            ? Icon(
                                Icons.star,
                                color: Colors.blue,
                              )
                            : Icon(
                                Icons.star_border_outlined,
                              ),
                        onPressed: () {
                          postInformation.toggleFavoriteStatus();
                        },
                      ),
                      if (postInformation.favesDetails.favesTotalNumber != 0)
                        Text(
                          postInformation.favesDetails.favesTotalNumber
                              .toString(),
                        ),
                    ],
                  ),
                  Expanded(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        IconButton(
                          icon: Icon(Icons.comment_outlined),
                          onPressed: () {},
                        ),
                        if (postInformation.commentsTotalNumber != 0)
                          Text(
                            postInformation.commentsTotalNumber.toString(),
                          ),
                      ],
                    ),
                  ),
                  Row(
                    children: <Widget>[
                      IconButton(
                        icon: Icon(
                          Icons.share_outlined,
                        ),
                        onPressed: () {},
                      ),
                      SizedBox(
                        width: 6,
                      ),
                      //Text("6"),
                    ],
                  ),
                ],
              ),
            ),
            //few details displayed about the comment(last comment) and one or two names if availabe of the users who faved the post
            FewDetailsOfFavesComments(postInformation),
          ],
        ),
      ),
    );
  }
}
