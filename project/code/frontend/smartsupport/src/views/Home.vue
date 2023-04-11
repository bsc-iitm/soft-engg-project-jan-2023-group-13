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

    <!-- <div class="mt-4">
        <div>
            <h2 class="ms-5">My Tickets</h2>
        </div>
        <h3 class="text-right">Raise a New Ticket</h3>

    </div> -->
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
                                <td>{{ ticket.title }}</td>
                                <td>{{ ticket.votes_count }}</td>
                                <td>{{ ticket.created_at }}</td>
                                <td>{{ ticket.status }}</td>
                            </tr>
                        </tbody>
                    </table>



                </div>
            </div>
            <div class="col">
                <div class="d-flex flex-column justify-content-center align-items-center">
                    <!-- Second flexbox content goes here -->
                    <h1>Raise a new Ticket</h1>
                    <form>
                        <div class="form-group">
                            <label for="input1">Subject</label>
                            <input type="text" class="form-control" id="input1">
                        </div>
                        <div class="form-group">
                            <label for="input2">Tags</label>
                            <input type="text" class="form-control" id="input2">
                        </div>
                        <div class="form-group">
                            <label for="input3">body</label>
                            <input type="text" class="form-control" id="input3">
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

        };
    },

    created() {
        fetch("http://127.0.0.1:5000/api/tickets/user", {
            headers: { Authorization: localStorage.getItem("access_key") },
        })
            .then((res) => res.json())
            .then((res) => {
                this.ticket_list = res

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