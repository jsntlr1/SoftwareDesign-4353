<template>
    <form @submit.prevent="submitForm">
        <div>
            <label for="eventName">Event Name:</label>
            <input id="eventName" v-model="eventName" type="text" maxlength="100" required>
        </div>

        <div>
            <label for="eventDescription">Event Description:</label>
            <textarea id="eventDescription" v-model="eventDescription" required></textarea>
        </div>

        <div>
            <label for="location">Location:</label>
            <textarea id="location" v-model="location" required></textarea>
        </div>

        <div>
            <label for="requiredSkills">Required Skills:</label>
            <select id="requiredSkills" v-model="requiredSkills" multiple required>
                <option value="communication">Communication (Placeholder)</option>
                <option value="teamwork">Teamwork (Placeholder)</option>
                <option value="leadership">Leadership (Placeholder)</option>
                <option value="problem-solving">Problem Solving (Placeholder)</option>
            </select>
        </div>

        <div>
            <label for="urgency">Urgency:</label>
            <select id="urgency" v-model="urgency" required>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
            </select>
        </div>

        <div>
            <label for="eventDate">Event Date:</label>
            <input id="eventDate" v-model="eventDate" type="date">
        </div>

        <button type="submit">Create Event</button>
    </form>
</template>

<script setup>
import { ref } from 'vue';

const eventName = ref('');
const eventDescription = ref('');
const location = ref('');
const requiredSkills = ref([]);
const urgency = ref('');
const eventDate = ref('');

const submitForm = () => {

    console.log({
        eventName: eventName.value,
        eventDescription: eventDescription.value,
        location: location.value,
        requiredSkills: requiredSkills.value,
        urgency: urgency.value,
        eventDate: eventDate.value
    });

    eventName.value = '';
    eventDescription.value = '';
    location.value = '';
    requiredSkills.value = [];
    urgency.value = '';
    eventDate.value = '';
};
</script>

<style scoped>
form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 500px;
    margin: 0 auto;
}

label {
    font-weight: bold;
}

input,
textarea,
select {
    width: 100%;
    padding: 0.5rem;
}

button {
    padding: 0.5rem 1rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
</style>