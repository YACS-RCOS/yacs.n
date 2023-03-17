import Vue from "vue";

// save our state (isPanel open or not) 
export const store = Vue.observable({
    isNavOpen: false,
    main: "col-md-12"
});

// We call toggleNav anywhere we need it in our app
export const mutations = {
    toggleNav() {
        store.isNavOpen = !store.isNavOpen;
        if (store.isNavOpen){
            store.main = "col-md-9";
        }else{
            store.main = "col-md-12";
        }
    }
};