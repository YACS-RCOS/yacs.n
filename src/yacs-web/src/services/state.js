var MyPlugin = {}

MyPlugin.install = function (Vue, options) {
    console.log(options);
    // 1. add global method or property
    Vue.prototype.nstate = {
        currentRequests: 0,
        currentResponses: 0,
        currentRequestsInFlight: 0,
        timeoutExpired: false
    }
    console.log(Vue);
}

export default MyPlugin;