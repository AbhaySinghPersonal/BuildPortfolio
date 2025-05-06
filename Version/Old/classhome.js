import React, { Component } from 'react';
import { StyleSheet, Text, View,Button,useState } from 'react-native';
export class ClassHome extends Component {
    state = {Name:'A K SINGH'}
    render() {
        return (
          <View>
              <Text>From Class {this.state.Name} </Text>
              <Button title = "Enter" onPress={ () => this.setState({Name:"Wife Pooja"})}/>
          </View>
        );
      }  
}
