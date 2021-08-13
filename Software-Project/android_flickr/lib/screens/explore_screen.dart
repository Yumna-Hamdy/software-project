import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import '../widgets/Explore_display.dart';
import 'package:provider/provider.dart';
import '../providers/flickr_posts.dart';

class ExploreScreen extends StatelessWidget {
  static const routeName = '/explore-screen';

  //when the explore is refreshed this function is called to fetch the latest data from the database
  Future<void> _refreshExplore(BuildContext context) async {
    await Provider.of<Posts>(context, listen: false).fetchAndSetExplorePosts();
  }

  @override
  Widget build(BuildContext context) {
    //this is the Main screen where we have diffrent tabs one of them is only configured which is the explore display
    return DefaultTabController(
      length: 5,
      child: Scaffold(
        backgroundColor: Colors.black.withOpacity(0.5),
        body: NestedScrollView(
          //to scroll through posts and also scroll the tab bar
          headerSliverBuilder: (context, index) {
            return [
              SliverAppBar(
                elevation: 0,
                toolbarHeight: 0,
                floating: true,
                automaticallyImplyLeading: false,
                backgroundColor: Colors.grey.shade900,
                bottom: TabBar(
                  indicatorColor: Colors.transparent,
                  //isScrollable: true,
                  tabs: <Widget>[
                    Tab(
                      icon: Icon(
                        Icons.image,
                      ),
                      //text: 'Categories',
                    ),
                    Tab(
                      icon: Icon(
                        Icons.search,
                      ),
                      //text: 'Favorites',
                    ),
                    Tab(
                      icon: Icon(
                        Icons.account_circle,
                        //color: Colors.white,
                      ),
                      //text: 'Categories',
                    ),
                    Tab(
                      icon: Icon(
                        Icons.notifications,
                      ),
                      //text: 'Favorites',
                    ),
                    Tab(
                      icon: Icon(
                        Icons.camera_alt,
                      ),
                      //text: 'Categories',
                    ),
                  ],
                ),
              )
            ];
          },
          dragStartBehavior: DragStartBehavior.start,
          body: TabBarView(
            //widgets each tab will display
            children: <Widget>[
              //wrapped with refresh indicator which runs the _refreshExplore function when triggered
              RefreshIndicator(
                onRefresh: () {
                  return _refreshExplore(context);
                },
                child: Explore(), //display the explore posts
              ),
              Center(
                child: Text("no search"),
              ),
              Center(
                child: Text("no profile"),
              ),
              Center(
                child: Text("no notifications"),
              ),
              Center(
                child: Text("no camera"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
