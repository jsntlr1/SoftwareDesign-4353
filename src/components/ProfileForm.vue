<template>
    <div class="profile">
      <!--<h1>Profile</h1>-->
      hello, {{ profile.fullName }}
  
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
            <DatePicker
              v-model = "profile.availability"
              multiple
              :close-on-select="false"
              format = "MM/dd/yyyy"
              placeholder = "Select availability"
              required
              />
            <div class="selected-items">Selected Dates: {{ formattedDates.join(', ') }}</div>
        </div>

        <!--submit-->
        <div>
          <button type="submit">Submit</button>
        </div>

      </form>
    </div>
  </template>
  
  
  <script setup>
  import { ref } from 'vue';
  import DatePicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css';
  import axios from 'axios';
  import { computed } from 'vue';
  
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
  const formSubmitted = ref(false);
  
  const states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
  ];

  
  const formattedDates = computed(() => {
  const availability = profile.value.availability;

  if (!Array.isArray(availability) || availability.length === 0) {
    return [];
  }

  return availability.map(date => {
    return new Date(date).toLocaleDateString('en-US');
  });
});

  
  const handleSubmit = async () => {
    console.log("Attempting to submit profile data...");
    try {
      profile.value.skills = multiSelected.value;
      
      const response = await axios.post('http://localhost:5000/api/profile', profile.value)
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
  
  </style>
  