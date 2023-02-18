<template>
    <b-container fluid>
        <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

        <b-tabs card class="h-100 d-flex flex-column flex-grow-1">
                <b-tab class="flex-grow-1" data-cy="course-search-tab">
                <template v-slot:title>
                    <div class="text-center" data-cy="course-search-tab-header">
                    GPA For Semester
                    </div>
                </template>
                <b-card-text class="w-100 d-flex flex-grow-1 flex-column">

                    <div class="calculator-box">
                        <h1>GPA CALCULATOR</h1>
                        <div id="course-wrapper">
                        <form class="key-0">
                        <p> <label id="course-row" for="courses">Courses:</label>
                        <label id="credit-row" for="credit-units">Credit Units:</label>
                        <label id="grade-row" for="grade">Grades: </label></p>
                        <input
                            type="text"
                            placeholder="Course Code"
                            class="courses key-0"
                            required/>
                            <!-- <label for="credit-units">Credit Units:</label> -->
                        <input
                            type="number"
                            class="credit-units key-0"
                            placeholder="Credit Units"
                            value=""
                            required
                        />
                            <!--<label for="grade">Grade: </label> -->
                        <select class="grade1 key-0" required>
                            <option class="grade" value="select">Select</option>
                            <option class="grade" value="4.00">A</option>
                            <option class="grade" value="3.67">A-</option>
                            <option class="grade" value="3.33">B+</option>
                            <option class="grade" value="3.00">B</option>
                            <option class="grade" value="2.67">B-</option>
                            <option class="grade" value="2.33">C+</option>
                            <option class="grade" value="2.00">C</option>
                            <option class="grade" value="1.67">C-</option>
                            <option class="grade" value="1.33">D+</option>
                            <option class="grade" value="1.00">D</option>
                            <option class="grade" value="0.67">D-</option>
                            <option class="grade" value="0.00">F</option>
                            <option class="grade" value="">P</option>
                        </select>
                    </form>
                    </div>
                    <!-- <section class"btn">+ Add Course</section> -->
                    <div class="btn">
                    <button @click="addCourse();">+ Add</button>
                    <button @click="removeCourse();">- Remove</button>
                    <button @click="calcCgpa();">Calculate GPA</button>
                    </div>
                    <div class="lastp">
                    <p id="cgpa-calc">Your GPA is:</p>
                    </div>
                    </div>
                </b-card-text>
                </b-tab>

                <b-tab class="flex-grow-1" data-cy="selected-courses-tab">
                <template v-slot:title>
                    <div class="text-center" data-cy="selected-courses-tab-header">
                    Total GPA After Semester
                    </div>
                </template>
                <b-card-text class="w-100 d-flex flex-grow-1 flex-column">

                    <div class="calculator-box">
                        <h1>TOTAL GPA CALCULATOR</h1>
                        <div id="semester-wrapper">

                        <input v-model="totCred" class= "credit_units0 key-0" placeholder="Total Credits" />
                        <input v-model="oldGPA" class = "oldGPA key-0" placeholder="GPA" />


                        </div>

                    <div class="btn">
                    <button @click="addClass();">+ Add Class</button>
                    <button @click="addGPA();">+ Add GPA</button>
                    <button @click="removeSemester();">- Remove</button>
                    <button @click="finClac(oldGPA,totCred,newGPA,curCred);">Calculate GPA</button>
                    </div>
                    <div class="lastp">
                    <p id="fin-calc">Your GPA is:</p>
                    </div>
                    </div>

                </b-card-text>
                </b-tab>


                <b-tab class="flex-grow-1" data-cy="selected-courses-tab">
                <template v-slot:title>
                    <div class="text-center" data-cy="elected-courses-tab-header">
                        Weight Calculator

                    </div>
                </template>
                <b-card-text class="w-100 d-flex flex-grow-1 flex-column">




                    <div class="calculator-box">
                        <h1>Weight Calculator</h1>
                        <div id="weight-wrapper">

                        <input v-model="totCred" class= "credit_units0 key-0" placeholder="Total Credits" />
                        <input v-model="oldGPA" class = "oldGPA key-0" placeholder="GPA" />

                        </div>

                    <div class="btn">
                    <button @click="addWeight();">+ Add Class</button>
                    <button @click="removeSemester();">- Remove</button>
                    <button @click="finClac(oldGPA,totCred,newGPA,curCred);">Calculate GPA</button>
                    </div>
                    <div class="lastp">
                    <p id="fin-calc">Your GPA is:</p>
                    </div>
                    </div>





                </b-card-text>
                </b-tab>





        </b-tabs>
    </b-container>
