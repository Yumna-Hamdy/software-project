import 'package:flutter/material.dart';
import '../providers/flickr_post.dart';

class PopupMenuButtonOfPost extends StatelessWidget {
  final PostDetails
      postInformation; //instance of post details that contains info about the post to set the info about faves and comments
  PopupMenuButtonOfPost(this.postInformation);
  //returns the popupmenubutton to display as trailing in listtile if needed
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: MediaQuery.of(context).size.width / 20,
      child: PopupMenuButton(
        //popupmenubutton takes on selected as an argument where we add the function followPicPoster to follow the owner of the post when option is pressed
        //it also takes builder as an argument which returns a List of popmenu entry with our customization
        onSelected: (int option) {
          if (option == 0) {
            postInformation.followPicPoster();
          }
          if (option == 1) {
            //GestureDetector().onTap();
            GestureDetector(
              onTap: () {},
              behavior: HitTestBehavior.opaque,
            );
          }
        },
        itemBuilder: (ctx) {
          return [
            PopupMenuItem(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(
                    height: MediaQuery.of(context).size.height / 60,
                  ),
                  Text(
                    'follow ' + postInformation.picPoster.name,
                    style: TextStyle(),
                    textAlign: TextAlign.left,
                  ),
                  SizedBox(
                    height: MediaQuery.of(context).size.height / 60,
                  ),
                  Divider(
                    thickness: 2,
                  ),
                ],
              ),
              value: 0,
            ),
            PopupMenuItem(
              child: GestureDetector(
                onTap: () {},
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(
                      height: MediaQuery.of(context).size.height / 60,
                    ),
                    Text(
                      'Why am I seeing this?',
                      style: TextStyle(
                        color: Colors.black,
                      ),
                      textAlign: TextAlign.left,
                    ),
                    SizedBox(
                      height: MediaQuery.of(context).size.height / 50,
                    ),
                    Text(
                      'This is a recomendation hand-picked from our community.',
                      style: TextStyle(
                        color: Colors.black54,
                      ),
                      softWrap: true,
                    ),
                    SizedBox(
                      height: MediaQuery.of(context).size.height / 60,
                    ),
                  ],
                ),
              ),
              value: 1,
            ),
          ];
        },
        icon: Icon(Icons.more_vert),
      ),
    );
  }
}
