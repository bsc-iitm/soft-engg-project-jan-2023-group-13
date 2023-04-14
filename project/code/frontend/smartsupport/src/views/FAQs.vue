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
    </div>
</template>

<script>

export default {
    name: "FAQs",
    data(){
        return {
            faq_list: [],
        }
    }
};

</script>


<style></style>