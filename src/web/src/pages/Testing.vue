<template>
    <b-container fluid>
        <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

        <div v-if="Object.keys(selectedCourses).length == 0" class="no-courses">
            Oops! It looks like you haven't selected anything!
            <br />
            To calculate your GPA, please add some courses to your schedule!
        </div>

        <div v-else>
            <b-row>
                <b-col
                    v-for="(courses, index) in courseObjects"
                    :key="`deptCol-${index}`"
                >
                    <b-row
                        v-for="course in courses"
                        :key="course.id"
                        class="selected"
                    >
                        <div>
                            <b data-cy="name">{{ course.name }}</b>
                            <br />
                            {{ course.title }}
                            <br />
                            {{ course.max_credits }}
                            
                            <b-form v-if="course.max_credits != 0" id="" class="add_new key-${this.counter}">                 
                                <b-form-group id="course.id-group" label="Grade:" label-for="course.id">
                                    <b-form-select
                                    id="course.id"
                                    :options="grades"
                                    required
                                    ></b-form-select>
                                </b-form-group>
                                
                            </b-form>
                        </div>
                    </b-row>
                </b-col>
                <b-col>
                    GPA
                </b-col>
            </b-row>
        </div>

    </b-container>
</template>

<script>
import { mapGetters, mapState } from "vuex";

import { SelectedCoursesCookie } from "../controllers/SelectedCoursesCookie";

import { userTypes } from "../store/modules/user";

import { COURSES } from "@/store";

