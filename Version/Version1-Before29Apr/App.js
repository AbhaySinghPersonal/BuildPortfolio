import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View,Button } from 'react-native';
import Home from './components/Home';
import Register from   './components/Register';
import Login from   './components/Login';
import Funds from   './components/Funds';
import AddFunds from   './components/AddFunds';
import UpdFunds from   './components/UpdFunds';
import Portfolio from   './components/Portfolio';
import Proposal from   './components/Proposal';
import Recommend from   './components/Recommend';
import Contants from 'expo-constants';
import { createStackNavigator} from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import Config from "react-native-config";
export const LINK=Config.LINK


const stack = createStackNavigator()

function App() {
  const onButtonPress = () => {
  console.log('Button Pressed')
  }
  return (
    <View style={styles.container}>
     <stack.Navigator>
      <stack.Screen name ="Login" component={Login}/> 
      <stack.Screen name ="Register" component={Register}/> 
      <stack.Screen name ="Home" component={Home}/>
      <stack.Screen name ="Funds" component={Funds}/>
      <stack.Screen name ="AddFunds" component={AddFunds}/>
      <stack.Screen name ="UpdFunds" component={UpdFunds}/>
      <stack.Screen name ="Portfolio" component={Portfolio}/>
      <stack.Screen name ="Proposal" component={Proposal}/>
      <stack.Screen name ="Recommend" component={Recommend}/>
     </stack.Navigator>
    </View>
  );
}

export default() => {
  return (
    <NavigationContainer>
      <App/>
    </NavigationContainer>
  )
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#eddfdf',
    marginTop:Contants.statusBarHeight
  },
});
