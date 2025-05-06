// Example of Splash, Login and Sign Up in React Native
// https://aboutreact.com/react-native-login-and-signup/

// Import React and Component
import React, {useState,useEffect} from 'react';
import {
  StyleSheet,
  TextInput,
  View,
  Text,
  ScrollView,
  Image,
  Keyboard,
  TouchableOpacity,
  KeyboardAvoidingView,
} from 'react-native';
import Config from '../config';
LINK=Config.LINK
import { commonStyles } from '../styles/commonStyles';

function RecommendScreen  (props) {
    const [ISIN, setISIN] = useState("");
    const [Date, setDate] = useState("");
    const [result, setResult] = useState({ long: "", short: "" });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [fetchTrigger, setFetchTrigger] = useState(false); // Trigger for useEffect
    apiToCal=LINK+"Recommend"
    var dataToSend = {ISIN: ISIN, Date: Date};
    useEffect(() => {
        const fetchData = async () => {
          if (!fetchTrigger) return; // Skip on initial render
          setLoading(true);
          setError("");
    
          try {
            const response = await fetch(apiToCal, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(dataToSend),
            });
    
            if (!response.ok) {
              throw new Error("Failed to fetch data from the server");
            }
    
            const data = await response.json();
            alert(data['BuySellRecommend'])
          } catch (err) {
            setError(err.message);
          } finally {
            setLoading(false);
            setFetchTrigger(false); // Reset fetch trigger
          }
        };
    
        fetchData();
      }, [fetchTrigger, ISIN, Date]); // Dependencies to watch
    
      const handleSubmit = (e) => {
        e.preventDefault();
        if (ISIN && Date) {
          setFetchTrigger(true); // Trigger useEffect
        } else {
          setError("Both ISIN and Date are required");
        }
      };
  return (
        <ScrollView contentContainerStyle={commonStyles.scrollView}
          keyboardShouldPersistTaps="handled"
        >
        <View>
          <KeyboardAvoidingView enabled>
            <View style={commonStyles.SectionStyleTitle}>
              <Text style={commonStyles.titleStyle}>ISIN</Text>
            </View>
            <View style={commonStyles.SectionStyle}>
              <TextInput
                style={commonStyles.input}
                onChangeText={(ISIN) =>
                  setISIN(ISIN)
                }
                placeholder="Enter ISIN" 
                placeholderTextColor="#8b9cb5"
                autoCapitalize="none"
                returnKeyType="next"
                underlineColorAndroid="#f000"
              />
            </View>
            <View style={commonStyles.SectionStyleTitle}>
              <Text style={commonStyles.titleStyle}>Date(YYYY-MM-DD)</Text>
            </View>
            <View style={commonStyles.SectionStyle}>
              <TextInput
                style={commonStyles.input}
                onChangeText={(Date) =>
                  setDate(Date)
                }
                placeholder="Enter Date on Which want system to recommend" //12345
                placeholderTextColor="#8b9cb5"
                keyboardType="default"
                underlineColorAndroid="#f000"
                returnKeyType="next"
              />
            </View>
            <TouchableOpacity
              style={commonStyles.buttonStyle}
              activeOpacity={0.5}
              onPress={handleSubmit}>
              <Text style={commonStyles.buttonTextStyle}>Find</Text>
            </TouchableOpacity>
          </KeyboardAvoidingView>
        </View>
      </ScrollView>
  );
};
export default RecommendScreen;