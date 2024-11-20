<template>
    <div class="login">
        <div class="login-box">
            <h1>Register</h1>

            <form @submit.prevent="handleSubmit">
                <div>
                    <label for="email">Email:</label>
                    <input type="email" id="email" v-model="email" required />
                </div>

                <div>
                    <label for="password">Password:</label>
                    <input type="password" id="password" v-model="password" required />
                </div>

                <div>
                    <label for="confirmPassword">Confirm Password:</label>
                    <input type="password" id="confirmPassword" v-model="confirmPassword" required />
                </div>

                <p v-if="errorMessage" class="error-message"> {{ errorMessage }}</p>

                <button type="submit">Register</button>
            </form>

            <p class="toggle-link">
                <router-link to="/login">Click here to login</router-link>
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");
const router = useRouter();

function handleSubmit() {
    if (password.value !== confirmPassword.value) {
        errorMessage.value = "Passwords do not match.";
        return;
    }

    console.log('Registered:', {
        email: email.value,
        password: password.value,
    });

    alert("Registration successful");

    email.value = "";
    password.value = "";
    confirmPassword.value = "";
    errorMessage.value = "";

    router.push('/login')
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