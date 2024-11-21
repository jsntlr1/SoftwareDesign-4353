<template>
    <div id="app">
        <nav>
            <router-link to="/">Home</router-link> |
            <router-link to="/event-management">Event Management</router-link> |
            <router-link to="/volunteer-matching">Volunteer Matching</router-link> |
            <router-link to="/login">Login</router-link> |
            <router-link to="/profile">Profile</router-link> |
            <router-link to="/register">Register</router-link>
        </nav>
        <router-view></router-view>
    </div>
</template>