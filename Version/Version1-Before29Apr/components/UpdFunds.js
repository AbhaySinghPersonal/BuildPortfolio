import React, {useState, createRef} from 'react';
import {
  StyleSheet,
  TextInput,
  View,
  Text,
  Image,
  KeyboardAvoidingView,
  ScrollView,
} from 'react-native';
import { Button } from 'react-native-paper';
import Config from '../config';
LINK=Config.LINK
import { commonStyles } from '../styles/commonStyles';

function UpdFundsScreen (props) {
    const inp_fr_par = props.route.params.data;
    console.log("---------Upd Fund---------")
    console.log(JSON.stringify(inp_fr_par))
    const [totalFund, setTotalFund] = useState(inp_fr_par.totalFund);
    const totalFundInputRef = createRef();
    const [allocatedFund, setAllocatedFund] = useState(inp_fr_par.allocatedFund);
    const allocatedFundInputRef = createRef();
    const [unusedFund, setUnusedFund] = useState(inp_fr_par.unusedFund);
    const unusedFundInputRef = createRef();
    const funds_Data_Upd = {
      Email:inp_fr_par.Email,
      totalFund:totalFund,
      allocatedFund:allocatedFund,
      unusedFund:unusedFund,
    };
    var IsError=false
    console.log('----------totalfund----------')
    console.log(totalFund)
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
      alert("You can't Allocated more than Total Fund")
    } 
    
    const updFund = (inp_fr_par) => {
        console.log('----------updFund----------')
        console.log(JSON.stringify(funds_Data_Upd))
        apiToCal=LINK+"updFund"
        console.log(apiToCal)
        if(IsError)
            alert("Some Error, Correct")
            
        fetch(apiToCal,{
            method:'PUT',
            headers:{
                'Content-Type':'application/json',
                'Access-Control-Allow-Origin':"*",
                'Access-Control-Allow-Methods': "PUT",
            },
            body:JSON.stringify(funds_Data_Upd),
        })
        .then(resp => resp.json())
        .then((responseJson) => {
          alert('Fund Updated Successfully')
          console.log(JSON.stringify(responseJson))
          Data=inp_fr_par
          {props.navigation.navigate('Home',{Data:Data})}
        })
        .catch((error) => {console.log('-----------error in add fund----------') })
  }
  const calUnusedFund = (value) => {
    setAllocatedFund(value)
    setUnusedFund(totalFund - value)
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
            value={totalFund}
            onChangeText={(TotalFund) => setTotalFund(TotalFund)}
            underlineColorAndroid="#f000"
            placeholder="Enter Total Funds"
            placeholderTextColor="#8b9cb5"
            autoCapitalize="sentences"
            keyboardType="numeric"
            returnKeyType="next"
            onSubmitEditing={() =>
                allocatedFundInputRef.current && allocatedFundInputRef.current.focus()
            }
            editable={true} 
            selectTextOnFocus={true} 
            />
        </View>
        <View style={commonStyles.SectionStyle}>
            <TextInput
            style={commonStyles.input}
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
            editable={true} 
            selectTextOnFocus={true} 
            />
        </View>
        <View style={commonStyles.SectionStyleTitle}>
          <Text style={commonStyles.titleStyle}>Unused Funds</Text>
        </View>
        <View style={commonStyles.SectionStyle}>
            <TextInput
            style={commonStyles.input}
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
            />
        </View>
        <View style={commonStyles.SectionStyle}>
            <Button
                style={commonStyles.buttonTextStyle}
                mode="contained"
                onPress={() => {updFund(Data)}}
            >Add/Allocate Fund</Button>
        </View>
        </KeyboardAvoidingView>
        </View>
        <View style={commonStyles.SectionStyle}>
          <Text style={commonStyles.tailorStyle}>
            Ahyaasena Yoga{'\n'}Manage Portfolio{'\n'}www.abhyaasenayoga.com
          </Text>
        </View>
    </ScrollView>
)};

export default UpdFundsScreen;

