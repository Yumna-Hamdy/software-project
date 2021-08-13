import 'package:android_flickr/screens/signUp_screen.dart';
import 'package:flutter/material.dart';
import 'package:email_validator/email_validator.dart';

class LogIn extends StatefulWidget {
  @override
  _LogInState createState() => _LogInState();
}

class _LogInState extends State<LogIn> {
  bool _secureText = true;
  String _buttonText = 'Next';
  bool _rememberMe = true;
  final _formKey = GlobalKey<FormState>();
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
            child: Column(
          children: <Widget>[
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
                      'Log in to Flicker',
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
                  child: Column(
                    children: <Widget>[
                      _EmailField(),
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
                      Row(
                        children: <Widget>[
                          Padding(padding: EdgeInsets.all(0.0)),
                          Checkbox(
                              value: _rememberMe,
                              onChanged: (value) {
                                setState(() {
                                  _rememberMe = value;
                                });
                              }),
                          GestureDetector(
                            child: Text('Remeber email address'),
                            onTap: () {
                              setState(() {
                                _rememberMe = !_rememberMe;
                              });
                            },
                          )
                        ],
                      ),
                      Form(
                        key: _formKey,
                        child: Container(
                          child: RaisedButton(
                            onPressed: () {
                              final form = _formKey.currentState;
                              _formKey.currentState.validate();
/*                         setState(() {
                                  _buttonText = 'Sign in';
                                }); */
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
                      ),
                      Container(
                        alignment: Alignment.center,
                        child: FlatButton(
                          onPressed: () {},
                          child: Text(
                            'Forget password ?',
                            style: TextStyle(color: Colors.blue[600]),
                          ),
                        ),
                      ),
                      Divider(
                        color: Colors.grey,
                      ),
                      Container(
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text('Not a Fotone member ?'),
                            FlatButton(
                                padding: EdgeInsets.all(0.0),
                                onPressed: () {
                                  Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                          builder: (context) => SignUp()));
                                },
                                child: Text('Sign up here.',
                                    style: TextStyle(color: Colors.blue[600])))
                          ],
                        ),
                      )
                    ],
                  ),
                ),
              ),
            ),
          ],
        )),
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
    child: TextFormField(
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

Widget _EmailField() {
  return Container(
      margin: EdgeInsets.only(top: 10),
      decoration: BoxDecoration(
        color: Colors.white,
      ),
      child: TextFormField(
          decoration: InputDecoration(
            hintText: 'Email address',
            labelText: 'Email address',
            border: OutlineInputBorder(),
            contentPadding: EdgeInsets.only(top: 20, bottom: 20, left: 20),
          ),
          keyboardType: TextInputType.emailAddress,
          autofillHints: [AutofillHints.email],
          validator: (String value) {
            if (value.isEmpty) {
              return 'Required';
            }
            return null;
          }));
}