import { getStudentCourses } from "@/services/YacsService";

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
                    text: "GPA Calculator",
                },
            ],
            grades: [{ text: 'Select', value: null }, 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'P'],
            selectedCourses: {},
            selectedScheduleSubsemester: null,
            loadedIndexCookie: 0,
        };
    },
    methods: {
        async loadStudentCourses() {
            this.selectedCourses = {};
            if (this.isLoggedIn) {
                var cids = await getStudentCourses();

                cids.forEach((cid) => {
                    if (cid.semester == this.selectedSemester) {
                        var c = this.courses.find(function (course) {
                            return (
                                course.name == cid.course_name &&
                                course.semester == cid.semester
                            );
                        });

                        if (cid.crn != "-1") {
                            var sect = c.sections.find(function (section) {
                                return section.crn == cid.crn;
                            });
                            sect.selected = true;
                        } else {
                            c.selected = true;
                            this.$set(this.selectedCourses, c.id, c);
                        }
                    }
                });
            } else {
                const selectedCoursesCookie = SelectedCoursesCookie.load(this.$cookies);
                try {
                    selectedCoursesCookie
                        .semester(this.selectedSemester)
                        .selectedCourses.forEach((selectedCourse) => {
                            const course = this.courses.find(
                                (course) => course.id === selectedCourse.id
                            );

                            this.$set(this.selectedCourses, course.id, course);
                            course.selected = true;
                        });
                } catch (err) {
                    selectedCoursesCookie.clear().save();
                }
            }
            
        },

        // AddForm() {
        //     const newForm = {
        //     id: Date.now(),
        //     name:``,

        //     }
        //     this.forms.push(newForm);
        // },

        // removeForm(id) {
        //     this.forms = this.forms.filter(form => form.id !== id);
        // },

        // finClac(oldGPA,totCred,newGPA,curCred){
        //     let resultGPA = 0;
        //     let gpaDif= Math.abs(oldGPA-newGPA);

        //     let per=curCred/totCred;
        //     let difference=per*gpaDif;
        //     if(oldGPA>newGPA){
        //         resultGPA=oldGPA-difference;
        //     }
        //     else if(oldGPA<newGPA){
        //         resultGPA=oldGPA+difference;
        //     }
        //     else{
        //         resultGPA=oldGPA
        //     }
        //     return resultGPA;
        // },

        // gradeCalc(grade, unit) {
        //     if (grade === "A") {
        //         return 4 * unit;
        //     } else if (grade === "A-") {
        //         return 3.67 * unit;
        //     } else if (grade === "B+") {
        //         return 3.33 * unit;
        //     } else if (grade === "B") {
        //         return 3 * unit;
        //     } else if (grade === "B-") {
        //         return 2.67 * unit;
        //     } else if (grade === "C+") {
        //         return 2.33 * unit;
        //     } else if (grade === "C") {
        //         return 2 * unit;
        //     } else if (grade === "C-") {
        //         return 1.67 * unit;
        //     } else if (grade === "D+") {
        //         return 1.33 * unit;
        //     } else if (grade === "D") {
        //         return 1 * unit;
        //     } else if (grade === "D-") {
        //         return .67 * unit;
        //     } else if (grade === "F") {
        //         return 0 * unit;
        //     }

        // },

        // addCourse() {
        //     let addNew = document.createElement("form");
        //     addNew.classList.add("add_new", `key-${this.counter}`);
        //     const course_name = `
        //     <form class="add_new key-${this.counter}">
        //         <input type="text" placeholder="Course Code" class="courses key-${this.counter}" required>
        //             <input type="number" placeholder="Credit Units" class="credit-units key-${this.counter}" required>
        //             <select class="grade1 key-${this.counter}" required>
        //         <option value="select">Select</option>
        //         <option value="4.00">A</option>
        //         <option value="3.67">A-</option>
        //         <option value="3.33">B+</option>
        //         <option value="3.00">B</option>
        //         <option value="2.67">B-</option>
        //         <option value="2.33">C+</option>
        //         <option value="2.00">C</option>
        //         <option value="2.33">C-</option>
        //         <option value="1.33">D+</option>
        //         <option value="1.00">D</option>
        //         <option value="0.67">D-</option>
        //         <option value="0.00">F</option>
        //         <option value="">P</option>
        //         </select>
        //     </form>
        //     `;
        //     addNew.innerHTML = course_name;
        //     document.getElementById("course-wrapper").appendChild(addNew);
        //     this.counter++;
        // },

        // // removeCourse() {
        // //     let mainForms = document.querySelectorAll("form.add_new");
        // //     mainForms[mainForms.length-1].remove();
        // // },

        // addGPA() {
        //     let addNew = document.createElement("form");
        //     addNew.classList.add("add_new1", `key-${this.counter}`);
        //     const semester_name = `
        //     <form class="add_new1 key-${this.counter}">
        //         <input type="text" placeholder="Current GPA" class="curr_gpa key-${this.counter}" required>
        //         <input type="number" placeholder="Current Credits" class="credit_units1 key-${this.counter}" required>

        //     </form>
        //     `;
        //     addNew.innerHTML = semester_name;
        //     document.getElementById("semester-wrapper").appendChild(addNew);
        //     this.counter++;
        // },

        // // addClass() {
        // //     let addNew = document.createElement("form");
        // //     addNew.classList.add("add_new1", `key-${this.counter}`);
        // //     addNew.classList.add("index", `key-${this.index}`);
        // //     const semester_name = `
        // //     <form class="add_new1 key-${this.counter} index-${this.index}">
        // //         <input type="number" placeholder="Credit Units" class="credit_units2 key-${this.counter}" required>
        // //         <select class="grade2 key-${this.counter}" required>
        // //         <option value="select">Select</option>
        // //         <option value="4.00">A</option>
        // //         <option value="3.67">A-</option>
        // //         <option value="3.33">B+</option>
        // //         <option value="3.00">B</option>
        // //         <option value="2.67">B-</option>
        // //         <option value="2.33">C+</option>
        // //         <option value="2.00">C</option>
        // //         <option value="2.33">C-</option>
        // //         <option value="1.33">D+</option>
        // //         <option value="1.00">D</option>
        // //         <option value="0.67">D-</option>
        // //         <option value="0.00">F</option>
        // //         <option value="">P</option>
        // //         </select>
        // //     </form>
        // //     `;
        // //     addNew.innerHTML = semester_name;
        // //     document.getElementById("semester-wrapper").appendChild(addNew);
        // //     this.counter++;

        // // },

        // removeSemester() {
        //     let mainForms = document.querySelectorAll("form.add_new1");
        //     mainForms[mainForms.length-1].remove();
        // },

        // calcFgpa() {
        //     const CGPAPARAGRAPH = document.getElementById("fin-calc");
        //     const GRADESSELECT = document.querySelectorAll("select.grade2");
        //     const GPAINP = document.querySelectorAll("input.curr_gpa");
        //     const UNITGPA = document.querySelectorAll("input.credit_units1");
        //     const UNITCLASS = document.querySelectorAll("input.credit_units2");
        //     const OGCREDITS = document.querySelector("input.credit_units0");
        //     const OGGPA = document.querySelector("input.oldGPA");

        //     //const courseReport = {};

        //     const listOfGrades = [];
        //     const listOfUnits = [];
        //     let totalUnits = 0;

        //     const listOfGPA = [];
        //     const listOfCredits = [];
        //     let totalCredits = 0;

        //     let originalCredit = parseInt(OGCREDITS.value);
        //     let originalGPA = parseFloat(OGGPA.value);
        //     console.log(originalCredit);
        //     console.log(originalGPA);

        //     GRADESSELECT.forEach((e) => {
        //         let GRADES = e.options;
        //         const selectedIndex = e.selectedIndex;
        //         const selectedGrade = GRADES[selectedIndex];
        //         const gradeValue = selectedGrade.text.toUpperCase();
        //         listOfGrades.push(gradeValue);
        //     });
        //     console.log(listOfGrades);

        //     UNITCLASS.forEach((e) => {
        //         const unitValue = parseInt(e.value);
        //         totalUnits += unitValue;
        //         listOfUnits.push(unitValue);
        //     });
        //     console.log(listOfUnits);

        //     GPAINP.forEach((a) => {
        //         const GPAValue = parseFloat(a.value);
        //         listOfGPA.push(GPAValue);
        //     });
        //     console.log(listOfGPA);

        //     UNITGPA.forEach((e) => {
        //         const creditValue = parseInt(e.value);
        //         totalCredits += creditValue;
        //         listOfCredits.push(creditValue);
        //     });
        //     console.log(listOfCredits);


        //     let totalEarnedUnits = 0;


        //     for (let i = 0; i < listOfUnits.length; i++) {
        //         if(listOfGrades[i] != "P"){
        //             totalEarnedUnits += this.gradeCalc(listOfGrades[i], listOfUnits[i]);
        //         }
        //         else{
        //             totalUnits -= listOfUnits[i];
        //         }

        //     }

        //     const gpaGrades = totalEarnedUnits / totalUnits;
        //     console.log(gpaGrades);

        //     let gpaUpdated = 0;

        //     totalCredits = originalCredit;


        //     for (let i = 0; i < listOfCredits.length; i++) {
        //         if(i==0){
        //             gpaUpdated = this.finClac(originalGPA, originalCredit+listOfCredits[i], listOfGPA[i], listOfCredits[i]);

        //         }
        //         else{
        //            gpaUpdated = this.finClac(gpaUpdated, totalCredits+listOfCredits[i], listOfGPA[i], listOfCredits[i]);
        //         }

        //         totalCredits += listOfCredits[i];
        //         console.log(gpaUpdated);


        //     }

        //     console.log(gpaUpdated);

        //     let finalGPA = 0;

        //     if(listOfUnits.length > 0 && listOfCredits.length > 0){
        //         finalGPA = this.finClac(gpaUpdated, totalCredits, gpaGrades, totalUnits);
        //         console.log(finalGPA);
        //     }
        //     else if(listOfCredits.length > 0){ 
        //         finalGPA = gpaUpdated;
        //         console.log(finalGPA);
        //     }
        //     else if(listOfUnits.length > 0){
        //         finalGPA = this.finClac(originalGPA, originalCredit, gpaGrades, totalUnits);
        //         console.log(finalGPA);
        //     }



        //     if (finalGPA >= 0){
        //         CGPAPARAGRAPH.textContent = "Your GPA is " + finalGPA.toFixed(2);
        //     } else {
        //         CGPAPARAGRAPH.textContent = "Please enter your correct grade and credit units";
        //     }
        // },

        // calcCgpa() {
        //     const CGPAPARAGRAPH = document.getElementById("cgpa-calc");
        //     const GRADESSELECT = document.querySelectorAll("select.grade1");
        //     const UNIT = document.querySelectorAll("input.credit-units");

        //     //const courseReport = {};

        //     const listOfGrades = [];
        //     const listOfUnits = [];
        //     let totalUnits = 0;

        //     GRADESSELECT.forEach((e) => {
        //         let GRADES = e.options;
        //         const selectedIndex = e.selectedIndex;
        //         const selectedGrade = GRADES[selectedIndex];
        //         const gradeValue = selectedGrade.text.toUpperCase();
        //         listOfGrades.push(gradeValue);
        //     });
        //     console.log(listOfGrades);

        //     UNIT.forEach((e) => {
        //         const unitValue = parseInt(e.value);
        //         totalUnits += unitValue;
        //         listOfUnits.push(unitValue);
        //     });
        //     console.log(listOfUnits);

        //     let totalEarnedUnits = 0;

        //     for (let i = 0; i < listOfUnits.length; i++) {
        //         if(listOfGrades[i] != "P"){
        //             totalEarnedUnits += this.gradeCalc(listOfGrades[i], listOfUnits[i]);
        //         }
        //         else{
        //             totalUnits -= listOfUnits[i];
        //         }

        //     }
        //     const gpa = totalEarnedUnits / totalUnits;

        //     if (gpa >= 0){
        //         CGPAPARAGRAPH.textContent = "Your GPA is " + gpa.toFixed(2);
        //     } else {
        //         CGPAPARAGRAPH.textContent = "Please enter your correct grade and credit units";
        //     }
        // },

        // clearFormTotal(){
        //     const mainForm = document.querySelectorAll("form.add_new1");
        //    	mainForm.forEach((e) => {
        //     	e.remove();
        //     });
        // },

        // clearFormSemester(){
        //     const mainForm = document.querySelectorAll("form.add_new");
        //    	mainForm.forEach((e) => {
        //     	e.remove();
        //     });
        // },

        // calcGrade(){

        //     const CGPAPARAGRAPH = document.getElementById("grade");
        //     const PERCENTAGES = document.querySelectorAll("input.Percent");
        //     const WEIGHTS = document.querySelectorAll("input.Weight");

        //     const listOfGrades = [];
        //     const listOfWeight = [];
        //     let totalWeight = 0;

        //     PERCENTAGES.forEach((e) => {
        //         const unitValue = parseFloat(e.value);
        //         listOfGrades.push(unitValue);
        //     });
        //     console.log(listOfGrades);

        //     WEIGHTS.forEach((a) => {
        //         const eachWeight = parseFloat(a.value);
        //         totalWeight+=eachWeight
        //         listOfWeight.push(eachWeight);
        //     });
        //     console.log(listOfWeight);


        //     let totalEarnedUnits = 0;


        //     for (let i = 0; i < listOfGrades.length; i++) {
        //         totalEarnedUnits+=listOfGrades[i]*listOfWeight[i];

        //     }

        //     const GradeIncludingWeight = totalEarnedUnits / totalWeight;
        //     console.log(GradeIncludingWeight);


        //     if (GradeIncludingWeight >= 0){
        //         CGPAPARAGRAPH.textContent = "Your Grade is " + GradeIncludingWeight.toFixed(2);
        //     } else {
        //         CGPAPARAGRAPH.textContent = "Please enter your correct grade and credit units";
        //     }
        // },

        // // addAssignment(){
        // //     let addNew = document.createElement("form");
        // //     addNew.classList.add("add_new2", `key-${this.counter}`);
        // //     const semester_name = `
        // //     <form class="add_new2 key-${this.counter}">
        // //         <input type="text" placeholder="Assignment/Exam" class="Assignment key-${this.counter}" optional>
        // //         <input type="number" placeholder="Grade(%)" class="Percent key-${this.counter}" required>
        // //         <input type="number" placeholder="Weight" class="Weight key-${this.counter}" required>

        // //     </form>
        // //     `;
        // //     addNew.innerHTML = semester_name;
        // //     document.getElementById("grade-wrapper").appendChild(addNew);
        // //     this.counter++;
        // // },
        // // removeAssignment() {
        // //     let mainForms = document.querySelectorAll("form.add_new2");
        // //     mainForms[mainForms.length-1].remove();
        // // },

    },
    computed: {
        ...mapState(["isLoading"]),
        ...mapState(["selectedSemester"]),
        ...mapGetters([COURSES]),
        ...mapGetters({ isLoggedIn: userTypes.getters.IS_LOGGED_IN }),

        loading() {
            return this.$store.state.isLoadingCourses;
        },

        courseObjects(){
            let columnArr = [[],[]];
            let courses = Object.values(this.selectedCourses).sort((a,b) => a.name - b.name);
            for (let i = 0; i < courses.length; i++) {
                if (i % 2 === 0) {
                    columnArr[0].push(courses[i]);
                } else {
                    columnArr[1].push(courses[i]);
                }
            }
            return columnArr;
        }
    
    },
    watch: {
        courses: {
            immediate: true,
            handler() {
                this.loadStudentCourses();
            },
        },
        isLoggedIn: {
            immediate: true,
            handler() {
                this.loadStudentCourses();
            },
        },
    },
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
    color: #aeb2b8;
    font-weight: bolder;
    margin-left: 6%;
}

