import React, {useState,useEffect} from 'react';
import {  View} from 'react-native';
import Config from '../config';
LINK=Config.LINK

function FundsScreen (props) {
    const inp_fr_par = props.route.params.Data;
    const [data,setData] = useState([])
    apiToCal=LINK+"getFund/"+inp_fr_par.id
    //apiToCal=LINK+"getFund"
    console.log(apiToCal)
    resp=article=null
    
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
          Funds =>{setData(Funds)
        })
      },[]  );
    console.log('--------after get---------')
    console.log(JSON.stringify(data))
    if(typeof(data.id) == 'undefined') 
    {
      {props.navigation.navigate('AddFunds',{inp_fr_par:inp_fr_par})}
    }
    else
    {
      data.UsrId=inp_fr_par.id
      {props.navigation.navigate('UpdFunds',{data:data})}
    }
 
  return (
    <View > </View>
  )};

export default FundsScreen;
