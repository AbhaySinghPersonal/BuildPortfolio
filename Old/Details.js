import React,{useState,useEffect} from 'react';
import { Text, View,StyleSheet,ScrollView } from 'react-native';
import { Button } from 'react-native-paper';


function Details(props) {
  console.log('--------Details---------')
  const data = props.route.params.data;
  console.log(data.id)
  const payload = {
    Title: "",
    Body: "",
  };
  const deleteData = (data) => {
    fetch(`http://192.168.56.1:8081/delete/${data.id}/`,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'Access-Control-Allow-Origin':"*",
            'Access-Control-Allow-Methods': "POST",
        },
        body:JSON.stringify(payload),
    })
    .then(data =>{props.navigation.navigate("Home")
    })
    .catch(error => console.log(error) )
  }

  return (
    <ScrollView>
      <View style={styles.viewStyle}>
        <Text style = {{fontSize:25}}>
          {data.Title}
        </Text>
        <Text style = {{fontSize:20, marginTop:10}}>
          {data.Body}
        </Text>
        <View style={styles.btnStyle}>
          <Button
          style={styles.inputStyle}
          icon="update"
          mode="contained"
          onPress={() => props.navigation.navigate('Edit',{data:data})}
          >Edit</Button>
                  <Button
          style={styles.inputStyle}
          icon="update"
          mode="contained"
          onPress={() => deleteData(data)}
          >Delete</Button>
        </View>
      </View>
      
    </ScrollView>
  );
}  

const styles = StyleSheet.create({
  viewStyle: {
    padding: 10,
    marginTop:10
  },
  btnStyle: {
    padding: 10,
    margin:15,
    flexDirection:"row",
    justifyContent:"space-around"
  },
});

export default Details