//test.html line 7 gives us access to a Vue object
const app = Vue.createApp({
    //data, functions to react to user
    data() {        //Create a function
        return {    //Return a data object in the function
            title: 'YACS',
            author: 'William Lin',
            age: 19,
            mood: 5
        }
    }, 
    // methods: {
    //     changeTitle() {
    //         console.log('clicked')
    //     }
    // }
    // methods: {
    //     toggleShowBooks() {
    //         this.toggleShowBooks = !this.showBooks;
    //     }
    // }
                //The comp a root component
})
//the {} inside the () allows us to create functions to handle a click



//Tells the app to mount on the element in line 11 on test.html
//The Vue app now controls anything inside the <div id = "app"> here <div>
app.mount('#app')   