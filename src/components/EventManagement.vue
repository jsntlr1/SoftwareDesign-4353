<template>

    <div v-if="formSubmitted">
        &#128077; Success!
    </div>

    <form @submit.prevent="submitForm">
        <div>
            <label for="eventName">Event Name:</label>
            <input id="eventName" v-model="eventName" type="text" maxlength="100" required>
        </div>

        <div>
            <label for="eventDescription">Event Description: (Min 10 chars)</label>
            <textarea id="eventDescription" v-model="eventDescription" required></textarea>
        </div>

        <div>
            <label for="location">Location:</label>
            <textarea id="location" v-model="location" required></textarea>
        </div>

        <div>
            <label for="requiredSkills">Required Skills:</label>
            <select id="requiredSkills" v-model="requiredSkills" multiple required>
                <option value="communication">Communication</option>
                <option value="teamwork">Teamwork</option>
                <option value="leadership">Leadership</option>
                <option value="problem-solving">Problem Solving</option>
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
import axios from 'axios';

const eventName = ref('');
const eventDescription = ref('');
const location = ref('');
const requiredSkills = ref([]);
const urgency = ref('');
const eventDate = ref('');
const formSubmitted = ref(false);

//validations
const isFormValid = () => {
    return (
        eventName.value &&
        eventDescription.value.length >= 10 &&
        location.value &&
        requiredSkills.value.length > 0 &&
        urgency.value &&
        eventDate.value
    );
};

const submitForm = async () => {
    if (!isFormValid()) {
        return;
    }

    const formattedEventDate = eventDate.value;

    const eventData = {
        eventName: eventName.value,
        eventDescription: eventDescription.value,
        location: location.value,
        requiredSkills: requiredSkills.value,
        urgency: urgency.value,
        eventDate: formattedEventDate,
    };

    try {
        const response = await axios.post('http://localhost:5000/api/events', eventData)
        console.log('Event submitted successfully:', response.data)
        formSubmitted.value = true;

        eventName.value = '';
        eventDescription.value = '';
        location.value = '';
        requiredSkills.value = [];
        urgency.value = '';
        eventDate.value = '';
    }catch (error) {
        console.error("ERROR submitting event:", error);
        alert("Error occurred while trying to submit an event")
    }
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