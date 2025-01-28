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
import { Button } from 'react-native-paper';
import Config from '../config';
LINK=Config.LINK



function FundsScreen (props) {
    const Data = props.route.params.Data;
    const [
        isFundsDataNotAvailable,
        setFundsDataAvailable
      ] = useState(false);
    const [
        isUnallocatedFundsAvailable,
        setUnallocatedFundsAvailable
      ] = useState(false);
    var condition=useState(''); // Initial condition
    const [Email, setEmail] = useState(Data.email);
    const emailInputRef = createRef();
    var [totalFund, setTotalFund] = useState(0.0);
    var totalFundInputRef = createRef();
    var [allocatedFund, setAllocatedFund] = useState(0.0);
    var allocatedFundInputRef = createRef();
    var [unusedFund, setUnusedFund] = useState(0.0);
    var unusedFundInputRef = createRef();
    var funds_Data_Return = {
        id:0,
        Email:Data.email,
        totalFund:0.0,
        allocatedFund:0.0,
        unusedFund:0.0,
        UpdDate:""
      };
    apiToCal=LINK+"getFund/"+Data.email
    fetch(apiToCal, {
      method: 'GET',
      headers: {
         'Content-Type':'application/json'
      },
      body:JSON.stringify(funds_Data_Return),
    })
      .then((response) => response.json())
      .then((responseJson) => {
        //Hide Loader
        console.log(JSON.stringify(responseJson))
        setFundsDataAvailable(true)
      })
      .catch((error) => {
        //Hide Loader
        console.log("--------------error------------")
      });
  
  if (isFundsDataNotAvailable ) { 
    if(funds_Data_Return.unusedFund>0)
        setUnallocatedFundsAvailable(true)
  }
  if((isFundsDataNotAvailable==true) && (isUnallocatedFundsAvailable==true))
    {
      condition='A'
    }
  if((isFundsDataNotAvailable==true) && (isUnallocatedFundsAvailable==false))
    {
      condition='B'
    }
  const [
    isFundsDataNeedsToAdd,
    setIsFundsDataNeedsToAdd
  ] = useState(false);
  if(isFundsDataNotAvailable==false) 
  {
    condition='C'
    setIsFundsDataNeedsToAdd(true)
  }
  var funds_Data_Create = {
    Email:Data.email,
    totalFund:totalFund,
    allocatedFund:allocatedFund,
    unusedFund:unusedFund,
  };

  apiToCal=LINK+"addFund/"
  const createFund = () => {
    fetch(apiToCal,{
      method:'POST',
      headers:{
          'Content-Type':'application/json'
      },
      body:JSON.stringify(funds_Data_Return),
  })
  .then(resp => resp.json())
  .then(data =>{props.navigation.navigate("Home")
  })
  .catch(error => console.log(error) )

}

  return (
    <View style={{flex: 1, backgroundColor: '#307ecc'}}>
    <ScrollView
        keyboardShouldPersistTaps="handled"
        contentContainerStyle={{
        justifyContent: 'center',
        alignContent: 'center',
        }}>
        <KeyboardAvoidingView enabled>
        
        <View style={styles.SectionStyle}>
            <TextInput
            style={styles.inputStyle}
            value={totalFund}
            onChangeText={(text) => setTotalFund(text)}
            underlineColorAndroid="#f000"
            placeholder="Enter Total Funds"
            placeholderTextColor="#8b9cb5"
            autoCapitalize="sentences"
            returnKeyType="next"
            onSubmitEditing={() =>
                allocatedFundInputRef.current && allocatedFundInputRef.current.focus()
            }
            editable={isFundsDataNeedsToAdd} 
            selectTextOnFocus={isFundsDataNeedsToAdd} 
            blurOnSubmit={false}
            />
        </View>
        <View style={styles.SectionStyle}>
            <TextInput
            style={styles.inputStyle}
            value={allocatedFund}
            onChangeText={(text) => setAllocatedFund(text)}
            underlineColorAndroid="#f000"
            placeholder="Enter Allocated Fund"
            placeholderTextColor="#8b9cb5"
            keyboardType="numeric"
            ref={allocatedFundInputRef}
            returnKeyType="next"
            onSubmitEditing={() =>
                allocatedFundInputRef.current &&
                allocatedFundInputRef.current.focus()
            }
            editable={isFundsDataNeedsToAdd} 
            selectTextOnFocus={isFundsDataNeedsToAdd} 
            blurOnSubmit={false}
            />
        </View>
        <View style={styles.SectionStyle}>
            <TextInput
            style={styles.inputStyle}
            value={unusedFund}
            onChangeText={(text) =>
                setUnusedFund(text)
            }
            underlineColorAndroid="#f000"
            placeholder="Enter Unused Fund"
            keyboardType="numeric"
            placeholderTextColor="#8b9cb5"
            ref={unusedFundInputRef}
            returnKeyType="next"
            onSubmitEditing={() =>
                unusedFundInputRef.current &&
                unusedFundInputRef.current.focus()
            }
            editable={true} 
            selectTextOnFocus={true} 
            blurOnSubmit={false}
            />
        </View>
        <View>
          {condition === 'A' ? (
                <Button
                    style={styles.buttonStyle}
                    mode="contained"
                    onPress={() => {console.log('Pressed >Add More Funds')}}
                >Add More Funds</Button>
          ): condition === 'B' ? (
                <Button
                    style={styles.buttonStyle}
                    mode="contained"
                    onPress={() => {console.log('Pressed Allocate Unallocated Funds')}}
                >Allocate Unallocated Funds</Button>
          ): (
                <Button
                    style={styles.buttonStyle}
                    mode="contained"
                    onPress={() => {console.log('Pressed Add Fund')}}
                >Add Fund</Button>
          )}
        </View>
        </KeyboardAvoidingView>
    </ScrollView>
    </View>
  )};

export default FundsScreen;

const styles = StyleSheet.create({
  SectionStyle: {
    flexDirection: 'row',
    height: 40,
    marginTop: 20,
    marginLeft: 35,
    marginRight: 35,
    margin: 10,
  },
  buttonStyle: {
    backgroundColor: '#7DE24E',
    borderWidth: 0,
    color: '#FFFFFF',
    borderColor: '#7DE24E',
    height: 40,
    alignItems: 'center',
    borderRadius: 30,
    marginLeft: 35,
    marginRight: 35,
    marginTop: 20,
    marginBottom: 20,
  },
  buttonTextStyle: {
    color: '#FFFFFF',
    paddingVertical: 10,
    fontSize: 16,
  },
  inputStyle: {
    flex: 1,
    color: 'white',
    paddingLeft: 15,
    paddingRight: 15,
    borderWidth: 1,
    borderRadius: 30,
    borderColor: '#dadae8',
  },
  errorTextStyle: {
    color: 'red',
    textAlign: 'center',
    fontSize: 14,
  },
  successTextStyle: {
    color: 'white',
    textAlign: 'center',
    fontSize: 18,
    padding: 30,
  },
});