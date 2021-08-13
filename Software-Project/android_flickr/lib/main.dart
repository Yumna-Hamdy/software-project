import 'package:android_flickr/providers/flickr_posts.dart';
import 'package:android_flickr/screens/click_on_image_screen.dart';
import 'package:android_flickr/screens/explore_screen.dart';
import 'package:android_flickr/screens/flickr_Camera_Screen.dart';
import 'package:android_flickr/screens/get_started_page_screen.dart';
import 'package:android_flickr/screens/splash_screen.dart';
//import 'package:android_flickr/screens/flickr_Camera_Screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show DeviceOrientation, SystemChrome;
import 'package:provider/provider.dart';
import './colors/blackSwatch.dart' as primBlack;
import './screens/login_screen.dart';
import './screens/photoEditScreen.dart';

//import './providers/flickr_post.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of the application.
  @override
  Widget build(BuildContext context) {
    //make app work only in portrait
    SystemChrome.setPreferredOrientations(
      [
        DeviceOrientation.portraitUp,
        DeviceOrientation.portraitDown,
      ],
    );

    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (ctx) => Posts(),
        )
      ],
      child: MaterialApp(
        title: 'Flickr',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          fontFamily: 'Rubik',
          primarySwatch: Colors.deepPurple,
          visualDensity: VisualDensity.adaptivePlatformDensity,
        ),
        home: FlickrSplashScreen(
          FlickrCameraScreen(),
        ),
        routes: {
          ExploreScreen.routeName: (ctx) => ExploreScreen(),
          ClickOnImageScreen.routeName: (ctx) => ClickOnImageScreen(),
          GetStartedScreen.routeName: (ctx) => GetStartedScreen(),
          //FlickrSplashScreen.routeName: (ctx) => FlickrSplashScreen(),
        },
      ),
    );
  }
}
