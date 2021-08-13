import 'package:android_flickr/screens/login_screen.dart';
import 'package:flutter/material.dart';

class SignUp extends StatefulWidget {
  @override
  _SignUpState createState() => _SignUpState();
}

bool _secureText = true;
String _buttonText = 'Sign up';

class _SignUpState extends State<SignUp> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: null,
        backgroundColor: Colors.grey[900],
        title: Row(
          children: <Widget>[
            Image.asset(
              'assets/images/Logo.png',
              height: 25,
              width: 25,
            ),
            SizedBox(width: 5),
            Text(
              'flicker',
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
      body: new Theme(
        data: new ThemeData(
          primaryColor: Colors.blue[400],
        ),
        child: Container(
          child: Column(children: <Widget>[
            Container(
              margin: EdgeInsets.only(top: 10),
              child: Column(
                children: [
                  Center(
                    child: Image.asset(
                      'assets/images/Logo.png',
                      height: 25,
                      width: 25,
                    ),
                  ),
                  Container(
                    margin: EdgeInsets.only(top: 5, bottom: 5),
                    child: Text(
                      'Sign up to Flicker',
                      style: TextStyle(
                        fontSize: 20,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              child: SingleChildScrollView(
                child: Container(
                  margin: EdgeInsets.only(right: 20, left: 20, top: 10),
                  child: Column(children: <Widget>[
                    _textInput(
                        hint: 'First name',
                        label: 'First name',
                        keyboardType: TextInputType.name),
                    _textInput(
                        hint: 'Last name',
                        label: 'Last name',
                        keyboardType: TextInputType.name),
                    _textInput(
                        hint: 'Your age',
                        label: 'Your age',
                        keyboardType: TextInputType.number),
                    _textInput(
                        hint: 'Email address',
                        label: 'Email address',
                        keyboardType: TextInputType.emailAddress),
                    _textInput(
                        hint: 'Password',
                        label: 'Password',
                        keyboardType: TextInputType.visiblePassword,
                        obscure: _secureText,
                        suffixIcon: _secureText
                            ? Icons.remove_red_eye_outlined
                            : Icons.remove_red_eye,
                        suffixIconPressed: () {
                          setState(() {
                            _secureText = !_secureText;
                          });
                        }),
                    Container(
                      child: RaisedButton(
                        onPressed: () {
                          /* Navigator.push(context,
                              MaterialPageRoute(builder: (context) => LogIn())); */
                        },
                        child: Container(
                          child: Text(
                            _buttonText,
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          width: double.infinity,
                          height: 25,
                          alignment: Alignment.center,
                        ),
                        color: Colors.blue[600],
                      ),
                    ),
                    Divider(
                      color: Colors.grey,
                    ),
                    Container(
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text('Already a Fotone member ?'),
                          FlatButton(
                              padding: EdgeInsets.all(0.0),
                              onPressed: () {
                                Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                        builder: (context) => LogIn()));
                              },
                              child: Text('Log in here.',
                                  style: TextStyle(color: Colors.blue[600])))
                        ],
                      ),
                    )
                  ]),
                ),
              ),
            ),
          ]),
        ),
      ),
    );
  }
}

Widget _textInput({
  hint,
  label,
  keyboardType,
  obscure = false,
  suffixIcon,
  suffixIconPressed,
}) {
  return Container(
    margin: EdgeInsets.only(top: 10),
    decoration: BoxDecoration(
      color: Colors.white,
    ),
    child: TextField(
      decoration: InputDecoration(
        hintText: hint,
        labelText: label,
        suffixIcon:
            IconButton(icon: Icon(suffixIcon), onPressed: suffixIconPressed),
        border: OutlineInputBorder(),
        contentPadding: EdgeInsets.only(top: 20, bottom: 20, left: 20),
      ),
      keyboardType: keyboardType,
      obscureText: obscure,
    ),
  );
}
