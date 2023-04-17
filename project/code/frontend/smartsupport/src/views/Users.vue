<template>
    <div class="container mt-4">
        <div class="row">
            <div class="col">
                <div class="d-flex flex-column justify-content-right align-items-left">
                    <h2> Tickets</h2>



                    <table class="table table-borderless table-group-divider">
                        <thead>
                            <tr>
                                <th>User ID</th>
                                <th>Username</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Roles</th>

                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in user_list">

                                <td>{{ user.user_id }}</td>
                                <td>{{ user.username }}</td>
                                <td>{{ user.first_name }} {{ user.last_name }}</td>
                                <td>{{ user.email }}</td>

                                <!-- <td>
                                    <label class="role-label" v-for="role in roles" :key="role.role_id">
                                        <input type="checkbox"
                                            :checked="user.roles.some(userRole => userRole.role_id === role.role_id)"
                                            v-model="user.roles" :value="role">
                                        {{ role.name }}
                                    </label>
                                </td> -->
                                <td>
                                    <label class="role-label" v-for="role in roles" :key="role.role_id">
                                        <input type="checkbox"
                                            :checked="user.roles.some(userRole => userRole.role_id === role.role_id)"
                                            v-model="user.roles" :value="role"
                                            :disabled="!editing || selectedUser !== user" />
                                        {{ role.name }}
                                    </label>
                                    <button class="btn btn-primary" v-if="user ===
                                        selectedUser && editing" @click="updateUser">Save</button>

                                    <button v-else class="btn btn-primary float-right"
                                        @click="toggleEditing(user)">Edit</button>
                                </td>


                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            // roles: [
            //     { name: 'Admin', role_id: 1 },
            //     { name: 'Support', role_id: 2 },
            //     { name: 'Student', role_id: 3 },
            // ],

            user_list: [],
            roles: [
                {
                    "description": null,
                    "name": "Admin",
                    "role_id": 1
                },
                {
                    "description": null,
                    "name": "Student",
                    "role_id": 3
                },
                {
                    "description": null,
                    "name": "Support",
                    "role_id": 2
                }
            ],
            userRole: {},
            editing: false,
            selectedUser: null,
            user_object: {
                username: '',
                role: []
            }


        }
    },
    methods: {

        toggleEditing(user) {
            if (this.selectedUser === user) {

                this.editing = !this.editing;
            } else {
                this.selectedUser = user;
                this.editing = true;
            }
        },
        updateUser() {
            console.log('update user')
            // console.log(JSON.stringify(this.selectedUser))
            this.user_object.username = this.selectedUser.username
            this.user_object.role = this.selectedUser.roles.map(role => role.name);
            console.log(JSON.stringify(this.user_object))


        }
    },
    created() {
        console.log('gettng users')
        const options = {
            method: 'GET',
            headers: {
                Authorization: localStorage.getItem("access_key")

            }
        };

        fetch('http://127.0.0.1:5000/api/user/all', options)
            .then(response => response.json())
            .then(response => this.user_list = response)
            .catch(err => console.error(err));
    },

}
</script>

<style>
.role-label {
    display: inline-block;
    margin-right: 10px;
}

.btn {
    width: 70px;
    /* adjust the width as needed */
}
</style>