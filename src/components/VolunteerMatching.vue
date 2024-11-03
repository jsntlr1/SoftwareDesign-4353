<template>
    <div>
        <h2>Volunteer Matching</h2>
        <form @submit.prevent="matchVolunteer">
            <div>
                <label for="volunteerName">Volunteer Name:</label>
                <input id="volunteerName" v-model="volunteerName" type="text">
            </div>

            <div>
                <label for="matchedEvent">Matched Event:</label>
                <select id="matchedEvent" v-model="matchedEvent">
                    <option value="">Select an event</option>
                    <option value="Marathon">Marathon</option>
                </select>
            </div>

            <button type="submit">Confirm Match</button>
        </form>

        <div v-if="message" class="message">
            {{ message }}
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const volunteerName = ref('');
const matchedEvent = ref('');
const message = ref('');
</script>
