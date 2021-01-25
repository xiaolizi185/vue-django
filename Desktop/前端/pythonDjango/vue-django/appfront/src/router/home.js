 
// import Home from '@/components/Home'
// import HelloWorld from '@/components/HelloWorld'
 
export default [
 
    {
        path: "/",
        name: 'Home',
        component: (resolve) => require(['../components/Home.vue'], resolve)//实现懒加载
    }
]
