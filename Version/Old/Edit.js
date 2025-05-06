import React,{useState,useEffect} from 'react';
import {  Text, View,StyleSheet,FlatList } from 'react-native';
import { TextInput,Button } from 'react-native-paper';

function Edit(props) {
  console.log('--------Edit---------')
  const data = props.route.params.data;
  console.log(data.Title)
  const [title,setTitle] = useState(data.Title)
  const [body,setBody] = useState(data.Body)
  const payload = {
    Title: title,
    Body: body,
  };
  const updateData = () => {
    fetch(`http://192.168.56.1:8081/update/${data.id}`,{
        method:'PUT',
        headers:{
            'Content-Type':'application/json',
            'Access-Control-Allow-Origin':"*",
            'Access-Control-Allow-Methods': "POST, GET, PATCH, PUT, OPTIONS",
        },
        body:JSON.stringify(payload),
    })
    .then(resp => resp.json())
    .then(data =>{props.navigation.navigate("Home",{data:data})
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
        icon="update"
        mode="contained"
        onPress={() => updateData()}
        >Update article</Button>
    </View>
  );
}  
const styles = StyleSheet.create({
    inputStyle: {
      padding: 10,
      marginTop:30
    },
  });
  
export default Edit