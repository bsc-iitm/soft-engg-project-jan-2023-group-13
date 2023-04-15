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
                    <router-link class="nav-link" to="/faqs">FAQs</router-link>


                    <form class="d-flex" role="search">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
                            v-model="ticket_data.title" @keyup="search_tickets">
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
                                <th>Date</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="ticket in ticket_list" :key="ticket.ticket_id">
                                <td><router-link :to="'/ticket/' + ticket.ticket_id" class="">{{ ticket.title }}</router-link></td>
                                <td>{{ ticket.votes_count }}</td>
                                <td><small>{{ ticket.created_at.substring(0, 10) }}</small></td>
                                <td>{{ ticket.status }}</td>
                            </tr>
                        </tbody>
                    </table>



                </div>
            </div>
            <div class="col">
                <div class="d-flex flex-column justify-content-center ">
                    <!-- Second flexbox content goes here -->
                    <h1>Raise a new Ticket</h1>
                    <div class="card border-light">
                        <div class="card-body">
                            <form @submit.prevent="Createticket">
                                <div class="form-group mb-3">
                                    <label for="title" class="form-label">Title</label>
                                    <input type="text" class="form-control" id="title" v-model="ticket_data.title"
                                        @keyup="search_tickets" required>
                                </div>
                                <div class="form-group mb-3">

                                    <label for="tags">Select Tag(s)</label>
                                    <select class="form-control" id="tags" required v-model="ticket_data.tags" multiple>
                                        <!-- <option value="Tags" disabled selected> </option> -->
                                        <option v-for="tag in tag_list">{{ tag.name }}</option>

                                    </select>
                                </div>

                                <div class="form-group mb-3">
                                    <label for="body">Body</label>
                                    <textarea type="text" class="form-control" id="body" v-model="ticket_data.body"
                                        required></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary">Submit</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <!-- <button @click="openOffcanvas">Open Offcanvas</button> -->
            <div class="offcanvas offcanvas-start" tabindex="-1" ref="offcanvas" :class="{ show: offcanvasState.show }"
                @hidden.bs.offcanvas="offcanvasState.show = false">
                <div class="offcanvas-header">
                    <h3 class="offcanvas-title" id="offcanvasExampleLabel">Existing Tickets</h3>
                    <button @click="closeOffcanvas" type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas"
                        aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                    <!-- offcanvas content -->
                    <div class="media justify-content-end" v-for="(s_ticket, index) in searched_ticket_list" :key="index">
                        <div class="media-body text-right">
                            <h5 class="mt-0">{{ s_ticket.title }}
                            </h5>
                            <p>
                                {{ s_ticket.body.substring(0, 100) + "..." }}
                            </p>
                            <div class="col align-self-end text-end">
                                <router-link :to="'/ticket/' + s_ticket.ticket_id">Read more... </router-link>
                            </div>

                </div>
                <hr>
            </div>
            <div v-if="show_search_spinner" class="d-flex text-primary justify-content-center">
                <div class="spinner-border" role="status">
                    <span class="sr-only"></span>
                </div>
            </div>
        </div>
        </div>
    </div>
    </div>
</template>

<script>
import { ref, reactive, watch } from 'vue';
import config from "@/config.js";

export default {
    name: "Home",
    setup() {
        const offcanvasRef = ref(null);
        const offcanvasState = reactive({
            show: false
        });

        const openOffcanvas = () => {
            offcanvasState.show = true;
            document.body.classList.add('offcanvas-open');
        }

        const closeOffcanvas = () => {
            offcanvasState.show = false;
            document.body.classList.remove('offcanvas-open');
        }


        return {
            offcanvasRef,
            offcanvasState,
            openOffcanvas,
            closeOffcanvas,
        }
    },
    data() {
        return {
            ticket_list: [],
            ticket_data: {
                title: "",
                tags: [],
                body: ""
            },
            tag_list: [],
            searched_ticket_list: [],
            show_search_spinner: true,
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

            fetch(`${config.BASE_API_URL}/tickets`, options)
                .then(response => response.json())
                .then(response => this.Get_Ticket_list())
                .catch(err => console.error(err));


        },
        Get_Ticket_list() {
            // Get list of tickets
            fetch(`${config.BASE_API_URL}/tickets/user`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.ticket_list = res
                    console.log("got ticket list")


                });
        },
        search_tickets() {
            this.show_search_spinner = true
            if (this.ticket_data.title.length > 3) {
                this.openOffcanvas()
                fetch(`${config.BASE_API_URL}/tickets/search?q=${this.ticket_data.title}`, {
                    headers: { Authorization: localStorage.getItem("access_key") },
                })
                    .then((res) => res.json())
                    .then((res) => {
                        this.searched_ticket_list = res
                        console.log("got searched ticket list")
                        console.log(this.searched_ticket_list)
                        this.show_search_spinner = false
                    });
            }

        }
    },

    created() {
        this.Get_Ticket_list()
        //Get list of tags

        fetch(`${config.BASE_API_URL}/tags`, {
            headers: { Authorization: localStorage.getItem("access_key") },
        })
            .then((res) => res.json())
            .then((res) => {
                this.tag_list = res

            });


        //Store user details in localstorage
        const options = {
            method: 'GET',
            headers: {
                Authorization: localStorage.getItem("access_key")
            }
        };

        fetch('http://127.0.0.1:5000/api/user', options)
            .then(response => response.json())
            .then(response => { localStorage.setItem("user_details", JSON.stringify(response)) })
            .catch(err => console.error(err));
    },
};
</script>

<style>
h3 {
    float: right;
}
</style>


<style></style>