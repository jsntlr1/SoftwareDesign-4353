<template>
    <div class="login">
      <div class="login-box">
        <h1>{{ isRegistering ? "Register" : "Login" }} </h1>
  
        <form @submit.prevent="handleSubmit">
  
            <!--Email-->
            <div>
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="email" required />
            </div>
  
            <!--Password-->
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
  
            <!--Confirm Password for registration-->
            <div v-if="isRegistering">
                <label for="confirmPassword"> Confirm Password:</label>
                <input type="password" id="confirmPassword" v-model="confirmPassword" required />
            </div>
            <!--Error-->
            <p v-if="errorMessage" class="error-message"> {{ errorMessage }}</p>
  
            <!--Submit-->
            <button type="submit"> {{ isRegistering ? "Register" : "Login" }}</button>
        </form>
  
        <!--Switch between login and register-->
        <p class="toggle-link">
            <a href="#" @click.prevent="toggleForm"> {{ isRegistering ? "Already have an account? Login here." : "Don't have an account? Register here." }}
            </a>
        </p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const isRegistering = ref(false);
  const email = ref("");
  const password = ref("");
  const confirmPassword = ref("")
  const errorMessage = ref("");
  
  function toggleForm() {
    isRegistering.value = !isRegistering.value;
    clearForm();
  }
  
  function handleSubmit() {
    if (isRegistering.value) {
        if (password.value !== confirmPassword.value) {
            errorMessage.value = "Passwords do not match";
            return;
        }
  
        console.log("Registered:", {
            email: email.value,
            password: password.value,
        });
        alert("Registration Success, please log in.");
  
        isRegistering.value = false;
        clearForm();
    } else {
        console.log("Logged in:", {
            email: email.value,
            password: password.value,
        });
        alert("Login success");
        clearForm();
    }
  }
  
  function clearForm() {
    email.value = "";
    password.value = "";
    confirmPassword.value = "";
    errorMessage.value = "";
  }
  </script>
  
  <style>
    
    .login {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 400px;
        width: 100%;
    }
  
    .login-box {
        border: 1px solid black;
        padding: 20px;
        border-radius: 5px;
        max-width: 400px;
    }
  
    h1 {
        text-align: center;
        margin-bottom: 20px;
    }
  
    form div {
        margin-bottom: 15px;
    }
  
    input {
        width: 100%;
        padding: 8px;
        box-sizing: border-box;
    }
  
    button {
        width: 100%;
        padding: 10px;
        background-color: lightgreen;
        color: white;
        cursor: hand;
        border-radius: 4px;
    }
  
    button:hover {
        background-color: green;
    }
  
    .toggle-link {
        text-align: center;
        margin-top: 15px;
        color: green;
    }
  
    .toggle-link:hover {
        text-decoration: underline;
    }
  
    .error-message {
        color: red;
        text-align: center;
    }
  
  </style>