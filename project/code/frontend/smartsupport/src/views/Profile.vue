<template>
    <NavBar></NavBar>

    <div class="container my-5">
        <div class="row">
            <div class="col-md-4">
                <img v-bind:src="url" class="img-fluid rounded-circle mb-3" alt="avatars">
                <h1 class="h4">{{ user_details.first_name }} {{ user_details.last_name }}</h1>

                <hr>

            </div>
            <div class="col-md-8">
                <h2 class="h5">User Information</h2>
                <p><strong>User ID:</strong> {{ user_details.user_id }}</p>
                <p><strong>Username:</strong> {{ user_details.username }}</p>
                <!-- <p><strong>Roles:</strong> Web Developer, UX Designer</p> -->
            </div>
        </div>
    </div>
</template>

<script>


import NavBar from '@/components/NavBar.vue';

export default {
    name: "Profile",
    data() {
        return {
            user_details: JSON.parse(localStorage.getItem("user_details")),
            url: `https://api.dicebear.com/6.x/big-ears/svg?size=200&seed=${JSON.parse(localStorage.getItem("user_details")).username}`
        }
    },
    components: {
        NavBar,
    },

};

</script>


<style></style>