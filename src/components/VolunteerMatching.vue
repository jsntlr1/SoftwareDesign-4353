<template>
    <div>
        <h2>Volunteer Matching</h2>
        <form @submit.prevent="matchVolunteer">
            <div>
                <label for="volunteerName">Volunteer Name:</label>
                <input id="volunteerName" v-model="volunteerName" type="text" readonly>
            </div>

            <div>
                <label for="matchedEvent">Matched Event:</label>
                <input id="matchedEvent" v-model="matchedEvent" type="text" readonly>
            </div>

            <button type="submit">Confirm Match</button>
        </form>

        <div v-if="message" class="message">
            {{ message }}
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const volunteerName = ref('');
const matchedEvent = ref('');
const message = ref('');
