import React, {useState, createRef} from 'react';
import {
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

function AddFundsScreen (props) {
    const inp_fr_par = props.route.params.inp_fr_par;
    Data=inp_fr_par
    console.log("---------Add Fund---------")
    console.log(JSON.stringify(inp_fr_par))
    const [totalFund, setTotalFund] = useState(0.0);
    const totalFundInputRef = createRef();
    const [allocatedFund, setAllocatedFund] = useState(0.0);
    const allocatedFundInputRef = createRef();
    const [unusedFund, setUnusedFund] = useState(0.0);
    const unusedFundInputRef = createRef();
    const [MFPer, setMFPer] = useState(0.0);
    const MFPerInputRef = createRef();
    const [EQPer, setEQPer] = useState(0.0);
    const EQPerInputRef = createRef();
    const [CMPer, setCMPer] = useState(0.0);
    const CMPerInputRef = createRef();
    const [OPPer, setOPPer] = useState(0.0);
    const OPPerInputRef = createRef();
    const funds_Data_Create = {
      Email:inp_fr_par.email,
      totalFund:totalFund,
      allocatedFund:allocatedFund,
      unusedFund:unusedFund,
      MFPer:MFPer,
      EQPer:EQPer,
      CMPer:CMPer,
      OPPer:OPPer,
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

    const addFund = (Data) => {
        console.log('----------addFund----------')
        console.log("----allocatedFund>totalFund------")
        console.log(allocatedFund)
        console.log(totalFund)
        if(allocatedFund>totalFund)
        {
          IsError=true
          alert("You can't Allocated more than Total Fund")
        } 
        apiToCal=LINK+"addFund"
        console.log(apiToCal)
        Total_Per=Number(MFPer)+Number(EQPer)+Number(CMPer)+Number(OPPer)
        console.log("----Total_Per------")
        console.log(Total_Per)
        if(IsError)
            alert("Some Error, Correct")

        if (!MFPer) {
          alert('Please fill MF %');
        }
        if (!EQPer) {
          alert('Please fill EQ %');
        }
        if (!CMPer) {
          alert('Please fill CM %');
    
        }
        if (!OPPer) {
          alert('Please fill OP %');
        }

        if (Total_Per!=100) {
          alert('Total % of Mutual Fund, Equity, Commodity & Option should be 100');
          return;
        }
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
        <View style={commonStyles.SectionStyleTitle}>
          <Text style={commonStyles.titleStyle}>Total Funds                               Allocated Funds</Text>
        </View>
        <View style={commonStyles.SectionStyle}>
            <TextInput
            style={commonStyles.input}
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
          <Text style={commonStyles.titleStyle}>Unused Funds                           MF %</Text>
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
            <TextInput
            style={commonStyles.input}
            onChangeText={(MFPer) => setMFPer(MFPer)}
            underlineColorAndroid="#f000"
            placeholder="Enter Total FundsEnter % of Total Fund want to utilize in Mutual Fund"
            placeholderTextColor="#8b9cb5"
            autoCapitalize="sentences"
            keyboardType="numeric"
            returnKeyType="next"
            onSubmitEditing={() =>
              MFPerInputRef.current && MFPerInputRef.current.focus()
            }
            editable={true} 
            selectTextOnFocus={true} 
            />
        </View>
        <View style={commonStyles.SectionStyleTitle}>
          <Text style={commonStyles.titleStyle}>Equity %                                    Commodity %</Text>
        </View>
        <View style={commonStyles.SectionStyle}>
            <TextInput
            style={commonStyles.input}
            onChangeText={(EQPer) => setEQPer(EQPer)}
            underlineColorAndroid="#f000"
            placeholder="Enter % of Total Fund want to utilize in Equity"
            placeholderTextColor="#8b9cb5"
            autoCapitalize="sentences"
            keyboardType="numeric"
            returnKeyType="next"
            onSubmitEditing={() =>
              EQPerInputRef.current && EQPerInputRef.current.focus()
            }
            editable={true} 
            selectTextOnFocus={true} 
            />
            <TextInput
            style={commonStyles.input}
            onChangeText={(CMPer) => setCMPer(CMPer)}
            underlineColorAndroid="#f000"
            placeholder="Enter % of Total Fund want to utilize in Commodity"
            placeholderTextColor="#8b9cb5"
            autoCapitalize="sentences"
            keyboardType="numeric"
            returnKeyType="next"
            onSubmitEditing={() =>
              CMPerInputRef.current && CMPerInputRef.current.focus()
            }
            editable={true} 
            selectTextOnFocus={true} 
            />
        </View>
        <View style={commonStyles.SectionStyleTitle}>
          <Text style={commonStyles.titleStyle}>Option & Right %</Text>
        </View>
        <View style={commonStyles.SectionStyle}>
            <TextInput
            style={commonStyles.input}
            onChangeText={(OPPer) => setOPPer(OPPer)}
            underlineColorAndroid="#f000"
            placeholder="Enter % of Total Fund want to utilize in Options & Futures"
            placeholderTextColor="#8b9cb5"
            autoCapitalize="sentences"
            keyboardType="numeric"
            returnKeyType="next"
            onSubmitEditing={() =>
              OPPerInputRef.current && OPPerInputRef.current.focus()
            }
            editable={true} 
            selectTextOnFocus={true} 
            />
        </View>
      
        </KeyboardAvoidingView>
      </View>
      <View style={commonStyles.SectionStyle}>
            <Button
                style={commonStyles.buttonStyle}
                mode="contained"
                onPress={() => {addFund(Data)}}
            >Add Fund</Button>
        </View>
      <View style={commonStyles.SectionStyle}>
        <Text style={commonStyles.tailorStyle}>
          Ahyaasena Yoga{'\n'}Manage Portfolio{'\n'}www.abhyaasenayoga.com
        </Text>
      </View>
    </ScrollView>
)};

export default AddFundsScreen;