</template>

<script>
export default {
    name: "GPACalculator",
    data() {
    return {
        breadcrumbNav: [
        {
            text: "YACS",
            to: "/",
        },
        {
            text: "GPACalculator",
        },
        ],
        counter: 0,
        reports: [],
        forms: [],
    };
    },
    methods: {
        AddForm() {
            const newForm = {
            id: Date.now(),
            name:``,

            }
            this.forms.push(newForm);
        },
        removeForm(id) {
            this.forms = this.forms.filter(form => form.id !== id);
        },
        finClac(oldGPA,totCred,newGPA,curCred){
            let resultGPA = 0;
            let gpaDif= Math.abs(oldGPA-newGPA);
            let per=curCred/totCred;
            let difference=per*gpaDif;
            if(oldGPA>newGPA){
                resultGPA=oldGPA-difference;
            }
            else if(oldGPA<newGPA){
                resultGPA=oldGPA+difference;
            }
            else{
                resultGPA=oldGPA
            }
            return resultGPA;
        },
        gradeCalc(grade, unit) {
            if (grade === "A") {
                return 4 * unit;
            } else if (grade === "A-") {
                return 3.67 * unit;
            } else if (grade === "B+") {
                return 3.33 * unit;
            } else if (grade === "B") {
                return 3 * unit;
            } else if (grade === "B-") {
                return 2.67 * unit;
            } else if (grade === "C+") {
                return 2.33 * unit;
            } else if (grade === "C") {
                return 2 * unit;
            } else if (grade === "C-") {
                return 1.67 * unit;
            } else if (grade === "D+") {
                return 1.33 * unit;
            } else if (grade === "D") {
                return 1 * unit;
            } else if (grade === "D-") {
                return .67 * unit;
            } else if (grade === "F") {
                return 0 * unit;
            }

        },
        addCourse() {
            let addNew = document.createElement("form");
            addNew.classList.add("add_new", `key-${this.counter}`);
            const course_name = `
            <form class="add_new key-${this.counter}">
                <input type="text" placeholder="Course Code" class="courses key-${this.counter}" required>
                    <input type="number" placeholder="Credit Units" class="credit-units key-${this.counter}" required>
                    <select class="grade1 key-${this.counter}" required>
                <option value="select">Select</option>
                <option value="4.00">A</option>
                <option value="3.67">A-</option>
                <option value="3.33">B+</option>
                <option value="3.00">B</option>
                <option value="2.67">B-</option>
                <option value="2.33">C+</option>
                <option value="2.00">C</option>
                <option value="2.33">C-</option>
                <option value="1.33">D+</option>
                <option value="1.00">D</option>
                <option value="0.67">D-</option>
                <option value="0.00">F</option>
                <option value="">P</option>
                </select>
            </form>
            `;
            addNew.innerHTML = course_name;
            document.getElementById("course-wrapper").appendChild(addNew);
            this.counter++;
        },
        removeCourse() {
            let mainForm = document.querySelector("form.add_new");
            mainForm.remove();
        },
        addGPA() {
            let addNew = document.createElement("form");
            addNew.classList.add("add_new", `key-${this.counter}`);
            const semester_name = `
            <form class="add_new key-${this.counter}">
                <input type="text" placeholder="Current GPA" class="curr_gpa key-${this.counter}" required>
                <input type="number" placeholder="Current Credits" class="credit_units1 key-${this.counter}" required>
                <button @click = "selfRemove()">-</button>

            </form>
            `;
            addNew.innerHTML = semester_name;
            document.getElementById("semester-wrapper").appendChild(addNew);
            this.counter++;
        },
        addClass() {
            let addNew = document.createElement("form");
            addNew.classList.add("add_new", `key-${this.counter}`);
            const semester_name = `
            <form class="add_new key-${this.counter}">
                <input type="number" placeholder="Credit Units" class="credit_units2 key-${this.counter}" required>
                <select class="grade2 key-${this.counter}" required>
                <option value="select">Select</option>
                <option value="4.00">A</option>
                <option value="3.67">A-</option>
                <option value="3.33">B+</option>
                <option value="3.00">B</option>
                <option value="2.67">B-</option>
                <option value="2.33">C+</option>
                <option value="2.00">C</option>
                <option value="2.33">C-</option>
                <option value="1.33">D+</option>
                <option value="1.00">D</option>
                <option value="0.67">D-</option>
                <option value="0.00">F</option>
                <option value="">P</option>
                </select>
                <button @click = "selfRemove()">-</button>
            </form>
            `;
            addNew.innerHTML = semester_name;
            document.getElementById("semester-wrapper").appendChild(addNew);
            this.counter++;
        },
        addWeight() {
            let addNew = document.createElement("form");
            addNew.classList.add("add_new", `key-${this.counter}`);
            const semester_name = `
            <form class="add_new key-${this.counter}">

                <input type="text" placeholder="Course Name" class="courses key-${this.counter}">

                <select class="level key-${this.counter}" required>
                <option value="select">Level</option>
                <option value="1">1000</option>
                <option value="2">2000</option>
                <option value="4">4000</option>
                </select>

                <select class="level key-${this.counter}" required>
                <option value="select">Type</option>
                <option value="0">Major</option>
                <option value="1">Hass</option>
                <option value="2">Others</option>

                </select>

            </form>
            `;
            addNew.innerHTML = semester_name;
            document.getElementById("weight-wrapper").appendChild(addNew);
            this.counter++;
        },
        removeSemester() {
            let mainForm = document.querySelector("form.add_new");
            mainForm.remove();
        },
        calcFgpa() {
            const CGPAPARAGRAPH = document.getElementById("fin-calc");
            const GRADESSELECT = document.querySelectorAll("select.grade2");
            const GPAINP = document.querySelectorAll("input.curr_gpa");
            const UNITGPA = document.querySelectorAll("input.credit_units1");
            const UNITCLASS = document.querySelectorAll("input.credit_units2");
            const OGCREDITS = document.querySelector("input.credit_units0");
            const OGGPA = document.querySelector("input.oldGPA");

            //const courseReport = {};

            const listOfGrades = [];
            const listOfUnits = [];
            let totalUnits = 0;

            const listOfGPA = [];
            const listOfCredits = [];
            let totalCredits = 0;

            let originalCredit = parseInt(OGCREDITS.value);
            let originalGPA = parseInt(OGGPA.value);

            GRADESSELECT.forEach((e) => {
                let GRADES = e.options;
                const selectedIndex = e.selectedIndex;
                const selectedGrade = GRADES[selectedIndex];
                const gradeValue = selectedGrade.text.toUpperCase();
                listOfGrades.push(gradeValue);
            });
            console.log(listOfGrades);

            UNITGPA.forEach((e) => {
                const unitValue = parseInt(e.value);
                totalUnits += unitValue;
                listOfUnits.push(unitValue);
            });
            console.log(listOfUnits);

            GPAINP.forEach((e) => {
                let GPA = e.options;
                const selectedIndex = e.selectedIndex;
                const selectedGPA = GPA[selectedIndex];
                const GPAValue = selectedGPA.text.toUpperCase();
                listOfGPA.push(GPAValue);
            });
            console.log(listOfGPA);

            UNITCLASS.forEach((e) => {
                const creditValue = parseInt(e.value);
                totalCredits += creditValue;
                listOfCredits.push(creditValue);
            });
            console.log(listOfCredits);



            let totalEarnedUnits = 0;


            for (let i = 0; i < listOfUnits.length; i++) {
                if(listOfGrades[i] != "P"){
                    totalEarnedUnits += this.gradeCalc(listOfGrades[i], listOfUnits[i]);
                }
                else{
                    totalUnits -= listOfUnits[i];
                }

            }

            const gpaGrades = totalEarnedUnits / totalUnits;

            let gpaUpdated = 0;

            totalCredits = originalCredit;


            for (let i = 0; i < listOfCredits.length; i++) {
                if(i==0){
                    gpaUpdated = this.finClac(originalGPA, originalCredit, listOfGPA[i], listOfCredits[i]);
                }
                else{
                   gpaUpdated = this.finClac(gpaUpdated, totalCredits, listOfGPA[i], listOfCredits[i]);
                }

                totalCredits += listOfCredits[i];


            }

            let finalGPA = 0;

            if(listOfUnits.length > 0 && listOfCredits.length > 0){
                finalGPA = this.finClac(gpaUpdated, originalCredit, gpaGrades, totalUnits);
            }
            else if(listOfCredits.length > 0){
                finalGPA = gpaUpdated;
            }
            else if(listOfUnits.length > 0){
                finalGPA = this.finClac(originalGPA, originalCredit, gpaGrades, totalUnits);
            }



            if (finalGPA >= 0){
                CGPAPARAGRAPH.textContent = "Your GPA is " + finalGPA.toFixed(2);
            } else {
                CGPAPARAGRAPH.textContent = "Please enter your correct grade and credit units";
            }
        },
        calcCgpa() {
            const CGPAPARAGRAPH = document.getElementById("cgpa-calc");
            const GRADESSELECT = document.querySelectorAll("select.grade1");
            const UNIT = document.querySelectorAll("input.credit-units");

            //const courseReport = {};

            const listOfGrades = [];
            const listOfUnits = [];
            let totalUnits = 0;

            GRADESSELECT.forEach((e) => {
                let GRADES = e.options;
                const selectedIndex = e.selectedIndex;
                const selectedGrade = GRADES[selectedIndex];
                const gradeValue = selectedGrade.text.toUpperCase();
                listOfGrades.push(gradeValue);
            });
            console.log(listOfGrades);

            UNIT.forEach((e) => {
                const unitValue = parseInt(e.value);
                totalUnits += unitValue;
                listOfUnits.push(unitValue);
            });
            console.log(listOfUnits);

            let totalEarnedUnits = 0;

            for (let i = 0; i < listOfUnits.length; i++) {
                if(listOfGrades[i] != "P"){
                    totalEarnedUnits += this.gradeCalc(listOfGrades[i], listOfUnits[i]);
                }
                else{
                    totalUnits -= listOfUnits[i];
                }

            }
            const gpa = totalEarnedUnits / totalUnits;

            if (gpa >= 0){
                CGPAPARAGRAPH.textContent = "Your GPA is " + gpa.toFixed(2);
            } else {
                CGPAPARAGRAPH.textContent = "Please enter your correct grade and credit units";
            }
        },

        selfRemove(){
            this.formData = null;
        },


        CourseWeight(level, isMajor, isHass){
            let TypeWeight = 0.7;
            let LevelWeight = 0.3;
            let type = 0;
            if(isMajor){
                type = 2;
            }else if(isHass){
                type = 0.7;
            }else{
                type = 1;
            }
            let score = TypeWeight * type + LevelWeight * level;
            return score;
        }


    }
};
//during the end of this semester one feature that I worked on was YACS gpa calculator
//this claculator has 2 features- 1 where you simply calculate your gpa from the given smemster
//                              - 1 see what your new gpa from your past gpa based on your credit hours
//this was a great project that helpred me get more familiar with vue
//Some features that were interesting was the buttons on my gpa calculator add remove and calculate
//add: adds to the list of classes taken and will show a new row in this calculaore
//remove: opposite of add and deletes the last row
//calculate: a calculate function that takes the credits and grades of each course and loops through with an algorithm to calculate your final gpa
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
    font-weight: bolder;
    margin-left: -2%;
    }

    #credit-row {
    font-size: 20px;
    font-weight: bolder;
    margin-left: 13%;
    }

    #grade-row {
    font-size: 20px;
    font-weight: bolder;
    margin-left: 8%;
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
    text-align: center;
    border: white;
    background-color: rgba(108, 90, 90, 0.15);
    }

    p{
    padding: 20px;
    font-size: 1rem;
    color: white;
    text-align: center;
    }

    #course-wrapper, form {
    color: white;
    padding-left: 10px;
    margin: 0 auto;
    text-align: center;
    }

    input{
    border: none;
    padding: 15px;
    margin: 10px;
    border-radius: 5px;
    width: 25%;
    text-align: center;
    }
    select{
    padding: 15px;
    border: none;
    border-radius: 7.5px;
    width: 20%;
    /*   height: 30px; */
    }
    button {
    width: 20%;
    height: 40px;
    padding: 1px;
    margin: 5px auto;
    margin-left: 10px;
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
    background-color: rgba(108, 90, 90, 0.15);
    }
    .lastp p {
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 30px;
    font-weight: bolder;
    }

</style>
