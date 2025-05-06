// Example of Splash, Login and Sign Up in React Native
// https://aboutreact.com/react-native-login-and-signup/

// Import React and Component
import React from 'react';
import {View, Text, ScrollView,Image,KeyboardAvoidingView} from 'react-native';
import { Button } from 'react-native-paper';
import { commonStyles } from '../styles/commonStyles';

const HomeScreen = (props) => {
  const Data = props.route.params.Data;
  console.log('--------HOME---------')
  console.log(Data.email)
  return (
     <ScrollView contentContainerStyle={commonStyles.scrollView}
            keyboardShouldPersistTaps="handled"
          >
          <View >
          <KeyboardAvoidingView enabled>
            <View style={{alignItems: 'center'}}>
              <Image
                source={require('../Image/logo.png')}
                style={commonStyles.ImgStyle}
              />
            </View>
            <View style={commonStyles.SectionStyle}>
              <Button
                style={commonStyles.buttonStyle1}
                mode="contained"
                onPress={() => {props.navigation.navigate('Funds',{Data:Data})}}
              >Manage Funds</Button>
            </View>
            <View style={commonStyles.SectionStyle}>
              <Button
                style={commonStyles.buttonStyle1}
                mode="contained"
                onPress={() => {props.navigation.navigate('Portfolio',{Data:Data})}}
              >Show Portfolio</Button>
            </View>
            <View style={commonStyles.SectionStyle}>
              <Button
                style={commonStyles.buttonStyle1}
                mode="contained"
                onPress={() => {props.navigation.navigate('Proposal',{Data:Data})}}
              >Analyze & Recommend Buy/Sell</Button>
            </View>
            <View style={commonStyles.SectionStyle}>
              <Button
                style={commonStyles.buttonStyle1}
                mode="contained"
                onPress={() => {props.navigation.navigate('Recommend',{Data:Data})}}
              >Short/Long Recommendation </Button>
            </View>
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

export default HomeScreen;