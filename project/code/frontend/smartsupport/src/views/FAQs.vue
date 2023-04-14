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
                    <router-link class="nav-link " aria-current="page" to="/home">Home</router-link>
                    <router-link class="nav-link" to="/profile">Profile</router-link>

                    <router-link class="nav-link" to="/mytickets">My Tickets</router-link>
                    <router-link class="nav-link active" to="/faqs">FAQs</router-link>

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
        <h1>Frequently Asked Questions</h1>
        <div class="media justify-content-end" v-for="(faq, index) in faq_list"
                :key="index">
            <!-- <div class="media-body text-right">
                <h5 class="mt-0">{{ faq.query }}
                </h5>
                <p>
                    {{ faq.answer }}
                </p>
            </div>
            <hr> -->

            <div class="accordion accordion-flush" id="accordionFlushExample">
                <div class="accordion-item">
                    <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                        :data-bs-target="'#collapseOne'+index" aria-expanded="false" aria-controls="">
                        {{ faq.query }}
                    </button>
                    </h2>
                    <div :id="'collapseOne'+index" class="accordion-collapse collapse"
                        data-bs-parent="#accordionFlushExample">
                    <div class="accordion-body">{{ faq.answer }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import config from "@/config.js";

export default {
    name: "FAQs",
    data(){
        return {
            faq_list: [],
        }
    },
    methods: {
        Get_FAQ_list() {
            // Get list of FAQs
            fetch(`${config.BASE_API_URL}/faqs`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.faq_list = res
                    console.log("got faq list")
                    console.log(this.faq_list)

                });
        },
    },
    created(){
        this.Get_FAQ_list()
    }
};

</script>


<style></style>