import 'dart:io';
import 'dart:typed_data';

import 'package:android_flickr/screens/photoEditScreen.dart';
import 'package:flutter/material.dart';
import 'package:photo_gallery/photo_gallery.dart';

class PhotoSelectionScreen extends StatefulWidget {
  final Album _album;
  PhotoSelectionScreen(this._album);
  @override
  _PhotoSelectionScreenState createState() => _PhotoSelectionScreenState();
}

class _PhotoSelectionScreenState extends State<PhotoSelectionScreen> {
  int selected = 0;
  List<File> thumbnailData = [];

  Future initAlbum() async {
    await widget._album
        .listMedia(
      newest: true,
      skip: 0,
    )
        .then((value) async {
      for (var i = widget._album.count - 1; i > -1; i--) {
        // value.items[i].getThumbnail().then((value) {
        //   thumbnailData.add(value);
        // });
        await value.items[i].getFile().then((value) {
          setState(() {
            thumbnailData.add(value);
          });
        });
      }
    });
  }

  @override
  void initState() {
    super.initState();
    initAlbum().then((value) {
      setState(() {});
    });
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
                  widget._album.name,
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
                  '$selected selected',
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
            Container(
              height: MediaQuery.of(context).size.height,
              child: GridView.builder(
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 4,
                  ),
                  itemCount: widget._album.count,
                  itemBuilder: (context, index) {
                    return Container(
                        child: GestureDetector(
                          onTap: () {
                            pushEditScreen(index);
                          },
                          child: getThumbnails(index),
                        ),
                        height: 50,
                        decoration: BoxDecoration(
                          border: Border.all(
                            width: 2,
                            color: Colors.black,
                          ),
                        ));
                  }),
            )
          ],
        ),
      ),
    );
  }

  Widget getThumbnails(int index) {
    try {
      return Image.file(
        thumbnailData[index],
        fit: BoxFit.cover,
      );
    } catch (e) {}
    return Container();
  }

  void pushEditScreen(int index) async {
    String imagePath;
    await widget._album.listMedia().then(
      (value) {
        value.items[index].getFile().then((value) {
          imagePath = value.path;
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (BuildContext context) => PhotoEditScreen(imagePath),
            ),
          );
        });
      },
    );
  }
}
