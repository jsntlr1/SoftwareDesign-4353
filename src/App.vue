<template>
    <div id="app">
        <EventManagementForm />
        <VolunteerMatchingForm />
        <LoginForm/>
        <ProfileForm/>
    </div>
</template>

<script setup>
import EventManagementForm from './components/EventManagement.vue'
import VolunteerMatchingForm from './components/VolunteerMatching.vue'
import LoginForm from './components/LoginForm.vue'
import ProfileForm from './components/ProfileForm.vue'
</script>