<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <span class="navbar-brand">Smart Support</span>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <router-link class="nav-link active" aria-current="page" to="/home">Home</router-link>
                    <router-link class="nav-link" to="/profile">Profile</router-link>

                    <router-link class="nav-link" to="/mytickets">My Tickets</router-link>




                    <form class="d-flex" role="search">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                        <button class="btn btn-outline-success" type="submit">Search</button>
                    </form>


                    <router-link to="/" class="nav-link">Logout</router-link>

                </div>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col">
                <div class="d-flex flex-column justify-content-left align-items-left">
                    <!-- First flexbox content goes here -->
                    <h1>My Tickets</h1>

                    <!-- <li v-for="ticket in ticket_list">{{ ticket.title }}</li> -->
                    <table class="table table-borderless table-group-divider">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Votes</th>
                                <th>Created At</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="ticket in ticket_list" :key="ticket.ticket_id">
                                <td><router-link :to="'/ticket/' + ticket.ticket_id">{{ ticket.title }}</router-link></td>
                                <td>{{ ticket.votes_count }}</td>
                                <td>{{ ticket.created_at }}</td>
                                <td>{{ ticket.status }}</td>
                            </tr>
                        </tbody>
                    </table>



                </div>
            </div>
            <div class=" col">
                <div class="d-flex flex-column justify-content-center align-items-center">
                    <!-- Second flexbox content goes here -->
                    <h1>Raise a new Ticket</h1>

                    <form @submit.prevent="Createticket">
                        <div class="form-group">
                            <label for="title">Title</label>
                            <input type="text" class="form-control" id="title" v-model="ticket_data.title" required>
                        </div>

                        <div class="form-group">

                            <label for="tags">Select Tag</label>
                            <select class="form-control" id="tags" required v-model="ticket_data.tags" multiple>
                                <!-- <option value="Tags" disabled selected> </option> -->
                                <option v-for="tag in tag_list">{{ tag.name }}</option>
                                <!-- <option value="SoftEng">Software Engineering</option>
                                <option value="SoftTest">Software Testing</option>
                                <option value="DeepLearn">Deep Learning</option>
                                <option value="ArtInt">Artificial Intelligence</option>
                                <option value="FinFor">Financial Forecasting</option>
                                <option value="Ops">Operations Management</option>
                                <option value="Clarification">Clarification Request</option>
                                <option value="Assignment">Assignment Submission</option>
                                <option value="PSM">Project Scope Management</option> -->
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="body">Body</label>
                            <input type="text" class="form-control" id="body" v-model="ticket_data.body" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "Home",
    data() {
        return {
            ticket_list: [],
            ticket_data: {
                title: "",
                tags: "",
                body: ""
            },
            tag_list: []

        };
    },
    methods: {
        Createticket() {
            console.log("clicked on create ticket")
            console.log(JSON.stringify(this.ticket_data))


            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: localStorage.getItem("access_key"),
                },
                body: JSON.stringify(this.ticket_data)
            };

            fetch('http://127.0.0.1:5000/api/tickets', options)
                .then(response => response.json())
                .then(response => console.log(response))
                .catch(err => console.error(err));
        }
    },
    created() {
        // Get list of tickets
        fetch("http://127.0.0.1:5000/api/tickets/user", {
            headers: { Authorization: localStorage.getItem("access_key") },
        })
            .then((res) => res.json())
            .then((res) => {
                this.ticket_list = res

            });

        //Get list of tags

        fetch("http://127.0.0.1:5000/api/tags", {
            headers: { Authorization: localStorage.getItem("access_key") },
        })
            .then((res) => res.json())
            .then((res) => {
                this.tag_list = res

            });
    },
};
</script>

<style>
h3 {
    float: right;
}
</style>


<style></style>