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
  Alert,
} from 'react-native';
import { Button } from 'react-native-paper';
import Config from '../config';
LINK=Config.LINK

function getFund(email)
{
    const funds_Data_Return = {
      id:0,
      Email:email,
      totalFund:0.0,
      allocatedFund:0.0,
      unusedFund:0.0,
      UpdDate:"",
    };
    apiToCal=LINK+"getFund/"+email
    console.log(apiToCal)
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
      console.log("--------------Found Fund------------")
      console.log(JSON.stringify(responseJson))
    })
    .catch((error) => {
      //Hide Loader
      console.log("--------------error in get Fund------------")
    });
    return funds_Data_Return
}

function FundsScreen (props) {
    const Data = props.route.params.Data;
    const [
        isFundsDataNotAvailable,
        setFundsDataNotAvailable
      ] = useState(true);
    const [
        isUnallocatedFundsAvailable,
        setUnallocatedFundsAvailable
      ] = useState(false);
    var condition=useState(''); // Initial condition
    const [Email, setEmail] = useState(Data.email);
    const emailInputRef = createRef();
    const [totalFund, setTotalFund] = useState(0.0);
    const totalFundInputRef = createRef();
    const [allocatedFund, setAllocatedFund] = useState(0.0);
    const allocatedFundInputRef = createRef();
    const [unusedFund, setUnusedFund] = useState(0.0);
    const unusedFundInputRef = createRef();

    
    funds_Data_Return=getFund(Data.email)
    setFundsDataNotAvailable(funds_Data_Return.id==0 ?false:true)
    if (isFundsDataNotAvailable == false ) { 
      if(funds_Data_Return.unusedFund>0)
          setUnallocatedFundsAvailable(true)
    }
    if((isFundsDataNotAvailable==false) && (isUnallocatedFundsAvailable==true))
      {
        condition='A'
      }
    if((isFundsDataNotAvailable==false) && (isUnallocatedFundsAvailable==false))
      {
        condition='B'
      }
    
    if(isFundsDataNotAvailable) 
    {
      condition='C'
    }
    const calUnusedFund = (value) => {
      setAllocatedFund(value)
      setUnusedFund(totalFund - value)
    };
    const funds_Data_Create = {
      Email:Data.email,
      totalFund:totalFund,
      allocatedFund:allocatedFund,
      unusedFund:unusedFund,
    };
    var IsError=false
    if(isNaN(+totalFund))
    {
      IsError=true
      alert("Enter Valid Number in Total Fund ")
    }
    if(isNaN(+allocatedFund))
      {
        IsError=true
        alert("Enter Valid Number in Allocated Fund")
      }
    if(allocatedFund>totalFund)
    {
      IsError=true
      console.log(funds_Data_Create.totalFund)
      console.log(funds_Data_Create.allocatedFund)
      alert("You can't Allocated more than Total Fund")
    }
    console.log('----------Before addFund------- ')

    console.log(funds_Data_Create.unusedFund)
    
    apiToCal=LINK+"addFund"
    console.log(apiToCal)
    const addFund = () => {
      fetch(apiToCal,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'Access-Control-Allow-Origin':"*",
            'Access-Control-Allow-Methods': "POST",
        },
        body:JSON.stringify(funds_Data_Create),
    })
    .then(resp => resp.json())
    .then((responseJson) => {
      alert('Fund Created Successfully')
      console.log(JSON.stringify(responseJson))
      {props.navigation.navigate('Home',{Data:Data})}
    })
    .catch((error) => {console.log('-----------error in add fund----------') })
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
            onChangeText={(TotalFund) => setTotalFund(TotalFund)}
            underlineColorAndroid="#f000"
            placeholder="Enter Total Funds"
            placeholderTextColor="#8b9cb5"
            autoCapitalize="sentences"
            returnKeyType="next"
            onSubmitEditing={() =>
                allocatedFundInputRef.current && allocatedFundInputRef.current.focus()
            }
            editable={isFundsDataNotAvailable} 
            selectTextOnFocus={isFundsDataNotAvailable} 
            blurOnSubmit={false}
            />
        </View>
        <View style={styles.SectionStyle}>
            <TextInput
            style={styles.inputStyle}
            value={allocatedFund}
            onChangeText={calUnusedFund}
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
            editable={isFundsDataNotAvailable} 
            selectTextOnFocus={isFundsDataNotAvailable} 
            blurOnSubmit={false}
            />
        </View>
        <View style={styles.SectionStyle}>
            <TextInput
            style={styles.inputStyle}
            value={unusedFund}
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
            editable={false} 
            selectTextOnFocus={false} 
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
                    onPress={() => {addFund()}}
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