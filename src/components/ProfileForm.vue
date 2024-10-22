<template>
    <div class="profile">
      <!--<h1>Profile</h1>-->
      Hello, {{ profile.fullName }}
  
      <!--Link to home-->
      <router-link to="/">Home</router-link>
  
      <div v-if="formSubmitted">
        &#128077; Success!
      </div>
  
      <form @submit.prevent="handleSubmit">
  
      <!--Full name-->
        <div>
          <label for="fullName">Full name:</label>
          <input type = "text" id="fullName" name="fullName" v-model="profile.fullName" maxlength="50" required />
        </div>
  
        <!--Address 1-->
        <div>
          <label for="address1">Address 1:</label>
          <input type="text" id="address1" name="address1" v-model="profile.address1" maxlength="100" required />
        </div>
  
        <!--Adress 2-->
        <div>
          <label for="Address2">Address 2 (Optional):</label>
          <input type="text" id="address2" name="address2" v-model="profile.address2" maxlength="100" />
        </div>
  
        <!--City-->
        <div>
          <label for="city">City:</label>
          <input type="text" id="city" name="city" v-model="profile.city" maxlength="100" required />
        </div>
  
        <!--State-->
        <div>
          <label for="state">State:</label>
          <select id="state" name="state" v-model="profile.state" required>
            <option value="" disabled>Select state</option>
            <option v-for="state in states" :key="state" :value="state"> {{ state }}</option>
            <!-- DB will store 2 character state code-->
          </select>
        </div>
  
        <!--Zip Code-->
        <div>
          <label for="zipCode">Zip Code:</label> <!-- 9 characters, at least 5 characters required-->
          <input type="text" id="zipCode" name="zipCode" v-model="profile.zipCode" maxLength="9" minlength="5" required />
        </div>
  
        <!--Skills-->
        <div>
          <label for="skills">Skills:</label>
          <select v-model="multiSelected" multiple required>
            <option>Promptness</option>
            <option>Teamwork</option>
            <option>Data Entry</option>
            <option>Social</option>
          </select>
          <div class="selected-items">Selected Skills: {{ multiSelected.join(", ") }}
          </div>
        </div>
  
        <!--Preferences-->
        <div>
          <label for="preferences">Preferences: (Optional)</label>
          <textarea id="preferences" name="preferences" v-model="profile.preferences" rows="4" cols="50" placeholder="Preferences..."></textarea>
        </div>
  
        <!--Availability Date-->
        <div>
            <label for="availability">Availability:</label>
            <VueDatePicker
              v-model = "selectedDate"
              :close-on-select="false"
              format="MM/dd/yyyy"
              placeholder = "Select availability"
              required
              />

              <button type="button" @click="addDate">Save Date</button>

              <div class="selected-items" v-if="profile.availability.length">
                <p>Selected Dates:</p>
                <ul>
                  <li v-for="(date, index) in profile.availability" :key="index">
                  {{ formatDate(date) }}
                  <button type="button" @click="removeDate(index)">Remove</button>
                  </li>
                </ul>
              </div>
        </div>

        <!--submit-->
        <div>
          <button type="submit" :disables="!profile.availability.length" class="submitbtn">Submit</button>
        </div>

      </form>
    </div>
  </template>
  
  
  <script setup>
  import { ref } from 'vue';
  import VueDatePicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css';
  import axios from 'axios';
  
  const profile = ref({
    fullName: "",
    address1: "",
    address2: "",
    city: "",
    state: "",
    zipCode: "",
    preferences: "",
    availability: [],
    skills: [],
  });
  
  const multiSelected = ref([]);
  const selectedDate = ref(null);
  const formSubmitted = ref(false);
  
  const states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'];

  const addDate = () => {
    if (selectedDate.value) {
      if (!profile.value.availability.some((date) => date.getTime() === selectedDate.value.getTime())) {
        profile.value.availability.push(new Date(selectedDate.value));
        selectedDate.value = null;
      } else {
          alert("Date already added");
      }
    }else {
        alert("You must select a date");
    }
  };

  const removeDate = (index) => {
    profile.value.availability.splice(index, 1);
  };


  const formatDate = (date) => {
    if(!(date instanceof Date)) return '';
    const options = { month: '2-digit', day: '2-digit', year: 'numeric' };
    return date.toLocaleDateString(undefined, options);
  };


  const handleSubmit = async () => {
    console.log("Attempting to submit profile data...");
    if (!profile.value.availability.length) {
      alert("Must select a date.");
      return;
    }
    try {
      profile.value.skills = multiSelected.value;
      const availabilityFormatted = profile.value.availability.map((date) => date.toISOString());

      const profileData = {
        ...profile.value,
        availability: availabilityFormatted,
      };
      
      const response = await axios.post('http://127.0.0.1:5000/api/profile', profileData);
      console.log('Profile data submitted successfully:', response.data);
      formSubmitted.value = true; 
      console.log("Profile Data:", profile.value)
    }catch (error) {
      console.error("ERROR submitting profile data", error);
    }
  };
  </script>
  
  <style>
    form {
      border: 1px solid black;
      padding: 20px;
      border-radius: 5px;
    }
  
  
    .profile {
      max-width: 600px;
      margin: 50px auto;
    }
  
    .back-link {
      text-align: center;
      margin-bottom: 20px;
      color: lightgreen;
    }
    
    .back-link:hover{
      text-decoration: underline;
      color: green;
    }
  
    form div {
      margin-bottom: 15px;
    }

    input, select, textarea, button {
      width: 100%;
      padding: 8px;
      margin-top: 5px;
      border: 1px solid beige
    }
  
    button {
      background-color: lightgreen;
      color: fff;
      border: none;
      cursor: pointer;
      border-radius: 4px;
      padding: 10px;
    }
  
    button:hover {
      background-color: green;
    }
  
    .selected-items {
      margin-top: 10px;
    }

    .submitbtn {
      background-color: lightgreen;
      padding: 5px 10px;
      border-radius: 4px;
      width: auto;
    }

    .submitbtn:hover {
      background-color: green;
    }
  
  </style>
  