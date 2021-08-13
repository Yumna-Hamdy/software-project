import 'package:android_flickr/Enums/enums.dart';
import 'package:flutter/material.dart';

class SwitchCaseHelper {
  ///Returns image path of the flash button icon according to chosen Flash mode
  static String getFlashMode(UserFlashMode flashMode) {
    switch (flashMode) {
      case UserFlashMode.always:
        return 'assets/images/FlashAlways.png';
        break;
      case UserFlashMode.auto:
        return 'assets/images/FlashAuto.png';
        break;
      case UserFlashMode.never:
        return 'assets/images/FlashNever.png';
        break;
      default:
        return 'assets/images/FlashAuto.png';
    }
  }

  ///Return the appropriate icon and text based on the [brushMode],
  ///method takes intiger [i] generated from the list view builder method as well as a bool
  ///[isIcon], if true return both icons and text, esle only return text.
  static Widget getIcon(int i, bool isIcon) {
    switch (i) {
      //Saturation
      case 0:
        return isIcon
            ? Row(mainAxisSize: MainAxisSize.max, children: [
                Expanded(
                  child: CircleAvatar(
                    backgroundColor: Colors.cyan,
                    radius: 40,
                    child: Icon(
                      Icons.flip_outlined,
                      color: Colors.white,
                      size: 40,
                    ),
                  ),
                ),
                Text(
                  'Saturation',
                  style: TextStyle(
                    color: Colors.white,
                  ),
                ),
              ])
            : Text(
                'Saturation',
                style: TextStyle(
                  color: Colors.white,
                ),
              );
      //Exposure
      case 1:
        return isIcon
            ? Row(children: [
                Icon(
                  Icons.exposure,
                  color: Colors.white,
                ),
                Text(
                  'Exposure',
                  style: TextStyle(
                    color: Colors.white,
                  ),
                ),
              ])
            : Text(
                'Exposure',
                style: TextStyle(
                  color: Colors.white,
                ),
              );
      //Contrast
      case 2:
        return isIcon
            ? Row(children: [
                Icon(
                  Icons.brightness_medium_rounded,
                  color: Colors.white,
                ),
                Text(
                  'Contrast',
                  style: TextStyle(
                    color: Colors.white,
                  ),
                ),
              ])
            : Text(
                'Contrast',
                style: TextStyle(
                  color: Colors.white,
                ),
              );
      //Brightness
      case 3:
        return isIcon
            ? Row(children: [
                Icon(
                  Icons.wb_sunny_outlined,
                  color: Colors.white,
                ),
                Text(
                  'Brightness',
                  style: TextStyle(
                    color: Colors.white,
                  ),
                ),
              ])
            : Text(
                'Brightness',
                style: TextStyle(
                  color: Colors.white,
                ),
              );
      //Crop
      case 4:
        return isIcon
            ? Row(children: [
                Icon(
                  Icons.crop,
                  color: Colors.white,
                ),
                Text(
                  'Crop',
                  style: TextStyle(
                    color: Colors.white,
                  ),
                ),
              ])
            : Text(
                'Crop',
                style: TextStyle(
                  color: Colors.white,
                ),
              );
      //Rotate
      case 5:
        return isIcon
            ? Row(children: [
                Icon(
                  Icons.rotate_left,
                  color: Colors.white,
                ),
                Text(
                  'Rotate',
                  style: TextStyle(
                    color: Colors.white,
                  ),
                ),
              ])
            : Text(
                'Rotate',
                style: TextStyle(
                  color: Colors.white,
                ),
              );
      //Saturation

      default:
        return isIcon
            ? Row(children: [
                Icon(
                  Icons.flip_outlined,
                  color: Colors.white,
                ),
                Text(
                  'Saturation',
                  style: TextStyle(
                    color: Colors.white,
                  ),
                ),
              ])
            : Text(
                'Saturation',
                style: TextStyle(
                  color: Colors.white,
                ),
              );
    }
  }
}
