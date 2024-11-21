import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import EventManagementForm from '@/components/EventManagement.vue';
import VolunteerMatchingForm from '@/components/VolunteerMatching.vue';
import LoginForm from '@/components/LoginForm.vue';
import ProfileForm from '@/components/ProfileForm.vue';
import RegisterForm from '@/components/RegisterForm.vue';

const routes = [
    { path: '/', name: 'Home', component: HomePage },
    { path: '/profile', name: 'Profile', component: ProfileForm },
    { path: '/event-management', name: 'EventManagement', component: EventManagementForm },
    { path: '/volunteer-matching', name: 'VolunteerMatching', component: VolunteerMatchingForm },
    { path: '/login', name: 'Login', component: LoginForm },
    { path: '/register', name: 'Register', component: RegisterForm },
    { path: '/', redirect: '/login'}
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
