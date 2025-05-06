import React,{useState,useEffect} from 'react';
import {  Text, View,StyleSheet,FlatList } from 'react-native';
import { TextInput,Button } from 'react-native-paper';

function Create(props) {
  console.log('--------Create---------')
  const [title,setTitle] = useState("")
  const [body,setBody] = useState("")
  const payload = {
    Title: title,
    Body: body,
  };
  const insertData = () => {
    fetch('http://192.168.56.1:8081/add',{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify(payload),
    })
    .then(resp => resp.json())
    .then(data =>{props.navigation.navigate("Home")
    })
    .catch(error => console.log(error) )

  }
  return (
    <View>
        <TextInput style={styles.inputStyle}
        label="Title"
        value={title}
        mode="outlined"
        onChangeText={text => setTitle(text)}
        />
        <TextInput style={styles.inputStyle}
        label="Description"
        value={body}
        mode="outlined"
        multiline
        numberOfLines={10}
        onChangeText={text => setBody(text)}
        />
        <Button
        style={styles.inputStyle}
        icon="pencil"
        mode="contained"
        onPress={() => insertData()}
        >Insert article</Button>
    </View>
  );
}  
const styles = StyleSheet.create({
    inputStyle: {
      padding: 10,
      marginTop:30
    },
  });
  
export default Create