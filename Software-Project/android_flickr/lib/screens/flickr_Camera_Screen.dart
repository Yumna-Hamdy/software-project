// Out of the box imports
import 'dart:io';
import 'dart:math';

//packages and Plugins
import 'package:camerawesome/models/orientations.dart';
import 'package:flutter/material.dart';
import 'package:camerawesome/camerawesome_plugin.dart';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:photo_manager/photo_manager.dart';
import './PhotoGalleryScreen.dart';
import 'package:permission_handler/permission_handler.dart';

//Personal Imports
import 'package:android_flickr/screens/photoEditScreen.dart';
import 'package:android_flickr/Enums/enums.dart';
import 'package:android_flickr/Classes/switch_Case_Helper.dart';

///Flash mode Enum, [always] On , [auto] use, [never] use.

///Main Camera View where users take images or videos,
///Its a widget that occupies the full screen.
class FlickrCameraScreen extends StatefulWidget {
  @override
  _FlickrCameraScreen createState() => _FlickrCameraScreen();
}

class _FlickrCameraScreen extends State<FlickrCameraScreen>
    with TickerProviderStateMixin {
  ///Camera Notifiers.

  ///flash mode notifier, accepts CameraFlashes ENUM.
  ValueNotifier<CameraFlashes> _switchFlash = ValueNotifier(CameraFlashes.NONE);

  ///current sensor notifiers, back or front, accepts Sensors ENUM.
  ValueNotifier<Sensors> _sensor = ValueNotifier(Sensors.BACK);
  ////Capture mode notifier, Photo or video, accepts CaptureModes ENUM.
  ValueNotifier<CaptureModes> _captureMode = ValueNotifier(CaptureModes.PHOTO);

  ///photo resultion notifier, Accepts a size (width, height).
  ValueNotifier<Size> _photoSize = ValueNotifier(Size(3840, 2160));

  ///zoom level notifier, accepts a double between 0 and 1.
  ValueNotifier<double> _zoom = ValueNotifier(0);

  /// Controllers.

  ///Picture Controller which is called to take pictures.
  PictureController _pictureController = new PictureController();

  ///Video Controller which is called to take Start and stop recording videos.
  VideoController _videoController = new VideoController();

  //TODO Replace With better Plugin used in loading library.
  // List of images on the device (customized to only load the first 2 images,
  /// we get the recent image from this list.
  List<AssetEntity> galleryList;

  /// the last image stored on the device.
  File recentImage;

  /// bool that reflects the user choice of either photo or video,a State variable.
  bool isVideoMode = false;

  ///index of the camera mode chosen by user, 0 = back camera, 1 = front, a State variable.
  int inUseCamera;

  /// flash mode chosen by user. its a State variable.
  UserFlashMode flashMode = UserFlashMode.auto;

  ///Discards any resources used by any of the objects. After this is called,
  ///the object is not in a usable state and should be discarded.
  @override
  void dispose() {
    _photoSize.dispose();
    _captureMode.dispose();
    _zoom.dispose();
    _sensor.dispose();
    _switchFlash.dispose();
    super.dispose();
  }

  ///hide notification panel and then initialize Camera and Gallery
  @override
  void initState() {
    super.initState();
    SystemChrome.setEnabledSystemUIOverlays([SystemUiOverlay.bottom]);
    initGallary();
  }

  ///Camera Screen widget Builder method.
  ///
  ///The widget Tree Consists of a main Scaffold That holds a body of a Container,
  ///The container holds a Stack, and a column of stacks. The first stack holds the camera preview,
  ///while the column of stacks presents two bars that hold some buttons including the Switch Camera
  ///mode, flash mode and upload from gallery.
  @override
  Widget build(BuildContext context) {
    final deviceHeight = MediaQuery.of(context).size.height;
    final deviceWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      backgroundColor: Color.fromARGB(255, 31, 31, 33),
      body: Container(
        height: deviceHeight,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Container(
              height: deviceHeight * 0.45,
              child: Stack(
                children: [
                  CameraAwesome(
                    testMode: false,
                    selectDefaultSize: (List<Size> availableSizes) {
                      // print(availableSizes.toString());
                      return availableSizes[0];
                    },
                    onOrientationChanged:
                        (CameraOrientations newOrientation) {},
                    zoom: _zoom,
                    sensor: _sensor,
                    photoSize: _photoSize,
                    switchFlashMode: _switchFlash,
                    captureMode: _captureMode,
                    orientation: DeviceOrientation.portraitUp,
                    fitted: false,
                  ),
                  Padding(
                    padding:
                        EdgeInsets.only(top: 20, left: deviceWidth * 0.825),
                    child: Container(
                      height: 50,
                      width: 50,
                      // padding: EdgeInsets.all(10),
                      color: Colors.black38,
                      child: Icon(
                        Icons.close,
                        color: Colors.white,
                        size: 33,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Stack(
                  children: [
                    Container(
                      color: Color.fromARGB(255, 21, 21, 21),
                      height: deviceHeight * 0.09,
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: deviceHeight * 0.025),
                      child: cameraModeButton('assets/images/CameraMode.png'),
                    ),
                    Align(
                      alignment: Alignment.topRight,
                      child: Padding(
                        padding: EdgeInsets.only(top: deviceHeight * 0.025),
                        child: flashModeButton(
                          SwitchCaseHelper.getFlashMode(flashMode),
                        ),
                      ),
                    ),
                  ],
                ),
                Stack(
                  children: [
                    Container(
                      color: Color.fromARGB(255, 12, 12, 12),
                      height: deviceHeight * 0.125,
                    ),
                    Align(
                      child: GestureDetector(
                        onTap: () {
                          takePhoto();
                        },
                        child: Container(
                          width: 60,
                          height: deviceHeight * 0.125,
                          decoration: BoxDecoration(
                            color: isVideoMode
                                ? Color.fromARGB(255, 167, 23, 23)
                                : Colors.white,
                            shape: BoxShape.circle,
                          ),
                        ),
                      ),
                      alignment: Alignment.center,
                    ),
                    Align(
                      child: Container(
                        width: 8,
                        height: deviceHeight * 0.125,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          shape: BoxShape.circle,
                        ),
                      ),
                      alignment:
                          isVideoMode ? Alignment(-0.2, 0) : Alignment(0.2, 0),
                    ),
                    Align(
                      child: Container(
                        padding: EdgeInsets.only(top: deviceHeight * 0.045),
                        width: 30,
                        child: GestureDetector(
                          onTap: () {
                            setState(() {
                              isVideoMode = false;
                            });
                          },
                          child: Image.asset(
                            isVideoMode
                                ? 'assets/images/Photo_Grey.png'
                                : 'assets/images/Photo.png',
                          ),
                        ),
                      ),
                      alignment: Alignment(0.32, 0),
                    ),
                    Align(
                      child: Container(
                        padding: EdgeInsets.only(top: deviceHeight * 0.045),
                        width: 30,
                        child: GestureDetector(
                          onTap: () {
                            setState(() {
                              isVideoMode = true;
                            });
                          },
                          child: Image.asset(
                            isVideoMode
                                ? 'assets/images/Video.png'
                                : 'assets/images/Video_Grey.png',
                          ),
                        ),
                      ),
                      alignment: Alignment(-0.32, 0),
                    ),
                    Align(
                      child: Container(
                        padding: EdgeInsets.only(top: deviceHeight * 0.0525),
                        width: 35,
                        height: 70,
                        child: GestureDetector(
                          onTap: () {
                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (BuildContext context) =>
                                        PhotoGalleryScreen()));
                          },
                          child: recentImage == null
                              ? Container(
                                  color: Colors.grey,
                                )
                              : Image.file(
                                  recentImage,
                                  fit: BoxFit.cover,
                                ),
                        ),
                      ),
                      alignment: Alignment(-0.9, 0),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  ///Initialize Camera and Gallery, retreive gallery list
  //initialization method, No unit Test.
  Future initGallary() async {
    await PhotoManager.requestPermission();
    await Permission.storage.request();
    PhotoManager.clearFileCache();

    //get a list of all assets and order them by date of creation to get most recent
    List<AssetPathEntity> list = await PhotoManager.getAssetPathList(
      onlyAll: true,
      filterOption: FilterOptionGroup(
        orders: [
          OrderOption(
            type: OrderOptionType.createDate,
          )
        ],
      ),
    );

    //only get the first two images, not anymore are needed in this view
    galleryList = await list[0].getAssetListRange(start: 0, end: 1);

    //Set recent image to the recieved file and rebuild
    galleryList[0].file.then((value) {
      setState(() {
        recentImage = value;
      });
    });
  }

  ///Camera Mode Button receives an image path string of the button icon
  ///When the button is pressed it toggles between front and back cameras
  Widget cameraModeButton(String imagePath) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.05,
      child: GestureDetector(
        onTap: () {
          if (inUseCamera == 1) {
            setState(() {
              inUseCamera = 0;
            });
            _sensor.value = Sensors.BACK;
          } else {
            setState(() {
              inUseCamera = 1;
            });
            _sensor.value = Sensors.FRONT;
          }
        },

        ///The image is rotated 180 degrees on the Y axis if mode is Front camera
        child: inUseCamera == 0
            ? Padding(
                padding: const EdgeInsets.only(left: 10),
                child: Image.asset(
                  imagePath,
                  width: 30,
                  height: 30,
                ),
              )
            : Padding(
                padding: const EdgeInsets.only(left: 40),
                child: Transform(
                  transform: Matrix4.rotationY(pi),
                  child: Image.asset(
                    imagePath,
                    width: 30,
                    height: 30,
                  ),
                ),
              ),
      ),
    );
  }

  ///Flash Mode Button receives and image path string of the button icon
  ///When the button is pressed it toggles between 3 available flash modes
  /// Always > Never > Auto > Always (and so forth)
  Widget flashModeButton(String imagePath) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.05,
      child: GestureDetector(
        onTap: () {
          if (flashMode == UserFlashMode.always) {
            setState(() {
              flashMode = UserFlashMode.never;
            });
            _switchFlash.value = CameraFlashes.NONE;
            return;
          }
          if (flashMode == UserFlashMode.never) {
            setState(() {
              flashMode = UserFlashMode.auto;
            });
            _switchFlash.value = CameraFlashes.AUTO;
            return;
          }
          if (flashMode == UserFlashMode.auto) {
            setState(() {
              flashMode = UserFlashMode.always;
            });
            _switchFlash.value = CameraFlashes.ALWAYS;
            return;
          }
        },
        child: Padding(
          padding: const EdgeInsets.only(right: 8.0),
          child: Image.asset(
            imagePath,
            width: 35,
            height: 35,
          ),
        ),
      ),
    );
  }

  ///Called When the take photo button is pressed.
  ///Image is initially saved in temporary directory,
  ///It is then saved to phone gallery,
  ///and the new photo path is passed to PhotoEditScreen.
  Future takePhoto() async {
    final Directory tempDir = await getTemporaryDirectory();
    final imageDir =
        await Directory('${tempDir.path}/test').create(recursive: true);
    final String filePath =
        '${imageDir.path}/${DateTime.now().millisecondsSinceEpoch}.jpg';
    await _pictureController.takePicture(filePath).then(
          (value) => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (BuildContext context) => PhotoEditScreen(filePath),
            ),
          ),
        );

    // if (filePath != null) {
    //   final result = await ImageGallerySaver.saveFile(filePath);
    //   print(result);
    // } else {
    //   print('Null path');
    // }
  }
}
