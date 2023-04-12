import { createRouter, createWebHistory } from 'vue-router'

import SignIn from '../views/SignIn.vue'
import SignUp from '../views/SignUp.vue'
import Home from '../views/Home.vue'
import Profile from '../views/Profile.vue'
import MyTickets from '../views/MyTickets.vue'
import Ticket from '../views/Ticket.vue'




const routes = [
  {
    path: '/',
    component: SignIn
  },
  {
    path: "/signup",
    component: SignUp,
  },
  {
    path: "/home",
    component: Home,
  },
  {
    path: "/profile",
    component: Profile,
  },
  {
    path: "/mytickets",
    component: MyTickets,
  },
  {
    path: "/ticket/:tid",
    component: Ticket,
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
