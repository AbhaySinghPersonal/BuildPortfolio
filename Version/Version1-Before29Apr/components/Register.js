// Example of Splash, Login and Sign Up in React Native
// https://aboutreact.com/react-native-login-and-signup/

// Import React and Component
import React, {useState, createRef} from 'react';
import {
  StyleSheet,
  TextInput,
  View,
  Text,
  Image,
  KeyboardAvoidingView,
  Keyboard,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import Config from '../config';
LINK=Config.LINK
import { commonStyles } from '../styles/commonStyles';


function RegisterScreen (props) {
  const [userName, setUserName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [userPassword, setUserPassword] = useState('');
  const [userPassword2, setUserPassword2] = useState('');
  const [loading, setLoading] = useState(false);
  const [errortext, setErrortext] = useState('');
  const [
    isRegistraionSuccess,
    setIsRegistraionSuccess
  ] = useState(false);

  const emailInputRef = createRef();
  const passwordInputRef = createRef();
  const passwordInputRef2 = createRef();



  const handleSubmitButton = () => {

    setErrortext('');
    if (!userName) {
      alert('Please give your mobile number');
      return;
    }
    const validateMobile = (mobile) => {
      const mobileRegex = /^[6-9]\d{9}$/; // Valid for 10-digit Indian numbers starting from 6-9
      if (!mobileRegex.test(mobile)) {
        alert("Invalid mobile number. Must be 10 digits and start with 6-9.");
      } 
    };
    validateMobile(userName);
    validate = (text) => {
      console.log(text);
      let reg = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/ ;
      if(reg.test(text) === false)
      {
      alert("Email is Not Correct");
      this.setState({email:text})
      return false;
      }
    }
    validate(userEmail)
    if (!userEmail) {
      alert('Please fill Email');
      return;
    }
    
    if (!userPassword2) {
      alert('Please fill Password Again');
      return;
    }
    if (userPassword !== userPassword2) {
      alert('Password Not Match');
      return;
    }
    //Show Loader
    setLoading(true);
    var dataToSend = {
      name: userName,
      email: userEmail,
      password: userPassword,
    };
    var formBody = [];
    for (var key in dataToSend) {
      var encodedKey = encodeURIComponent(key);
      var encodedValue = encodeURIComponent(dataToSend[key]);
      formBody.push(encodedKey + '=' + encodedValue);
    }
    formBody = formBody.join('&');

    apiToCal=LINK+'register'
    console.log("---------register start---------")
    console.log(apiToCal)
    console.log("---------register end---------")
    fetch(apiToCal, {
      method: 'POST',
      body:JSON.stringify(dataToSend),
      headers: {
         'Content-Type':'application/json'
      },
    })
      .then((response) => response.json())
      .then((responseJson) => {
        //Hide Loader
        setLoading(false);
        console.log(JSON.stringify(responseJson))
        setIsRegistraionSuccess(true)
        // If server response message same as Data Matched
        if (responseJson.status === 'success') {
          setIsRegistraionSuccess(true);
          console.log(
            'Registration Successful. Please Login to proceed'
          );
        } 
      })
      .catch((error) => {
        //Hide Loader
        setLoading(false);
        console.log("--------------error------------")
        console.log(error);
        alert("Duplicate")
      });
  };

  console.log("isRegistraionSuccess")
  console.log(isRegistraionSuccess)
  if (isRegistraionSuccess) {
    return (
      <View
        style={{
          flex: 1,
          backgroundColor: '#307ecc',
          justifyContent: 'center',
        }}>
        <Text style={commonStyles.successTextStyle}>
          Registration Successful
        </Text>
        <TouchableOpacity
          style={commonStyles.buttonStyle}
          activeOpacity={0.5}
          //</View>onPress={() => props.navigation.navigate('LoginScreen')}>
          onPress={() => props.navigation.navigate('Login')}>
          <Text style={commonStyles.buttonTextStyle}>Login Now</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    
    <ScrollView contentContainerStyle={commonStyles.scrollView}
            keyboardShouldPersistTaps="handled"
    >
      <View>
        <KeyboardAvoidingView enabled>
          <View style={{alignItems: 'center'}}>
                  <Image
                    source={require('../Image/logo.png')}
                    style={commonStyles.ImgStyle}
                  />
          </View>
          <View style={commonStyles.SectionStyle}>
            <TextInput
              style={commonStyles.input}
              onChangeText={(UserName) => setUserName(UserName)}
              underlineColorAndroid="#f000"
              placeholder="Enter Mobile Number"
              placeholderTextColor="#8b9cb5"
              autoCapitalize="sentences"
              returnKeyType="next"
              onSubmitEditing={() =>
                emailInputRef.current && emailInputRef.current.focus()
              }
            />
          </View>
          <View style={commonStyles.SectionStyle}>
            <TextInput
              style={commonStyles.input}
              onChangeText={(UserEmail) => setUserEmail(UserEmail)}
              underlineColorAndroid="#f000"
              placeholder="Enter Email"
              placeholderTextColor="#8b9cb5"
              keyboardType="email-address"
              ref={emailInputRef}
              returnKeyType="next"
              onSubmitEditing={() =>
                passwordInputRef.current &&
                passwordInputRef.current.focus()
              }
            />
          </View>
          <View style={commonStyles.SectionStyle}>
            <TextInput
              style={commonStyles.input}
              onChangeText={(UserPassword) =>
                setUserPassword(UserPassword)
              }
              underlineColorAndroid="#f000"
              placeholder="Enter Password"
              placeholderTextColor="#8b9cb5"
              ref={passwordInputRef}
              returnKeyType="next"
              secureTextEntry={true}
              onSubmitEditing={() =>
                passwordInputRef2.current &&
                passwordInputRef2.current.focus()
              }
            />
          </View>
          <View style={commonStyles.SectionStyle}>
            <TextInput
              style={commonStyles.input}
              onChangeText={(UserPassword2) =>
                setUserPassword2(UserPassword2)
              }
              underlineColorAndroid="#f000"
              placeholder="Enter Password Again"
              placeholderTextColor="#8b9cb5"
              ref={passwordInputRef2}
              returnKeyType="next"
              secureTextEntry={true}
              onSubmitEditing={Keyboard.dismiss}
            />
          </View>
          {errortext != '' ? (
            <Text style={commonStyles.errorTextStyle}>
              {errortext}
            </Text>
          ) : null}
          <TouchableOpacity
            style={commonStyles.buttonStyle}
            activeOpacity={0.5}
            onPress={handleSubmitButton}>
            <Text style={commonStyles.buttonTextStyle}>REGISTER</Text>
          </TouchableOpacity>
        </KeyboardAvoidingView>
        </View>
        <View style={commonStyles.SectionStyle}>
          <Text style={commonStyles.tailorStyle}>
            Ahyaasena Yoga{'\n'}Manage Portfolio{'\n'}www.abhyaasenayoga.com
          </Text>
        </View>
      </ScrollView> 
  );
};
export default RegisterScreen;

