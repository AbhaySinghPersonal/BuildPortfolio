// Example of Splash, Login and Sign Up in React Native
// https://aboutreact.com/react-native-login-and-signup/

// Import React and Component
import React, {useState, createRef} from 'react';
import {
  TextInput,
  View,
  Text,
  ScrollView,
  Image,
  Keyboard,
  TouchableOpacity,
  KeyboardAvoidingView,
} from 'react-native';
import Config from '../config';
LINK=Config.LINK

import { commonStyles } from '../styles/commonStyles';


function LoginScreen  (props) {
  const [userEmail, setUserEmail] = useState('');
  const [userPassword, setUserPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errortext, setErrortext] = useState('');

  const passwordInputRef = createRef();

  const handleSubmitPress = () => {
    setErrortext('');
    if (!userEmail) {
      alert('Please fill Email');
      return;
    }
    if (!userPassword) {
      alert('Please fill Password');
      return;
    }
    setLoading(true);
    var dataToSend = {email: userEmail, password: userPassword};

    apiToCal=LINK+'login'
    console.log(apiToCal)
    fetch(apiToCal, {
      method: 'POST',
      body:JSON.stringify(dataToSend),
      headers: {
        //Header Defination
        'Content-Type':'application/json',
      },
    })
      .then((response) => response.json())
      .then((responseJson) => {
        //Hide Loader
        setLoading(false);
        console.log('--------------Return--------------')
        console.log(responseJson["FRM_API"]["RETURN_CODE"] )
        // If server response message same as Data Matched
        id_ret=responseJson["FRM_API"]["RETURN_CODE"]
        if (id_ret > 0) {
          //AsyncStorage.setItem('user_id', responseJson.data.email);
          console.log('Move to Home---');
          var Data = {email: userEmail,id:id_ret};
          {props.navigation.navigate('Home',{Data:Data})}
        } else {
          setErrortext(responseJson.msg);
          console.log('Please check your email id or password');
        }
      })
      .catch((error) => {
        //Hide Loader
        setLoading(false);
        console.log('Error');
      });
  };

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
                onChangeText={(UserEmail) =>
                  setUserEmail(UserEmail)
                }
                placeholder="Enter Email        " //dummy@abc.com
                placeholderTextColor="#8b9cb5"
                autoCapitalize="none"
                keyboardType="email-address"
                returnKeyType="next"
                onSubmitEditing={() =>
                  passwordInputRef.current &&
                  passwordInputRef.current.focus()
                }
                underlineColorAndroid="#f000"
              />
            </View>
            <View style={commonStyles.SectionStyle}>
              <TextInput
                style={commonStyles.input}
                onChangeText={(UserPassword) =>
                  setUserPassword(UserPassword)
                }
                placeholder="Enter Password" //12345
                placeholderTextColor="#8b9cb5"
                keyboardType="default"
                ref={passwordInputRef}
                onSubmitEditing={Keyboard.dismiss}
                secureTextEntry={true}
                underlineColorAndroid="#f000"
                returnKeyType="next"
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
              onPress={handleSubmitPress}>
              <Text style={commonStyles.buttonTextStyle}>LOGIN</Text>
            </TouchableOpacity>
            <Text
              style={commonStyles.registerTextStyle}
              onPress={() => props.navigation.navigate('Register')}>
              New Here ? Register
            </Text>
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
export default LoginScreen;
