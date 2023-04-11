<template>
    <b-container fluid>
        <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

       
            <b-card-text class="w-100 d-flex flex-grow-1 flex-column">

                <div class="calculator-box">
                    <h1>FINAL SCHEDULE GENERATOR</h1>
                    <div id="course-wrapper">
                    <form class="key-0">
                    <p> <label id="dept-row" for="courses">Dept:</label>
                        <label id="course-row" for="courses">Course#:</label>
                        <label id="section-row" for="courses">Section:</label>
                    </p>
                </form>
                </div>
                <!-- <section class"btn">+ Add Course</section> -->
                <div class="btn">
                <button @click="addClass();">+ Add</button>
                <button @click="removeClass();">- Remove</button>
                <button @click="generateSchedule();">Generate Schedule</button>
            
                
                </div>
                </div>
            </b-card-text>


    </b-container>
</template>

<script>
export default {
    name: "FinalSchedule",
    data() {
    return {
        breadcrumbNav: [
        {
            text: "YACS",
            to: "/",
        },
        {
            text: "FinalSchedule",
        },
        ],
        counter: 0,
        reports: [],
        forms: [],
        index: 0,
    };
    },
    methods: {
        

        addClass(){

        },
        removeClass(){

        },
        generateSchedule(){

        },
     


    }
};

</script>

<style>
    * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: sans-serif;
    }

    #course-row {
    font-size: 20px;
    color: #aeb2b8;
    font-weight: bolder;
    margin-left: 6%;
    }


    .calculator-box {
    width: 50%;
    height: auto;
    border:  rgba(108, 90, 90, 0.15);
    margin: 100px auto;
    /*  text-align: center; */
    }


    /* On screens that are 1200px or less, set the width to 75% */
    @media screen and (max-width: 1200px) {
    .calculator-box {
        width: 70%;
    }
    }

    /* On screens that are 950px or less, set the width to 75% */
    @media screen and (max-width: 950px) {
    .calculator-box {
        width: 75%;
    }
    }

    /* On screens that are 600px or less, set the width to 90% */
    @media screen and (max-width: 600px) {
    .calculator-box {
        width: 90%;
    }
    }

    h1 {
    padding: 15px;
    font-size: 40px;
    font-weight: bolder;
    text-align: center;
    border: white;
    background-color: #AFC9C6;
    }

    p{
    padding: 10px;
    font-size: 1rem;
    color: black;
    text-align: center;
    }

    #course-wrapper, form {
    color: white;
    margin: 0 auto;
    text-align: center;
    width: 100%;
    }

    input{
    padding: 10px;
    margin: 10px;
    border-radius: 5px;
    width: 25%;
    text-align: center;
    }
    select{
    padding: 10px;
    margin: 9px;
    border-radius: 7.5px;
    /*   height: 30px; */
    }
    button {
    width: 20%;
    height: 40px;
    padding: 1px;
    margin: 5px auto;
    margin-left: 20px;
    border-width: 1px;
    border-radius: 10%;
    border-style: solid;
    }

    .btn {
    width: 100%;
    padding: 10px;
    display: inline-block;
    margin: 1px auto;
    text-align: center;
    }

    .lastp {
    border:  rgba(108, 90, 90, 0.15);
    background-color: #AFC9C6;
    }
    .lastp p {
    color: black;
    text-align: center;
    padding: 10px;
    font-size: 30px;
    font-weight: bolder;
    }

</style>
