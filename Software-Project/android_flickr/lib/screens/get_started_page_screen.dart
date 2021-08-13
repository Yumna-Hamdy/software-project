//import 'dart:js';
//import 'dart:ui';
//import 'package:http/http.dart' as http;
import 'package:android_flickr/screens/explore_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_swiper/flutter_swiper.dart';
import './splash_screen.dart';

enum SlideNumber {
  slide1,
  slide2,
  slide3,
  slide4,
}

class GetStartedScreen extends StatefulWidget {
  static const routeName = '/get-started-screen';
  @override
  _GetStartedScreenState createState() => _GetStartedScreenState();
}

class _GetStartedScreenState extends State<GetStartedScreen> {
  Map<String, Image> swipeImageMap;
  Image moaz;
  Image swipeImage1;
  Image swipeImage2;
  Image swipeImage3;
  Image swipeImage4;

  //returns the String to be dsplayed as title based on the Swipe image we are on
  String _setStartedScreenTitle(int index) {
    switch (index) {
      case 0:
        return 'Powerful';
        break;
      case 1:
        return 'Keep your memories safe';
        break;
      case 2:
        return 'Organisation simpified';
        break;
      case 3:
        return 'Sharing made easy';
        break;
      default:
        return 'Unknown';
    }
  }

  //returns the String to be dsplayed as subtitle based on the Swipe image we are on
  String _setStartedScreenSubTitle(int index) {
    switch (index) {
      case 0:
        return 'Save all of your photos and videos in one place.';
        break;
      case 1:
        return 'Your uploaded photos stay private until you choose to share them.';
        break;
      case 2:
        return 'Search, edit and organise in seconds.';
        break;
      case 3:
        return 'Share with friends, family and the world.';
        break;
      default:
        return 'Unknown';
    }
  }

  //navigates to the loading screen where we give ExploreScreen as an argument to the FlickrSplashScreen
  void exploreScreen(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (context) => FlickrSplashScreen(
          ExploreScreen(),
        ),
      ),
    );
  }

  //to preload the images from assets and added them in a map
  @override
  void initState() {
    swipeImage1 = Image.asset(
      'assets/images/GetStartedScreens/GetStartedScreenSlide1.png',
      alignment: Alignment.center,
      fit: BoxFit.cover,
      height: double.infinity,
      width: double.infinity,
    );
    swipeImage2 = Image.asset(
      'assets/images/GetStartedScreens/GetStartedScreenSlide2.png',
      alignment: Alignment.center,
      fit: BoxFit.cover,
      height: double.infinity,
      width: double.infinity,
    );
    swipeImage3 = Image.asset(
      'assets/images/GetStartedScreens/GetStartedScreenSlide3.png',
      alignment: Alignment.center,
      fit: BoxFit.cover,
      height: double.infinity,
      width: double.infinity,
    );
    swipeImage4 = Image.asset(
      'assets/images/GetStartedScreens/GetStartedScreenSlide4.png',
      alignment: Alignment.center,
      fit: BoxFit.cover,
      height: double.infinity,
      width: double.infinity,
    );

    swipeImageMap = {
      'swipeImage1': swipeImage1,
      'swipeImage2': swipeImage2,
      'swipeImage3': swipeImage3,
      'swipeImage4': swipeImage4,
    };
    print(swipeImageMap.keys.first);

    super.initState();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    //preloades the images from app to the cache so they can be displayed immediately
    precacheImage(swipeImage1.image, context);
    precacheImage(swipeImage2.image, context);
    precacheImage(swipeImage3.image, context);
    precacheImage(swipeImage4.image, context);
  }

  @override
  Widget build(BuildContext context) {
    //returns scaffold where we set the Title, subtitle, button, SwipeImages and author name on stack so we can set the positoin of
    //each widget
    //we also use Swiper widget so we can swipe between images and titles and subtitles
    return Scaffold(
      body: Container(
        padding: EdgeInsets.only(
          top: MediaQuery.of(context).padding.top,
        ),
        height: MediaQuery.of(context).size.height,
        child: Stack(
          children: [
            Container(
              //to provide which swipe image and which title and subtitle to be displayed
              height: double.infinity,
              width: double.infinity,
              child: Swiper(
                containerWidth: double.infinity,
                itemCount: 4,
                loop: false,
                controller: SwiperController(),
                onTap: (index) {
                  if (index < 3) {
                    moaz = swipeImageMap['swipeImage' + '${index + 2}'];
                  }
                },
                itemBuilder: (ctx, index) {
                  return Stack(
                    children: [
                      swipeImageMap['swipeImage' + '${index + 1}'],
                      //so we can postion the title and subtitle in the loaction specified
                      Positioned(
                        top: MediaQuery.of(context).size.height / 1.75,
                        left: MediaQuery.of(context).size.width / 11,
                        child: Container(
                          width: MediaQuery.of(context).size.width -
                              MediaQuery.of(context).size.width / 5.5,
                          alignment: Alignment.center,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Text(
                                _setStartedScreenTitle(index),
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                ),
                                softWrap: true,
                                textAlign: TextAlign.center,
                              ),
                              SizedBox(
                                height: 10,
                              ),
                              Text(
                                _setStartedScreenSubTitle(index),
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 15,
                                ),
                                softWrap: true,
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  );
                },
                //viewportFraction: 1.5,
                scale: 1,
                pagination: SwiperPagination(),
              ),
            ),
            Positioned(
              //to postion the app name on stack
              top: MediaQuery.of(context).size.height / 5,
              //left: MediaQuery.of(context).size.width / 3.5,
              child: Container(
                width: MediaQuery.of(context).size.width,
                child: Text(
                  "flickr",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 70,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
            Positioned(
              //to postion the flat button on stack
              height: MediaQuery.of(context).size.height * 1.65,
              left: MediaQuery.of(context).size.width / 8,
              child: Container(
                alignment: Alignment.center,
                width: MediaQuery.of(context).size.width -
                    MediaQuery.of(context).size.width / 3.7,
                child: InkWell(
                  splashColor: Colors.blue,
                  child: FlatButton(
                    shape: Border.all(
                      color: Colors.white,
                      width: 1,
                    ),
                    height: 60,
                    minWidth: double.infinity,
                    onPressed: () => exploreScreen(context),
                    child: Text(
                      "Get started",
                      style: TextStyle(
                        color: Colors.white,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    color: Colors.transparent,
                  ),
                ),
              ),
            ),
            //to postion the author name on stack
            Positioned(
              height: MediaQuery.of(context).size.height * 1.88,
              left: 10,
              child: Row(
                children: [
                  Icon(
                    Icons.camera_alt,
                    color: Colors.white,
                  ),
                  SizedBox(
                    width: 5,
                  ),
                  Text(
                    "Ben Flasher",
                    style: TextStyle(
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
