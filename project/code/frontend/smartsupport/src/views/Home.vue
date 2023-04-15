<template>
    <NavBar></NavBar>
    <div class="offcanvas">
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
                    <router-link :to="'/ticket/' + s_ticket.ticket_id"  class="text-decoration-none text-dark">
                        <div class="media-body text-right">
                            <h5 class="mt-0 text-dark">{{ s_ticket.title }}
                            </h5>
                            <p>
                                {{ s_ticket.body.substring(0, 100) + "..." }}
                            </p>
                            <div class="col align-self-end text-end">
                                <!-- <router-link :to="'/ticket/' + s_ticket.ticket_id">Read more... </router-link> -->
                            </div>
                        </div>
                    </router-link>
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

    </div>
</template>

<script>
import { ref, reactive, watch } from 'vue';
import * as search from '../utilities/search.js';
import config from "@/config.js";
import NavBar from '@/components/NavBar.vue';




export default {
    name: "Home",
    components: {
        NavBar,
    },
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
            user_details: {},
            ticket_list: [],
            ticket_data: {
                title: "",
                tags: [],
                body: ""
            },
            tag_list: [],
            searched_ticket_list: [],
            show_search_spinner: true,
            is_admin: false,
            is_support: false,
            is_student: false,
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
            search.search_tickets(this.ticket_data.title, this)
        },
        user_roles(){
            this.user_details.roles.forEach((item) => {
                console.log(item.name);
                if (item.name === "Student") {this.is_student = true;}
                if (item.name === "Admin") {this.is_admin = true;}
                if (item.name === "Support") {this.is_support = true;}
            })
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

        fetch(`${config.BASE_API_URL}/user`, options)
            .then(response => response.json())
            .then(response => { localStorage.setItem("user_details", JSON.stringify(response)) })
            .then(this.user_details = JSON.parse(localStorage.getItem("user_details")))
            .catch(err => console.error(err));


    },
    mounted(){
        this.user_roles()
    }
};
</script>

<style>
h3 {
    float: right;
}
</style>


<style></style>