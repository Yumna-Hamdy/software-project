//out of the box imports
import 'dart:typed_data';
import 'package:android_flickr/screens/photo_selection_screen.dart';
import 'package:flutter/material.dart';
//Packages and Plugins
import 'package:photo_gallery/photo_gallery.dart';

//Personal imports
import 'package:android_flickr/screens/flickr_Camera_Screen.dart';

///A screen where the user picks an album, then chooses and image to upload to the server.
class PhotoGalleryScreen extends StatefulWidget {
  @override
  _PhotoGalleryScreenState createState() => _PhotoGalleryScreenState();
}

class _PhotoGalleryScreenState extends State<PhotoGalleryScreen> {
  ///List of all Albums that hold [Image] assets
  List<Album> imageAlbums;

  ///List of Merged Albums, holding both Images and Videos
  List<Album> gallery = [];

  ///A list of thumbnails for each merged album
  List<List<int>> albumThumbnailData = [];

  ///A list of booleans, if [index] is flase,
  ///then the list view builder renders a grey tile instead of a black one, at that index
  List<bool> greyTile = [];

  ///Total number of folders
  int folderCount = 0;

  ///gallery initialization and creating all needed lists
  Future initGallary() async {
    await PhotoGallery.cleanCache();
    gallery = await PhotoGallery.listAlbums(
      hideIfEmpty: true,
      mediumType: MediumType.image,
    );

    gallery.sort((x, y) {
      if (x.name == null) return 0;
      if (y.name == null) return 0;

      if (x.name == 'Download' || x.name == 'Downloads') return -1;
      if (y.name == 'Download' || y.name == 'Downloads') return -1;
      return x.name.toLowerCase().compareTo(y.name.toLowerCase());
    });
    bool tempGreyTile = true;
    for (var i = 0; i < gallery.length; i++) {
      greyTile.add(tempGreyTile);
      tempGreyTile = !tempGreyTile;
    }

    for (var i = 0; i < gallery.length; i++) {
      await PhotoGallery.getAlbumThumbnail(
        height: 70,
        width: 70,
        highQuality: true,
        albumId: gallery[i].id,
        mediumType: MediumType.image,
      ).then((value) => albumThumbnailData.add(value));
      folderCount++;
    }

    setState(() {});
  }

  ///Returns the number of videos and images in a certain album
  String getImageCount(int index) {
    String returnedString = '';

    var imageCount = gallery[index].count;

    returnedString =
        imageCount == 1 ? '$imageCount photo' : '$imageCount photos';

    return returnedString;
  }

  ///initialize gallery at state initialization
  @override
  void initState() {
    super.initState();
    initGallary();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(255, 0, 0, 0),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            SizedBox(
              height: 20,
            ),
            Container(
              height: 40,
              child: ListTile(
                leading: Text(
                  'Photo Gallery',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w400,
                    fontSize: 16,
                  ),
                ),
                trailing: TextButton(
                  onPressed: () {
                    Navigator.pop(context);
                  },
                  child: Text(
                    'Cancel',
                    style: TextStyle(
                      color: Colors.blueAccent,
                    ),
                  ),
                ),
              ),
            ),
            Divider(
              color: Colors.grey,
            ),
            Container(
              height: 20,
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  '$folderCount folders',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    height: 0.1,
                  ),
                ),
              ),
              padding: EdgeInsets.only(
                left: 18,
              ),
            ),
            Divider(
              height: 0,
              color: Colors.grey,
            ),
            ListView.builder(
              padding: EdgeInsets.zero,
              shrinkWrap: true,
              itemCount: gallery.length,
              physics: BouncingScrollPhysics(),
              itemBuilder: (context, index) {
                return GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      PageRouteBuilder(
                        pageBuilder: (context, animation1, animation2) =>
                            PhotoSelectionScreen(gallery[index]),
                        transitionDuration: Duration(seconds: 0),
                      ),
                    );
                  },
                  child: Container(
                    color: greyTile[index]
                        ? Color.fromARGB(255, 0, 0, 0)
                        : Colors.grey.shade900,
                    child: Stack(
                      children: [
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Container(
                            width: 60,
                            height: 60,
                            alignment: Alignment.centerLeft,
                            child: FadeInImage(
                              fit: BoxFit.fitWidth,
                              placeholder: MemoryImage(
                                Uint8List.fromList(albumThumbnailData[index]),
                              ),
                              image: AlbumThumbnailProvider(
                                albumId: gallery[index].id,
                                width: 1000,
                                height: 1000,
                              ),
                            ),
                          ),
                        ),
                        Padding(
                          padding: const EdgeInsets.only(
                            left: 70,
                            top: 20,
                          ),
                          child: Align(
                            alignment: Alignment.topLeft,
                            child: Text(
                              '${gallery[index].name}',
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                color: Colors.white,
                                height: 1,
                              ),
                            ),
                          ),
                        ),
                        Padding(
                          padding: const EdgeInsets.only(
                            left: 70,
                            top: 30,
                          ),
                          child: Align(
                            alignment: Alignment.centerLeft,
                            child: Text(
                              getImageCount(index),
                              style: TextStyle(
                                color: Colors.grey.shade700,
                                height: 2,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
