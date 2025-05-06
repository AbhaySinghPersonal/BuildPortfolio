import React, {useState, createRef,useEffect} from 'react';
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
  Alert,FlatList,
} from 'react-native';
import { Button } from 'react-native-paper';
import Config from '../config';
LINK=Config.LINK
import { commonStyles } from '../styles/commonStyles';


function ProposalScreen (props) {
    const inp_fr_par = props.route.params.Data;
    const [data,setData] = useState([])
    apiToCal=LINK+"getProposedFund/"+inp_fr_par.id
    console.log(apiToCal)
    resp=null
    useEffect(() => 
      {
        fetch(apiToCal, {
          method: 'GET',
          headers: {
            'Content-Type':'application/json'
          },
        })
        .then(resp => resp.json())
        .then(
          Proposed =>{setData(Proposed)
        })
      },[]  );
    console.log('--------after get Proposed Fund---------')
    console.log(JSON.stringify(data))
    let BuySelMap= {
      'B': "BUY",
      'S': 'SELL'
    };
    const renderItem = ({ item }) => (
        <View style={commonStyles.inputStyle}>
          <Text style={commonStyles.titleStyle}>ISIN:            {item.ISIN}</Text>
          <Text style={commonStyles.titleStyle}>FundPrice:   {item.FundPrice}</Text>
          <Text style={commonStyles.titleStyle}>UNITS:         {item.Units}</Text>
          <Text style={commonStyles.titleStyle}>BUY/SELL:   {BuySelMap[item.BUY_SELL]}</Text>
        </View>
      );
    
      return (
        <ScrollView contentContainerStyle={commonStyles.scrollView}
              keyboardShouldPersistTaps="handled"
        >
          <KeyboardAvoidingView enabled>
            <View style={{alignItems: 'center'}}>
              <Image
                source={require('../Image/logo.png')}
                style={commonStyles.ImgStyle}
              />
            </View>
            <View style={commonStyles.container}>
              <FlatList
                data={data} // Pass the data array
                renderItem={renderItem} // Render each item using this function
                keyExtractor={(item) => item.ISIN} // Unique key for each item
              />
            </View>
        </KeyboardAvoidingView>
          <View style={commonStyles.SectionStyle}>
            <Text style={commonStyles.tailorStyle}>
              Ahyaasena Yoga{'\n'}Manage Portfolio{'\n'}www.abhyaasenayoga.com
            </Text>
          </View>
      </ScrollView>
  )};

export default ProposalScreen;