#credit-row {
    font-size: 20px;
    color: #aeb2b8;
    font-weight: bolder;
    margin-left: 14%;
}

#grade-row {
    font-size: 20px;
    color: #aeb2b8;
    font-weight: bolder;
    margin-left: 8%;
}

.calculator-box {
    width: 50%;
    height: auto;
    border: rgba(108, 90, 90, 0.15);
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

p {
    padding: 10px;
    font-size: 1rem;
    color: black;
    text-align: center;
}

#course-wrapper,
form {
    color: white;
    margin: 0 auto;
    text-align: center;
    width: 100%;
}

input {
    padding: 10px;
    margin: 10px;
    border-radius: 5px;
    width: 25%;
    text-align: center;
}

select {
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
    border: rgba(108, 90, 90, 0.15);
    background-color: #AFC9C6;
}

.lastp p {
    color: black;
    text-align: center;
    padding: 10px;
    font-size: 30px;
    font-weight: bolder;
}

.no-courses {
    margin: 20px;
    border-style: solid;
    border-width: 2px;
    font-size: 16px;
    padding: 20px;
}

#selected-course-list {
    overflow-y: scroll !important;
    overflow-x: auto;
    min-height: 200px;
    flex-grow: 1;
    flex-basis: 0px;
    border-bottom: 1px solid #dbdbdc;
}
</style>
