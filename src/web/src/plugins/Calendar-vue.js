import DaySpanVuetify from "dayspan-vuetify";
import "dayspan-vuetify/dist/lib/dayspan-vuetify.min.css";

Vue.use(DaySpanVuetify, {
  methods: {
    getDefaultEventColor: () => "success",
  },
});
