<template>
    <div>
        <h2>Volunteer Matching</h2>
        <form @submit.prevent="fetchAvailableEvents">
            <div>
                <label for="volunteerName">Volunteer Name:</label>
                <input id="volunteerName" v-model="volunteerName" type="text">
            </div>
            <button type="submit">Find events</button>
        </form>

        <div v-if="events.length > 0">
            <h3>Events matching your available dates</h3>
            <div>
                <label for="matchedEvent">>Select an event:</label>
                <select id="matchedEvent" v-model="selectedEventId" required>
                    <option value="">Select and event</option>
                    <option v-for="event in events" :key="event.id" :value="event.id">
                        {{ event.name }} on {{ formatDate(event.date) }}
                    </option>
                </select>
            </div>
            <button @click="registerForEvent">Register for event</button>
        </div>

        <div v-if="message" class="message">
            {{ message }}
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const volunteerName = ref('');
const volunteerId = ref(null);
const events = ref([]);
const selectedEventId = ref('');
const message = ref('');

const fetchAvailableEvents = async () => {
    if (!volunteerName.value) {
        message.value = "You must enter name";
        return;
    }

    try {
        const response = await axios.post('http://localhost:5000/api/available_events', {
            volunteerName: volunteerName.value
        });
        volunteerId.value = response.data.volunteerId;
        events.value = response.data.events;
        console.log('Recieved events:', events.value)

        if (events.value.length === 0) {
            message.value = 'No matching events found for your selected available dates';
        }else {
            message.value = '';
        }
    }catch (error) {
        console.error('Error while trying to fetch available events:', error)
        message.value = "Error while trying to fetch available events";
    }
};

const registerForEvent = async () => {
    if (!volunteerId.value) {
        message.value = "volunteer ID not found";
        return;
    }

    if (!selectedEventId.value) {
        message.value = "you must select an event";
        return;
    }

    try {
        const response = await axios.post('http://localhost:5000/api/match', {
            volunteerId: volunteerId.value,
            eventId: selectedEventId.value
        });
        message.value = response.data.message;
    }catch (error) {
        console.error("Error while trying to register for event:", error);
        console.log("Error details:", error);

        if (error.response && error.response.data && error.response.data.message) {
            message.value = error.response.data.message;
        }else {
            message.value = "An error occured while registering for the event";
        }
    }
};

const formatDate = (dateString) => {
    return dateString;
};
</script>
