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
            <div class="col" style="min-width: 50%; max-width: 51%; max-height:50%;">
                <div class="d-flex flex-column justify-content-left align-items-left">
                    <!-- First flexbox content goes here -->
                    <h1>{{ ticket.title }}
                    </h1>
                    <div class="d-flex">
                        <span v-for="tag in ticket.tags" class="badge bg-success rounded-pill me-1">{{ tag.name }}</span>
                        <!-- <span class="badge bg-info rounded-pill me-2">Badge 1</span> -->
                    </div>

                    <button @click="upvote" type="button" class="btn btn-primary mt-3" style="width: 20%;">
                        Votes <span class="badge text-bg-secondary">{{ ticket.votes_count }}</span>
                    </button>

                    <button class="btn btn-danger mt-2" @click="deleteticket" style="width: 20%;">Delete Ticket</button>
                    <p class="mt-4  fs-5 fw-normal text-body">{{ ticket.body }}</p>
                </div>
            </div>

            <div class="col">
                <div class="d-flex flex-column justify-content-center align-items-center">
                    <!-- Second flexbox content goes here -->
                    <h1>Comments</h1>
                    <div class="container">
                        <div class="d-flex flex-column">
                            <div class="card mb-3">
                                <div class="card-body">
                                    <h5 class="card-title">Comments</h5>

                                    <div class="media justify-content-end" v-for="(comment, index) in comments"
                                        :key="index">
                                        <hr>
                                        <div class="media-body text-right" :class="{ 'bg-success': comment.solution }">

                                            <h5 class="mt-0">{{ comment.commentor.first_name }} {{
                                                comment.commentor.last_name }}
                                            </h5>

                                            <p>{{ comment.body }}<span v-if="comment.solution"
                                                    class="badge rounded-pill text-bg-success m-1 ">Solution</span>
                                            </p>

                                            <button class="btn btn-success m-1"
                                                v-if="ticket.student.user_id === currentUser_id && !comment.solution"
                                                @click="mark_solution(comment.comment_id)">
                                                Mark as solution
                                            </button>

                                            <button class="btn btn-danger"
                                                v-if="comment.commentor.user_id === currentUser_id"
                                                @click="deleteComment(comment.comment_id)">
                                                Delete
                                            </button>
                                        </div>

                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <div class="d-flex flex-column justify-content-left align-items-left">
                    <!-- Third flexbox content goes here -->
                    <h1>Post comments</h1>
                    <form>
                        <div class="form-group form-floating " style="width: 50%;">
                            <textarea v-model="new_comment" class="form-control" placeholder=""
                                id="floatingTextarea"></textarea>
                            <label for="floatingTextarea">Leave a comment here</label>

                        </div>
                        <button @click.prevent="post_comment" type="submit" class="btn btn-primary">Post comment</button>
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
            ticket: {},
            comments: [],
            new_comment: '',
            currentUser_id: JSON.parse(localStorage.getItem("user_details")).user_id

        }
    },
    methods: {

        mark_solution(comment_id) {
            console.log("marked sol")
            const options = {
                method: 'PUT',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch(`http://127.0.0.1:5000/api/comments/${comment_id}/solution`, options)
                .then(response => response.json())
                .then(response => console.log(response))
                .catch(err => console.error(err));
        },
        deleteComment(comment_id) {
            console.log(comment_id)
            const options = {
                method: 'DELETE',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch(`http://127.0.0.1:5000/api/comments/${comment_id}`, options)
                .then(response => response.json())
                .then(response => { this.get_comments() })
                .catch(err => console.error(err));
        },

        upvote() {
            console.log('clicked on upvote')
            const options = {
                method: 'POST',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}/upvote`, options)
                .then(response => {
                    if (response.status === 200) {
                        this.ticket.votes_count++;
                    }
                    return response.json();
                })
                .then(response => console.log(response))
                .catch(err => console.error(err));
        },


        deleteticket() {
            const options = {
                method: 'DELETE',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}`, options)
                .then(response => {
                    response.json();
                })
                .then(response => {
                    this.$router.push('/home')
                })
                .catch(err => console.error(err));
        },


        get_comments() {
            console.log("getting comments")
            const options = {
                method: 'GET',
                headers: {
                    Authorization: localStorage.getItem("access_key")
                }
            };

            fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}/comments`, options)
                .then(response => response.json())
                .then(response => { this.comments = response; })
                .catch(err => console.error(err));
        },

        post_comment() {
            console.log("clicked post comment")
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: localStorage.getItem("access_key")

                },
                body: `{"body":"${this.new_comment}"}`
            };

            fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}/comments`, options)
                .then(response => response.json())
                .then(response => {
                    this.get_comments();
                    this.new_comment = ''

                })
                .catch(err => console.error(err));
        }

    },
    created() {
        this.ticket_id = this.$route.params.tid;

        //Get comments
        this.get_comments();

        // Get ticket details
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
    },



};

</script>


<style>
.bg-success {
    --bs-bg-opacity: .6;
    background-color: rgba(var(--bs-success-rgb), var(--bs-bg-opacity)) !important;
}
</style>