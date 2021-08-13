import 'package:android_flickr/Enums/enums.dart';
import 'package:android_flickr/Classes/switch_Case_Helper.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('FlashMode', () {
    test('FlashModeAlways', () {
      //Arrange
      String matcher = 'assets/images/FlashAlways.png';
      //Act
      String actual = SwitchCaseHelper.getFlashMode(UserFlashMode.always);
      //Assert
      expect(actual, matcher);
    });
    test('FlashModeAuto', () {
      //Arrange
      String matcher = 'assets/images/FlashAuto.png';
      //Act
      String actual = SwitchCaseHelper.getFlashMode(UserFlashMode.auto);
      //Assert
      expect(actual, matcher);
    });
    test('FlashModeNever', () {
      //Arrange
      String matcher = 'assets/images/FlashNever.png';
      //Act
      String actual = SwitchCaseHelper.getFlashMode(UserFlashMode.never);
      //Assert
      expect(actual, matcher);
    });
  });
}
