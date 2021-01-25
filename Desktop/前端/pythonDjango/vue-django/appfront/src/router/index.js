import Vue from 'vue'
import Router from 'vue-router'
// import Home from '@/components/Home'
// import HelloWorld from '@/components/HelloWorld'

import home from "./home.js"//导入路由文件
import helloword from "./helloword.js"//导入路由文件

Vue.use(Router)

let routes = new Set([...home, ...helloword]);
 
export default new Router({
  // mode:'history',
  routes: routes
})

/*
export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
*/
