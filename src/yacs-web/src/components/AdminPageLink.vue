<template>
    <b-card no-body
        class="bg-primary text-white text-center justify-content-center d-flex"
        style="height:200px; width:200px;"
        @click="$emit('click', type)"
    >
        <span v-if="type === 'csv'">CSV</span>
        <span v-if="type === 'date'">Date</span>
    </b-card>
</template>

<script>
export default {
    name: "AdminPageLink",
    props: {
        type: String
    },
    components: {},
    data () {
        return {

        }
    },
    methods: {}
}
</script>