<template>
    <nav class="topNav">
      <input type="checkbox" id="check" /> <!--invisible checkbox to open notifications box-->
      <label for="check" class="checkbtn">
        <i class="fas fa-bars"></i> <!--icon for smaller screens-->
      </label>
      <label class="logo">Volunteering</label>

      <ul>
        <!--displays the number of unread notifications-->
        <li class= "nav-item dropdown">
          <a href="#" @click.prevent="toggleDropdown" class="dropdown-toggle">
            Notifications <span v-if="unreadCount > 0" class="badge"> {{ unreadCount }}</span>
          </a>

          <!--Displays the unread notifications if there are any-->
          <div v-if="showDropdown" class="dropdown-menu">
            <h4 class="dropdown-header">Notifications</h4>
            <div v-if="unreadNotifications.length === 0" class="dropdown-items"> No new notifications</div>
            <div v-else>
              <a
                v-for="notification in unreadNotifications"
                :key="notification.id"
                href="#"
                class="dropdown-item"
                @click="markAsRead(notification.id)"
                >
                {{ notification.message }}
              </a>
            </div>
            <!--view past notifications-->
            <div class="dropdown-driver"></div>
            <a href="#" class="dropdown-item text-center" @click.prevent="viewAllNotifications"><u>View All Notifications</u></a>
          </div>
        </li>
        <li><a href="#">Settings</a></li>
      </ul>
    </nav>

    <!-- pop up to display past notifications-->
    <div v-if="showAllNotifications" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>All Notifications</h3>
        <ul>
          <li
            v-for="notification in allNotifications"
            :key="notification.id"
            :class="{ read: notification.read }"
          >
            {{ notification.message }}
          </li>
        </ul>
        <button @click="closeModal">Close</button>
      </div>
    </div>

</template>

<script>
import { ref, onMounted } from 'vue';
export default {
  name: 'HomePage',
  setup() {
    const unreadNotifications = ref([]);
    const allNotifications = ref([]);
    const unreadCount = ref(0);
    const showDropdown = ref(false);
    const showAllNotifications = ref(false);

    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value;
      if (showDropdown.value) {
        fetchUnreadNotifications();
      }
    };

    const fetchUnreadNotifications = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/get_notifications');
        const data = await response.json();
        unreadNotifications.value = data.notifications;
        unreadCount.value = unreadNotifications.value.length;
      }catch(error) {
        console.log("ERROR fetching unread notifications:", error);
      }
    };

    const fetchAllNotifications = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/get_notifications');
        const data = await response.json();
        allNotifications.value = data.notifications;
      }catch(error) {
        console.error("ERROR fetching notifications", error)
      }
    }

    const markAsRead = async (notificationID) => {
      try {
        await fetch('http://localhost:5000/api/mark_notification_read', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ notification_id: notificationID }),
        });
        unreadNotifications.value = unreadNotifications.value.filter (
          (n) => n.id !== notificationID
        );
        unreadCount.value = unreadNotifications.value.length;
      }catch (error) {
        console.error("Error marking notification as read", error);
      }
    };

    const viewAllNotifications = async () => {
      await fetchAllNotifications();
      showAllNotifications.value = true;
    };

    const closeModal = () => {
      showAllNotifications.value = false;
    };

    onMounted (() => {
      fetchUnreadNotifications();
    });

    return {
      unreadNotifications,
      allNotifications, 
      unreadCount,
      showAllNotifications,
      showDropdown,
      toggleDropdown,
      markAsRead,
      viewAllNotifications,
      closeModal,
    };
  },
};
</script>

<style scoped>
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

body {
  font-family: "Montserrat", sans-serif;
}

nav {
  background: black;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

nav .logo {
  color: white;
  font-size: 35px;
  font-weight: bold;
}

nav ul {
  display: flex;
  align-items: center;
}

nav ul li {
  position: relative;
  margin: 0 10px;
}

nav ul li a {
  color: white;
  font-size: 17px;
  padding: 7px 13px;
  text-transform: uppercase;
  border-radius: 3px;
  transition: background 0.5s;
}

nav ul li a:hover,
nav ul li a.active {
  background: gray;
}

/* Badge */
.badge {
  background-color: red;
  color: white;
  padding: 2px 6px;
  border-radius: 50%;
  font-size: 12px;
}

/* Hamburger Menu Button */
.checkbtn {
  font-size: 30px;
  color: white;
  display: none;
  cursor: pointer;
}

#check {
  display: none;
}

/* Dropdown Menu */
.dropdown-menu {
  position: absolute;
  top: 100%; /* Position below the parent */
  right: 0;
  background-color: white;
  min-width: 250px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-menu .dropdown-header {
  font-weight: bold;
  padding: 8px 16px;
}

.dropdown-menu .dropdown-item {
  padding: 12px 16px;
  cursor: pointer;
  color: black;
}

.dropdown-menu .dropdown-item:hover {
  background-color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}

.modal-content h3 {
  margin-top: 0;
}

.modal-content ul {
  list-style: none;
  padding: 0;
}

.modal-content li {
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
}

.modal-content li.read {
  color: gray;
}

.modal-content button {
  margin-top: 20px;
}

/* Media Query for Smaller Screens */
@media (max-width: 858px) {
  nav {
    flex-wrap: wrap;
  }

  nav .logo {
    font-size: 30px;
    padding-left: 0;
    margin-bottom: 10px;
  }

  .checkbtn {
    display: block;
  }

  nav ul {
    flex-direction: column;
    position: fixed;
    top: 80px;
    left: -100%;
    width: 100%;
    background: black;
    text-align: center;
    transition: left 0.5s;
  }

  nav ul li {
    margin: 20px 0;
  }

  nav ul li a {
    font-size: 20px;
  }

  #check:checked ~ ul {
    left: 0;
  }

  /* Dropdown Menu Adjustments */
  .dropdown-menu {
    position: static;
    background-color: black;
    box-shadow: none;
  }

  .dropdown-menu .dropdown-item {
    color: white;
  }

  .dropdown-menu .dropdown-item:hover {
    background-color: black;
  }
}
</style>
