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
                    <h1>{{ ticket.title }}
                    </h1>
                    <div class="d-flex">
                        <span v-for="tag in ticket.tags" class="badge bg-success rounded-pill me-1">{{ tag.name }}</span>
                        <!-- <span class="badge bg-info rounded-pill me-2">Badge 1</span> -->
                    </div>

                    <button type="button" class="btn btn-primary mt-3" style="width: 20%;">
                        Votes <span class="badge text-bg-secondary">{{ ticket.votes_count }}</span>
                    </button>
                    <p class="mt-4  fs-5 fw-normal text-body">{{ ticket.body }}</p>
                </div>
            </div>

            <div class="col">
                <div class="d-flex flex-column justify-content-center align-items-center">
                    <!-- Second flexbox content goes here -->
                    <h1>Comments</h1>

                </div>
            </div>
        </div>
        <br>
        <br>
        <br>
        <div class="row">
            <div class="col">
                <div class="d-flex flex-column justify-content-left align-items-left">
                    <!-- Third flexbox content goes here -->
                    <h1>Post comments</h1>
                    <form>
                        <div class="form-group form-floating " style="width: 50%;">
                            <textarea class="form-control" placeholder="" id="floatingTextarea"></textarea>
                            <label for="floatingTextarea">Leave a comment here</label>

                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    name: "Ticket",
    data() {
        return {
            ticket_id: '',
            ticket: {}
        }
    },
    created() {
        this.ticket_id = this.$route.params.tid;

        const options = {
            method: 'GET',
            headers: {
                Authorization: localStorage.getItem("access_key")
            }
        };

        fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}`, options)
            .then(response => response.json())
            .then(response => { this.ticket = response })
            .catch(err => console.error(err));
    }

};

</script>