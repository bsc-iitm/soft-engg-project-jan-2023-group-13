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
                    <router-link :class="{ 'nav-link': true, active: $route.path === '/home' }" to="/home">
                        Home
                    </router-link>
                    <router-link :class="{ 'nav-link': true, active: $route.path === '/profile' }" to="/profile">
                        Profile
                    </router-link>
                    <router-link :class="{ 'nav-link': true, active: $route.path === '/mytickets' }" to="/mytickets">
                        My Tickets
                    </router-link>
                    <router-link :class="{ 'nav-link': true, active: $route.path === '/faqs' }" to="/faqs">
                        FAQs
                    </router-link>

                    <form class="d-flex" role="search">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
                            v-model="ticket_data.title" @keyup="search_tickets" />
                        <button class="btn btn-outline-success" type="submit">
                            Search
                        </button>
                    </form>
                    <router-link :class="{ 'nav-link': true }" to="/">
                        Logout
                    </router-link>
                </div>
            </div>
        </div>
    </nav>
</template>
  

  

<script>
export default {
    name: "Navbar",
    data() {
        return {
            ticket_data: {
                title: "",
            },
        };
    },
    methods: {
        search_tickets() {
            // add your search_tickets function here
        },
    },
};
</script>