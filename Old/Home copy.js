

import React,{useState,useEffect} from 'react';
import {  Text, View,StyleSheet,Button,FlatList } from 'react-native';
import { Card, Title,FAB } from 'react-native-paper';

function Home(props) {
  console.log('--------Home---------')
  const [data,setData] = useState([])
  const [loading,setIsloading] = useState (true)
  resp=article=null
  useEffect(() => 
  {
    fetch('http://192.168.56.1:8081/get',{method:'GET'})
      .then(resp => resp.json())
      .then(
        article =>{setData(article)
        setIsloading(false)
      })
  },[]  );
  const clickedItem = (data) => {
    props.navigation.navigate('Details',{data:data})
  }
  
  const renderData=(item)=> {
    return (  
        <Card style={styles.cardStyle}>
          <Text style={{fontSize:50}} onPress = {() => clickedItem(item)}>{item.Title}</Text>
        </Card>
    )
  }
  return (
    <View styles={{flex:1}}>
      <FlatList
      data={data}
      renderItem={  ({item}) => {
        return renderData(item)
       }
      }
       keyExtractor={item=>`${item.ID}`}
      />
      
      <FAB
      style={styles.fab}
      small = {false}
      icon="plus"
      theme={{colors:{accent:"green"}}}
      onPress = {() => props.navigation.navigate('Create')}
      />

    </View>
  );
}

const styles = StyleSheet.create({
    cardStyle: {
        padding:10,
        margin:10
    },
    fab: {
      position:'absolute',
      margin:16,
      right:0,
      bottom:-100
  },
});
  
export default Home