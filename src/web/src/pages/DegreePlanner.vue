<template>
    <b-container fluid>
        <div class="main-loading" v-if="mainLoading">
          YACS<h1>&#32; &#32;Degree Planner</h1>
        </div>
        <div @dragover.prevent @drop="schedulerRemove">

        <div ref="searchModalContainer" style="position: absolute; z-index: 9999;">
          <SearchBarModal ref="searchModal" @result="results => modalAdd(activeSemester, results)" @dragover.prevent @elementDragStart="schedulerDragFromModal" @setSubjectColors="setSubjectColors" @setSubjectGroupColors="setSubjectGroupColors"></SearchBarModal>
        </div>
        <div class="columns">

          <div class="column-left">
            <div ref="deletionPrompt" class="schedule-deletion-prompt" v-show="scheduleDeletionPrompt">
              Confirm Deletion of {{ scheduleSelected }}?
              <div class="schedule-deletion-prompt-options">
                <span>
                  <button class="schedule-confirm-delete" @click="commenceDeleteSchedule(scheduleSelected)">
                    YES
                  </button>
                </span>
                <span>
                  <button class="schedule-deny-delete" @click="cancelDeleteSchedule">
                    NO
                  </button>
                </span>
              </div>
            </div>

            <div class="schedule-selection">
              <button :ref="'renameSchedule'" v-bind:class="{'schedule-selection-button':schedule != scheduleSelected, 'schedule-selection-button-active':schedule == scheduleSelected}" v-for="(schedule, index) in schedules" :key="index" @click="setSchedule(schedule)">
                <span class="schedule-button-content">
                  <button class="schedule-selection-delete" @click.stop="promptDeleteSchedule(schedule)">
                    &#10008;
                  </button>
                  <button class="schedule-selection-edit" @click="renameScheduleButton(schedule, index)">
                    &#9998;
                  </button>
                  <span v-show="scheduleBeingRenamed != schedule">{{ schedule }}</span>
                  <input :ref="'editScheduleNameInput'" v-show="scheduleBeingRenamed == schedule" class="edit-schedule-input" v-model="renameScheduleInputField" @keyup.enter="renameSchedule(schedule, renameScheduleInputField)"/>
                </span>
              </button>
              <input class="new-schedule-input" placeholder="+ new schedule" v-model="newScheduleInputField" @keyup.enter="addSchedule(newScheduleInputField)"/>
            </div>
            <div class="courses-grid">
              <div v-for="(semester, semester_index) in getSchedule(scheduleSelected)" :key="semester_index" 
                  v-bind:class="{'semester-block':hoverOverSemester!=semester_index, 'semester-block-highlighted':hoverOverSemester==semester_index}" 
                  @dragenter="schedulerDragEnter($event, semester_index)" 
                  @dragleave="schedulerDragLeave()" 
                  @dragover.prevent 
                  @drop="schedulerDrop($event, semester_index)">
                <div class="semester-title-row">
                  <span style="width: 100%;"><h3>Semester {{ semester_index + 1 }}</h3></span>
                  <span style="color:#a1a7a8; margin-top:-8px; margin-right:-8px;" class="schedule-search">
                    <button
                      type="button"
                      :ref="'addButton${index}'"
                      class="search-open"
                      @click="addCourseModal(semester_index)">
                      &#10010;
                    </button>
                  </span>
                </div>

                <div class="schedule-button-container" v-for="(course, course_index) in semester" :key="`${semester_index}-${course_index}`">
                  <button class="course-buttons" type="button" @click="goToCoursePage(course)" draggable="true" @dragstart="schedulerDrag($event, course, semester_index)">
                    <span style="color:#ffc680">{{ course.substring(0, 10) }}</span> <span style="color: #dae0e1;">{{ course.substring(10) }}</span>
                  </button>
                  <button class="course-remove-button" type="button" @click="remove(semester_index, course, true, true)">
                    <span style="color:#b05f6e">&#10008;</span>
                  </button>
                </div>

              </div>
            </div>
            
          </div>
          
          <div class="column-center" ref="columnCenter">
            <div v-if="scheduleSelected != ''">
              <div class="center-top-row">
                <div ref="degreeSelect" style="width: 180px">
                  <button class="toggle-degree-selection-button" @click="toggleDegreeSelectionMenu">Degree Selection</button>
                  <div class="degree-selection-menu" v-if="openedDegreeSelectionMenu">
                    <CatalogTree style="width: 50vw; margin-top: -10px" :nodes="degrees" :label="''" :depth="0" :subjectColors="subjectColors" :subjectGroupColors="subjectGroupColors" :labelAliases="labelAliases" :selectedDegree="degreeSelected" @setDegree="degree => setDegree(degree)"></CatalogTree>
                  </div>
                </div>
                <div v-if="recommendationsLoading" style="color: #727d80">
                  ...loading recommendations
                </div>
              </div>

              <div class="requirements-orggrid">
                <div v-bind:class="{'fulfillment-org-block-highlighted':highlightedFulfillment == group.name, 'fulfillment-org-block':highlightedFulfillment != group.name}" v-for="(group, group_index) in requirementGroups" :key="group_index" @click="toggleHighlightFulfillment(group.name)">
                  <div v-if="true">
                    <div class="group-heading">
                      <span class="group-title"> {{ group.name }} </span> 
                      <span v-if="group.minimum_requirements.credits > 0" 
                        v-bind:class="{'group-credit-stats-fulfilled':getTalliedAmount(group.name, 'credits') >= group.minimum_requirements.credits, 'group-credit-stats-unfulfilled':getTalliedAmount(group.name, 'credits') < group.minimum_requirements.credits}">
                        <span style="color:#707a7a"> credits:&nbsp;&nbsp; </span> {{ getTalliedAmount(group.name, 'credits') }} / {{ group.minimum_requirements.credits }} </span>
                    </div>
                    <div v-for="(requirement, index) in group.requirements" :key="index">
                      
                      <div v-if="requirements[requirement].wildcard_resolutions && Object.keys(requirements[requirement].wildcard_resolutions).length > 0">
                        <div v-for="(alternative_choices, alternative_orig) in requirements[requirement].wildcard_resolutions" :key="alternative_orig">
                          <div v-for="(alternative_choice, alternative_choice_index) in alternative_choices" :key="alternative_choice_index">
                            <button v-bind:class="{'alternative-buttons':chosenAlternative(alternative_orig) != alternative_choice, 'alternative-buttons-selected':chosenAlternative(alternative_orig) == alternative_choice}" type="button" @click.stop="toggleWildcardRequirement(alternative_orig, alternative_choice)">
                              {{ formatAlternativeButtonText(alternative_choice) }}
                            </button>
                          </div>
                        </div>
                      </div>

                      <div v-bind:class="{'minimal-fulfillment':requirements[requirement].actual_count >= requirements[requirement].required_count, 'minimal-unfulfilled-fulfillment':requirements[requirement].actual_count < requirements[requirement].required_count}">
                        <div v-bind:class="{'req-fulfilled':requirements[requirement].actual_count >= requirements[requirement].required_count, 'req-unfulfilled':requirements[requirement].actual_count < requirements[requirement].required_count}">
                          <div class="req-fulfillment-text">
                            <span class="req-fulfillment-name"> {{ formatFulfillmentName(requirements[requirement].name) }} </span> <span class="req-fulfillment-count"> {{ requirements[requirement].actual_count }} / {{ requirements[requirement].required_count }}</span>
                          </div>
                        </div>

                        <div v-for="(course, index) in requirements[requirement].fulfillment_set" :key="index">
                          <button class="course-buttons" type="button" @click="goToCoursePage(course)">
                            <span style="color:#e4ded5">{{ course.substring(0, 10) }}</span> <span style="color: #e6e8e9;">{{ course.substring(10) }}</span>
                          </button>
                        </div>
                      </div>

                      <div class="req-recommendations" v-if="requirement in recommendations && recommendations[requirement].length > 0 && recommendations[requirement][0].fulfillment_set.length > 0">
                        <div class="minimal-recommendations" v-for="(recommendation, recommendation_index) in recommendations[requirement]" :key="recommendation_index">
                          <div v-if="recommendations[requirement].length > 1">
                            <h5>{{ recommendation.specifications }}</h5>
                          </div>
                          <div class="minimal-recommendations-courses" v-for="(course, index) in recommendation.fulfillment_set" :key="index">
                            <button class="minimal-course-buttons" type="button" @click="goToCoursePage(course)" draggable="true" @dragstart="schedulerDrag($event, course, -1)">
                              <span style="color:#a9a9a9"> {{ course }} </span>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                </div>
              </div>
            </div>
          </div>

          <div class="column-right">
            <div class="schedule-selection" style="font-size: 16px;">
              <span style="color:#eb8d75">Schedule:</span> {{ scheduleSelected }} <br>
              <span style="color:#e6bc8a">Degree:</span> {{ degreeSelected }}
            </div>

            <div v-if="getRequirementGroup(highlightedFulfillment) == null">
              <div style="margin-top: 100px; color: #545f5f; font-size: 20px; font-weight: 700">
                Click on a Fulfillment Card to View Details!
              </div>
            </div>

            <div v-if="getRequirementGroup(highlightedFulfillment) != null">

              <div v-for="(requirement_name, index) in getRequirementGroup(highlightedFulfillment).requirements" :key="index">
                <div v-if="detailsAllPossibleCourses[requirement_name] && detailsAllPossibleCourses[requirement_name].length != 0" class="details-panel">
                  <div v-if="detailsLoading" style="color: #859393; font-size: 14px; font-weight: 600">
                    loading details...
                  </div>
                  <h5>{{ requirement_name }}:</h5>
                  <div class="details-wildcard-title" v-for="(fulfillment, fulfillment_index) in detailsAllPossibleCourses[requirement_name]" :key="fulfillment_index">
                    {{ fulfillment[0] }}
                    <div class="details-info" v-for="(course, index) in fulfillment[1]" :key="index">

                      <button v-if="coursePresentIn(course).includes(requirement_name)" class="course-buttons" type="button" @click="goToCoursePage(course)">
                        <span style="color: #ffc680; font-weight: 600;">{{ course.substring(0, 10) }}</span> <span style="color: #85c07d; font-weight: 600;">{{ course.substring(10) }}</span> <span style="color: #9db09b; font-weight: 600;">(applied)</span>
                      </button>

                      <button v-if="coursePresentIn(course).length > 0 && !coursePresentIn(course).includes(requirement_name)" class="course-buttons" type="button" @click="goToCoursePage(course)">
                        <span style="color: #c0a17c; font-weight: 600;">{{ course.substring(0, 10) }}</span> <span style="color: #ded190; font-style: italic; font-weight: 600;">{{ course.substring(10) }}</span> <span style="color: #b0a59b; font-weight: 600;">applied to: ({{ coursePresentIn(course).join(', ') }})</span>
                      </button>

                      <button v-if="coursePresentIn(course).length == 0" class="course-buttons" type="button" @click="goToCoursePage(course)" draggable="true" @dragstart="schedulerDrag($event, course, -1)">
                        <span style="color:#c0a17c">{{ course.substring(0, 10) }}</span> {{ course.substring(10) }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </b-container>
</template>
  
<script>

import SearchBarModal from '../components/SearchBarModal.vue';
import CatalogTree from '@/components/CatalogTree.vue';
import Vue from 'vue';
import VueCookies from 'vue-cookies';

Vue.use(VueCookies);

  export default {
    data() {
        return {
          /* -------- FLAGS AND MENU TOGGLES -------- */
          mainLoading: true,
          detailsLoading: false,
          recommendationsLoading: false,
          scheduleDeletionPrompt: false,
          openedDegreeSelectionMenu: false,
          highlightedFulfillment: null,
          switchedSchedule: true, // flag indicates schedule has switched and to recompute certain calculations

          // scheduler flags
          dragElement: null,
          dragFromSemester: -1,
          hoverOverSemester: -1,
          lastDropInsideZone: false, // indicates if course is dropped within scheduler (since dropping outside means removal)
          hoverCounter: 0, // entering child elements creates a dragenter + dragleave event
          activeSemester: -1,
          showSearchModal: false,
          scheduleBeingRenamed: '', // stores the name of the schedule currently being renamed
          scheduleBeingRenamedIndex: -1, // stores the index of the schedule being modified for the sake of tracking clickOutside

          /* -------- DEFAULTS AND COMPUTED PROPERTIES -------- */
          defaultScheduleName: 'my schedule',
          SemestersMax: 12,
          labelAliases: {},
          subjectColors: {},
          subjectGroupColors: {},

          /* -------- USERDATA -------- */
          userid: 'nulluser',

          schedules: [], // a flat structure, can be replaced by a folder structure
          scheduleSelected: '',
          
          degrees: {}, // follow a folder structure
          degreeSelected: '',

          scheduleData: {}, // a dictionary of schedules containing course information and degree information for each schedule
          wildcardRequirements: {},

          requirementGroups: [],
          tally: {},
          requirements: {},
          recommendations: {},
          detailsAllTakenCourses: {},
          detailsAllPossibleCourses: {},

          /* -------- INPUT FIELDS -------- */
          newScheduleInputField: '',
          renameScheduleInputField: '',
        };
    },
    methods: {
        async computeHash(inputString) {
          const encoder = new TextEncoder();
          const string = encoder.encode(inputString);
          const hashBuffer = await crypto.subtle.digest('SHA-256', string);

          // Convert hash to hexadecimal
          const hashArray = Array.from(new Uint8Array(hashBuffer));
          const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');

          return hashHex;
        },
        async beginTemporarySession() {
          console.log('registering new accountless session');
          let start = performance.now();
          const response = await fetch("/api/dp/newuser");
          const hashdata = await response.json();
          const hash = hashdata.hashhead;
          const difficulty = hashdata.difficulty;
          let suffix = 1;
          while ((await this.computeHash(hash + suffix.toString())).substring(0, difficulty.length) != difficulty) {
            suffix++;
          }
          this.userid = hash + suffix.toString();
          let end = performance.now();
          console.log(`registered with USERID: ${this.userid} in ${end - start} milliseconds`);
        },
        ////////////////////////////////////////////////
        // COOKIES
        ////////////////////////////////////////////////

        loadUser() {
          let userid = this.getFromLocalStorage('userid');
          if (userid) {
            this.userid = userid;
          }
          let schedules = this.getFromLocalStorage('schedules');
          if (schedules) {
            this.schedules = JSON.parse(schedules);
          }
          let hangingSchedules = [];
          for (let i = 0; i < this.schedules.length; ++i) {
            let key = 's:' + this.schedules[i];
            const courseData = this.getFromLocalStorage(key);
            if (courseData == null) {
              hangingSchedules.push(this.schedules[i]);
            } else {
              let courseDataJson = JSON.parse(courseData);
              if (courseDataJson && courseDataJson.courses && courseDataJson.degree != null) {
                this.scheduleData[this.schedules[i]] = courseDataJson;
              } else {
                this.removeFromLocalStorage(key);
                hangingSchedules.push(this.schedules[i]);
              }
            }
          }

          for (let i = 0; i < hangingSchedules.length; ++i) {
            this.schedules.splice(this.schedules.indexOf(hangingSchedules[i]), 1);
            console.log('removed excess ' + hangingSchedules[i]);
          }

          if (this.schedules.length > 0) {
            this.setSchedule(this.schedules[0], false);
          } else {
            this.addSchedule(this.defaultScheduleName);
            this.setSchedule(this.defaultScheduleName, false);
          }
        },

        loadUserid() {
          let userid = this.getFromLocalStorage('userid');
          if (userid) {
            this.userid = userid;
          }
        },

        saveUserid() {
          this.saveToLocalStorage('userid', this.userid);
        },

        saveuser() {
          this.cleanseSchedules();
          this.saveToLocalStorage('userid', this.userid);
          this.saveToLocalStorage('schedules', JSON.stringify(this.schedules));
          for (let i = 0; i < this.schedules.length; ++i) {
            this.saveToLocalStorage('s:' + this.schedules[i], JSON.stringify(this.scheduleData[this.schedules[i]]));
          }
        },

        cleanseSchedules() {
          const keys = [];
          for (let i = 0; i < localStorage.length; i++) {
              keys.push(localStorage.key(i));
              // console.log('localstorage: ' + localStorage.key(i) + ' DATA: ' + this.getFromLocalStorage(localStorage.key(i)));
          }
          // delete all previously saved schedule data
          keys.forEach(key => {
            if (key.startsWith('s:')) {
              this.removeFromLocalStorage(key);
            }
          });
        },

        saveToLocalStorage(key, value) {
            try {
              localStorage.setItem(key, value);
              return true;
            } catch (error) {
              console.error("Failed to save to localStorage:", error);
              return false;
            }
        },
        getFromLocalStorage(key) {
            try {
                const value = localStorage.getItem(key);
                if (value == "undefined") {
                  return undefined;
                }
                return value;
            } catch (error) {
                console.error("Failed to retrieve from localStorage:", error);
                return null;
            }
        },
        removeFromLocalStorage(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (error) {
                console.error("Failed to remove from localStorage:", error);
                return false;
            }
        },

        updateCookie(key, value, duration="366d") {
          this.$cookies.set(key, value, duration);
        },

        removeCookie(key) {
          this.$cookies.remove(key);
        },

        getCookie(key) {
          const value = this.$cookies.get(key);
          return value
        },

        ////////////////////////////////////////////////
        // LOGIC HELPERS
        ////////////////////////////////////////////////

        getAllCourses(schedule) {
          let courses = [];
          if (!this.scheduleData[schedule]) {
            return courses
          }
          for (let i = 0; i < this.scheduleData[schedule].courses.length; ++i) {
            for (let j = 0; j < this.scheduleData[schedule].courses[i].length; ++j) {
              courses.push(this.scheduleData[schedule].courses[i][j]);
            }
          }
          return courses
        },

        coursePresentIn(course) {
          // returns the list of requirements that the course is present in
          let presentIn = [];
          for (const requirement in this.requirements) {
            if (this.requirements[requirement].fulfillment_set.includes(course)) {
              presentIn.push(requirement);
            }
          }
          return presentIn
        },
        getRequirementGroup(name, firstOnly=true) {
          // gets requirement group by name
          if (this.requirementGroups.length == 0) {
            return null
          }
          let filteredGroup = this.requirementGroups.filter(group => group.name == name);

          if (filteredGroup.length > 0) {
            if (firstOnly) {
              return filteredGroup[0]
            }
            return filteredGroup
          }
          return null
        },
        handleClickOutside(event) {
          // Check if the clicked element is outside both the input box and the results list
          if (
            this.activeSemester >= 0 &&
            this.$refs['addButton${index}'][this.activeSemester] &&
            !this.$refs['addButton${index}'][this.activeSemester].contains(event.target) &&
            this.$refs.searchModalContainer &&
            !this.$refs.searchModalContainer.contains(event.target)
          ) {
            this.toggleSearchModal(false);
          }
          if (this.scheduleBeingRenamedIndex >= 0 && this.$refs['renameSchedule'][this.scheduleBeingRenamedIndex] && !this.$refs['renameSchedule'][this.scheduleBeingRenamedIndex].contains(event.target)) {
            this.renameScheduleInputField = '';
            this.scheduleBeingRenamed = '';
          }
          if (this.$refs.deletionPrompt && !this.$refs.deletionPrompt.contains(event.target)) {
            this.cancelDeleteSchedule();
          }
          if (this.$refs.degreeSelect && !this.$refs.degreeSelect.contains(event.target)) {
            this.openedDegreeSelectionMenu = false;
          }
        },
        getTalliedAmount(groupName, tally) {
            if (this.tally[groupName][tally] == null) {
                return 0;
            }
            return this.tally[groupName][tally];
        },

        ////////////////////////////////////////////////
        // RENDERING HELPERS
        ////////////////////////////////////////////////

        delayedFinishedLoading(timer=1000) {
          // Calling the method with a delay
          setTimeout(this.finishedLoading, timer);
        },
        finishedLoading() {
          this.mainLoading = false;
        },

        toggleDegreeSelectionMenu() {
          this.openedDegreeSelectionMenu = (!this.openedDegreeSelectionMenu);
        },
        setSubjectColors(colors) {
          this.subjectColors = colors;
        },
        setSubjectGroupColors(colors) {
          this.subjectGroupColors = colors;
        },
        toggleHighlightFulfillment(group) {
          if (group == this.highlightedFulfillment) {
            this.highlightedFulfillment = null;
          } else {
            this.highlightedFulfillment = group;
          }
        },
        toggleSearchModal(on) {
          this.showSearchModal = on;
          this.$refs.searchModal.showSelf = on;
          if (!on) {
            this.$refs.searchModal.onClose();
          }
        },

        formatAlternativeButtonText(str) {
            if (str.includes('*')) {
                str = str.split('*')[0] + " automatically select";
            }
            str = str.replace('.', ': ');
            str = str.replace(' -', '');
            str = str.replace('-', '');
            return str;
        },
        formatFulfillmentName(str) {
            if (str.includes('-')) {
                str = str.substring(str.indexOf('-') + 1);
            }
            return str;
        },

        generateSearchOccurrences() {
          const courses = this.scheduleData[this.scheduleSelected].courses;
          let elementSelectionOccurrences = {};
          for (let semester = 0; semester < courses.length; ++semester) {
            for (let i = 0; i < courses[semester].length; ++i) {
              const course_name = courses[semester][i];
              if (course_name in elementSelectionOccurrences) {
                elementSelectionOccurrences[course_name].push(semester + 1);
              }
              else {
                elementSelectionOccurrences[course_name] = [semester + 1];
              }
            }
          }
          return elementSelectionOccurrences
        },

        ////////////////////////////////////////////////
        // USER ACTIONS
        ////////////////////////////////////////////////

        // wildcards

        toggleWildcardRequirement(alternative_orig, alternative_choice) {
          // don't recalculate if the user spams the original button
          if ((!(alternative_orig in this.wildcardRequirements) && alternative_choice == alternative_orig) || (alternative_orig in this.wildcardRequirements && this.wildcardRequirements[alternative_orig] == alternative_choice)) {
            return
          }
          if (alternative_orig == alternative_choice) {
            delete this.wildcardRequirements[alternative_orig];
          } else {
            this.wildcardRequirements[alternative_orig] = alternative_choice
          }
          this.queryCalculations(true, true);
        },
        chosenAlternative(alternative_orig) {
          if (alternative_orig in this.wildcardRequirements) {
            return this.wildcardRequirements[alternative_orig]
          }
          return alternative_orig
        },

        // scheduler
        
        schedulerDragFromModal(course) {
          this.schedulerDrag(null, course, -1);
        },
        addCourseModal(semester) {
          if (this.showSearchModal && this.activeSemester == semester) {
            this.toggleSearchModal(false);
            return
          }
          this.activeSemester = semester;
          this.toggleSearchModal(true);
          if (this.switchedSchedule) {
            this.$refs.searchModal.elementSelectionOccurrences = this.generateSearchOccurrences();
            this.switchedSchedule = false;
          }
          this.$refs.searchModal.onOpen("SEMESTER " + (semester + 1).toString());
          document.removeEventListener('click', this.handleClickOutside);
          document.addEventListener('click', this.handleClickOutside);
          this.$nextTick(() => {
            const targetDiv = this.$refs.columnCenter;
            const targetDivRect = targetDiv.getBoundingClientRect();
            const searchModal = this.$refs.searchModalContainer;
            searchModal.style.left = targetDivRect.left + 'px';
            searchModal.style.top = targetDivRect.top - searchModal.offsetHeight + 'px';
          });
        },
        modalAdd(semester, course) {
          if (this.scheduleData[this.scheduleSelected].courses[semester].includes(course)) {
            this.remove(semester, course, true, true);
          }
          else {
            this.add(semester, course, true, true);
          }

          if (this.$refs.searchModal.closeModalOnSelection) {
            this.toggleSearchModal(false);
          }
        },
        schedulerDrag(event, item, semester) {
            this.dragElement = item;
            this.dragFromSemester = semester;
            this.lastDropInsideZone = false;
            if (event != null) {
              event.dataTransfer.effectAllowed = "move";
            }
        },
        schedulerDrop(event, dragToSemester) {
            event.preventDefault();
            if (this.dragElement != null) {
                if (this.dragFromSemester == -1) {
                    this.add(dragToSemester, this.dragElement, true, true);
                }
                else if (this.dragFromSemester != -1 && this.dragFromSemester != dragToSemester) {
                    this.remove(this.dragFromSemester, this.dragElement, false, false);
                    this.add(dragToSemester, this.dragElement, false, false);
                }
            }
            this.hoverCounter = 0;
            this.hoverOverSemester = -1;
            this.lastDropInsideZone = true;
        },
        schedulerRemove(event) {
          //console.log("remove func activated, hover counter: " + this.hoverCounter + " hoveroversem: " + this.hoverOverSemester + " dragFromSemester: " + this.dragFromSemester + ", " + this.dragElement);
          if (this.dragFromSemester == -1 || this.hoverOverSemester != -1 || this.lastDropInsideZone) {
            return
          }
          event.preventDefault();
          if (this.dragElement != null) {
              if (this.dragFromSemester != -1) {
                  this.remove(this.dragFromSemester, this.dragElement, true, true);
              }
          }
          this.hoverOverSemester = -1;
        },
        schedulerDragEnter(event, hoverOverSemester) {
            event.preventDefault();
            this.hoverOverSemester = hoverOverSemester;
            this.hoverCounter++;
        },
        schedulerDragLeave() {
            this.hoverCounter--;
            if (this.hoverCounter == 0) {
                this.hoverOverSemester = -1;
            }
        },
        goToCoursePage(course) {
            let page = course.substring(0, 4).toUpperCase() + "/" + course.substring(0, 4).toUpperCase() + "-" + course.substring(5, 9);
            this.$router.push("/explore/" + page);
        },

        add(semester, course, fulfill = true, recommend = true) {
          if (this.scheduleData[this.scheduleSelected].courses[semester].includes(course)) {
            return
          }
          this.scheduleData[this.scheduleSelected].courses[semester].push(course);
          this.$forceUpdate();
          this.$refs.searchModal.elementSelectionOccurrences = this.generateSearchOccurrences();
            
          // skips fulfill/recommend if this course occurs multiple times
          if (!(course in this.$refs.searchModal.elementSelectionOccurrences && this.$refs.searchModal.elementSelectionOccurrences[course].length > 1) && (fulfill || recommend)) {
            this.queryCalculations(fulfill, recommend);
          }

          this.saveuser();
        },
        remove(semester, course, fulfill = true, recommend = true) {
          if (!this.scheduleData[this.scheduleSelected].courses[semester].includes(course)) {
            return
          }
          const index = [this.scheduleData[this.scheduleSelected].courses[semester].indexOf(course)];
          this.scheduleData[this.scheduleSelected].courses[semester].splice(index, 1);
          this.$forceUpdate();
          this.$refs.searchModal.elementSelectionOccurrences = this.generateSearchOccurrences();
            
          // skips fulfill/recommend if this course still occurs
          if (!(course in this.$refs.searchModal.elementSelectionOccurrences && this.$refs.searchModal.elementSelectionOccurrences[course].length > 0) && (fulfill || recommend)) {
            this.queryCalculations(fulfill, recommend);
          }
          
          this.saveuser();
        },

        ////////////////////////////////////////////////
        // API CALLING
        ////////////////////////////////////////////////

        async validateSession() {
          const response = await fetch('/api/dp/validateid/' + this.userid);
          const responseJson = await response.json();
          if (!responseJson.valid) {
            await this.beginTemporarySession();
          }
          return responseJson.valid
        },

        async queryCalculations(fulfill = true, recommend = true) {
            // performs fulfillment call first before validation. This ensures that if our ID is valid,
            // fulfillment is underway without needing to wait for a validation call.
            // validation call then occurs after fulfillment call, and if it fails, we revalidate and rerun this function.
            if (fulfill) {
              this.getFulfillment(this.wildcardRequirements);
              this.getFulfillmentDetails();
            }
            let valid = await this.validateSession();
            if (!valid) {
              await this.queryCalculations(fulfill, recommend);
              return
            }
            if (recommend) {
              this.getRecommendations();
            }
        },

        async getFulfillment(attributes_replacement = null) {
            let userid = this.userid;
            let degree_name = this.degreeSelected;
            let taken_courses = this.getAllCourses(this.scheduleSelected);
            if (attributes_replacement == null) {
              attributes_replacement = {};
            }
            const response = await fetch('/api/dp/fulfillment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userid, degree_name, taken_courses, attributes_replacement }),
            });
            const fulfillment = await response.json();
            if (fulfillment) {
              this.requirements = fulfillment.fulfillments;
              this.requirementGroups = fulfillment.groups;
              this.tally = fulfillment.tally;
            }
            else {
              this.requirements = {};
              this.requirementGroups = [];
            }
        },
        async getFulfillmentDetails() {
          let userid = this.userid;
          this.detailsLoading = true;
          const response = await fetch('/api/dp/fulfillmentdetails/' + userid);
          const results = await response.json();
          if (results) {
            this.detailsAllPossibleCourses = results.details_all_possible;
            //console.log(`detailsAllPossible: ${JSON.stringify(this.detailsAllPossibleCourses)}`)
            this.detailsAllTakenCourses = results.details_all_taken;
          }
          this.detailsLoading = false;
        },
        async getRecommendations() { 
            this.recommendationsLoading = true;
            let userid = this.userid;
            let degree_name = this.degreeSelected;
            let attributes_replacement = this.wildcardRequirements;
            let taken_courses = this.getAllCourses(this.scheduleSelected);
            await fetch('/api/dp/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userid, degree_name, taken_courses, attributes_replacement }),
            });
            const response2 = await fetch('/api/dp/recommend/' + userid);
            const recommendations = await response2.json();
            if (recommendations) {
              this.recommendations = recommendations;
            }
            this.recommendationsLoading = false;
        },
        async getInfo() {
          const response  = await fetch('/api/dp/info');
          const responseData = await response.json();
          this.degrees = responseData.degrees;
        },

        setDegree(degreeName, queryCalculations=true) {
          if (degreeName.toLowerCase() == this.degreeSelected.toLowerCase()) {
            return
          }
          this.degreeSelected = degreeName;
          if (this.scheduleData[this.scheduleSelected]) {
            this.scheduleData[this.scheduleSelected].degree = this.degreeSelected;
          }
          if (this.openedDegreeSelectionMenu) {
            this.openedDegreeSelectionMenu = false;
          }
          console.log('setting degree to ' + degreeName)
          if (queryCalculations) {
            this.queryCalculations();
          }
        },
        getDegree() {
          if (!this.scheduleData[this.scheduleSelected]) {
            return ''
          }
          return this.scheduleData[this.scheduleSelected].degree
        },
        promptDeleteSchedule(schedule) {
          document.removeEventListener('click', this.handleClickOutside);
          document.addEventListener('click', this.handleClickOutside);
          this.scheduleSelected = schedule;
          this.scheduleDeletionPrompt = true;
        },

        cancelDeleteSchedule() {
          this.scheduleDeletionPrompt = false;
        },

        commenceDeleteSchedule(schedule) {
          this.scheduleDeletionPrompt = false;
          this.deleteSchedule(schedule);
        },

        renameScheduleButton(schedule, index) {
          document.removeEventListener('click', this.handleClickOutside);
          document.addEventListener('click', this.handleClickOutside);
          this.scheduleBeingRenamed = schedule;
          this.renameScheduleInputField = schedule;
          this.scheduleBeingRenamedIndex = index;
          this.$nextTick(() => {
            if (this.$refs['editScheduleNameInput'][this.scheduleBeingRenamedIndex]) {
              this.$refs['editScheduleNameInput'][this.scheduleBeingRenamedIndex].focus();
            }
          });
        },

        addSchedule(scheduleName, courseData = null) {
          if (this.schedules.includes(scheduleName)) {
            this.setSchedule(scheduleName);
            return
          }
          if (courseData == null) {
            let courseDataCourses = [];
            for (let i = 0; i < this.SemestersMax; i++) {
              courseDataCourses.push([]);
            }
            courseData = {'courses': courseDataCourses, 'degree': ''};
          }
          this.schedules.push(scheduleName);
          this.scheduleData[scheduleName] = courseData;
          this.setSchedule(scheduleName);

          this.saveuser();
        },

        deleteSchedule(scheduleName) {
          delete this.scheduleData[scheduleName];
          this.schedules.splice([this.schedules.indexOf(scheduleName)], 1);
          if (scheduleName == this.scheduleSelected && this.schedules.length > 0) {
            this.setSchedule(this.schedules[0]);
          }
          if (this.schedules.length == 0) {
            this.scheduleSelected = '';
          }
          this.scheduleBeingRenamed = '';
          this.renameScheduleInputField = '';
          this.newScheduleInputField = '';

          this.saveuser();
        },

        setSchedule(scheduleName, queryCalculations=true) {
          if (this.scheduleSelected == scheduleName) {
            return
          }
          this.scheduleSelected = scheduleName;
          this.degreeSelected = this.getDegree();
          this.scheduleBeingRenamed = '';
          this.renameScheduleInputField = '';
          this.newScheduleInputField = '';
          this.switchedSchedule = true;
          if (queryCalculations) {
            this.queryCalculations();
          }
        },

        renameSchedule(oldScheduleName, newScheduleName) {
          if (oldScheduleName == newScheduleName || this.schedules.includes(newScheduleName)) {
            return
          }
          this.addSchedule(newScheduleName, this.scheduleData[oldScheduleName]);
          this.deleteSchedule(oldScheduleName);
          this.scheduleSelected = newScheduleName;

          this.saveuser();
        },

        getSchedule(scheduleName) {
          if (!(this.scheduleData[scheduleName] && this.scheduleData[scheduleName].courses)) {
            return [];
          }
          return this.scheduleData[scheduleName].courses;
        },

        setlabelAliases() {
          this.labelAliases = {
            "computer science": "CSCI",
            "electrical engineering": "ECSE",
            "mechanical engineering": "MANE",
            "electronic arts": "ARTS",
            "architecture": "ARCH",
            "business and management": "MGMT",

            "computer science + computer engineering": "CSCI",

            "school of engineering": "engineering",
            "school of science": "science",
            "school of humanities": "humanities",
            "school of architecture": "architecture",
            "lally school of management": "business"
          };
        },
    },
    async created() {
        console.log('DEGREE PLANNER - PROJECT OVERLORD / YACS.N 2023');
        
        this.mainLoading = true;
        this.loadUserid();
        await this.validateSession();
        this.saveUserid();
        console.log('session validated');

        this.loadUser();
        await this.getInfo();
        await this.queryCalculations();
        this.setlabelAliases();
        if (this.degreeSelected.length == 0) {
          this.openedDegreeSelectionMenu = true;
        }
        document.addEventListener('click', this.handleClickOutside);
        this.finishedLoading();
    },
    components: { SearchBarModal, CatalogTree }
};
</script>
  
<style scoped>
  .main-loading {
    text-align:center;
    font-size:128px;
    font-weight:600;
    color:#e19e8c;
    position: fixed;
    display: flex;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background-color: rgba(8, 26, 32, 0.85);
    backdrop-filter: blur(4px);
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  .degree-selection-menu {
    position: absolute;
    z-index: 999;
  }
  .main-loading h1 {
    font-size:0.9em;
    margin: 30px;
    color:#cadbdb;
  }
  .schedule-selection {
    margin: 2px;
    padding: 2px;
    color:#d7dde3;
  }
  .schedule-button-content {
    justify-items: left;
    display: flex;
  }
  .schedule-selection-button {
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    min-width: 120px;
    border: none;
    padding: 1px;
    padding-left: 2px;
    padding-right: 2px;
    margin: 2px;
    color:rgb(190, 199, 205);
    background-color: rgba(51, 58, 61, 0.8);
    transition: background-color 0.2s ease;
  }
  .schedule-selection-button:hover {
    background-color: rgba(84, 92, 95, 0.8);
  }

  .schedule-selection-button-active {
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    min-width: 120px;
    border: solid 1px #74808a;
    padding-left: 2px;
    padding-right: 2px;
    margin: 2px;
    color:rgb(227, 234, 237);
    background-color: rgba(91, 102, 106, 0.8);
    transition: background-color 0.2s ease;
  }
  .schedule-selection-button-active:hover {
    background-color: rgba(122, 132, 136, 0.8);
  }
  .schedule-selection-delete {
    border-radius: 8px;
    font-size: 10px;
    width: 16px;
    border: none;
    margin: 1px;
    padding: 0px;
    color: #dc8664;
    background-color:rgba(135, 150, 155, 0.1);
  }
  .schedule-selection-delete:hover {
    background-color: rgba(135, 150, 155, 0.8);
  }
  .schedule-selection-edit {
    border-radius: 8px;
    font-size: 11px;
    width: 16px;
    border: none;
    margin: 1px;
    padding: 0px;
    color: #b5b5d6;
    background-color:rgba(135, 150, 155, 0.1);
  }
  .schedule-selection-edit:hover {
    background-color: rgba(135, 150, 155, 0.8);
  }
  .edit-schedule-input {
    font-size: 11px;
    color:#89949d;
    width: 70px;
    border: none;
    margin: 1px;
  }
  .new-schedule-input {
    font-size: 12px;
    color:#ced8e0;
    background-color:#3f474e;
    width: 130px;
    border: none;
    margin: 2px;
    padding: 2px;
    padding-right: 4px;
    padding-left: 4px;
    border-radius: 4px;
  }
  .new-schedule-input::placeholder {
    color: #cad4db;
    opacity: 0.7;
  }
  .schedule-deletion-prompt {
    position: absolute;
    z-index: 9999;
    font-size: 18px;
    font-weight: 700;
    text-justify: center;
    border: 2px solid rgba(161, 207, 224, 1 );
    border-radius: 4px;
    padding: 16px;
    margin: 8px;
    top: 180px;
    color: #202121;
    background-color:rgba(161, 207, 224, 0.7);
  }
  .schedule-deletion-prompt-options {
    width: 100%;
    display: flex;
    justify-content: center;
    justify-items: center;
  }
  .schedule-confirm-delete {
    font-size: 16px;
    font-weight: 600;
    border: 2px solid rgb(218, 140, 106);
    border-radius: 4px;
    padding: 6px;
    width: 64px;
    margin: 4px;
    color:#121313;
    background-color:rgba(230, 165, 135, 0.85);
  }
  .schedule-deny-delete {
    font-size: 16px;
    font-weight: 600;
    border: 2px solid rgba(212, 225, 224, 1);
    border-radius: 4px;
    padding: 6px;
    width: 64px;
    margin: 4px;
    color:#171d1a;
    background-color:rgba(212, 225, 224, 0.85);
  }
  .search-modal {
    position: absolute;
    z-index: 9999;
    list-style: none;
    border-radius: 4px;
    border-top: none;
  }
  .toggle-degree-selection-button {
    margin: 2px;
    padding: 6px;
    padding-left: 12px;
    padding-right: 12px;
    border-radius: 4px;
    border: none;
    font-size: 16px;
    color:#9faab2;
    background-color: #323434;
  }
  .toggle-degree-selection-button:hover {
    color:#a7aeb5;
    background-color: #56585e;
  }
  .schedule-search {
    justify-self: right;
    z-index: 999;
    padding: 0;
  }
  .search-open {
    border-radius: 4px;
    font-size: 16px;
    align-content: center;
    border: none;
    padding: 1px;
    padding-left: 8px;
    padding-right: 8px;
    margin: 0px;
    color:rgb(153, 160, 164);
    background-color: rgba(197, 211, 218, 0.1);
    transition: background-color 0.2s ease;
    font-weight: 900;
  }
  .search-open:hover {
    background-color: #60666d;
  }
  .semester-title-row {
    display: flex;
  }
  .center-top-row {
    display: flex;
  }
  .columns {
    display: flex;
    height: 90vh;
    width: 100%;
  }
  .column-left {
    flex: 8;
    overflow-y: auto;
    padding: 4px;
    border: 1px solid #171d1a;
    background-color:#272a2c;
    font-size: 0.8em;
    min-width: 400px;
    max-width: 650px;
  }
  .column-left::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .column-center {
    flex: 11;
    overflow-y: auto;
    padding: 4px;
    background-color:rgb(36, 37, 40);
    justify-content: center;
    border: 1px solid #171d1a;
  }
  .column-center::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .column-right {
    flex: 5;
    overflow-y: auto;
    padding: 4px;
    border: 1px solid #171d1a;
    background-color:#272a2c;
    font-size: 0.8em;
    min-width: 280px;
    max-width: 450px;
  }
  .column-right::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .requirements-orggrid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    justify-content: center;
    gap: 1px;
  }
  .courses-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0px;
    position: relative;
  }
  .semester-block {
    border: 2px solid #43494f;
    border-radius: 6px;
    padding: 6px;
    margin: 2px;
    font-size: 0.75em;
    background-color: rgba(8, 26, 32, 0.35);
  }
  .semester-block h3 {
    font-size: 1.5em;
    color: #98bdd4;
  }
  .semester-block-highlighted {
    border: 2px solid #43494f;
    border-radius: 6px;
    padding: 6px;
    margin: 2px;
    font-size: 0.75em;
    background-color: rgba(69, 94, 104, 0.35);
    position: relative;
  }
  .semester-block-highlighted h3 {
    font-size: 1.5em;
    color: #98bdd4;
  }
  .schedule-button-container {
    display: flex;
  }
  .text-input{
    border:2px solid #21242b;
    border-radius:4px;
    width:100%;
    padding:4px;
    background-color:#393b40;
  }
  .fulfillment-org-block {
    border: 2px solid #43494f;
    border-radius: 8px;
    padding: 6px;
    margin: 2px;
    width: 320px;
    min-height: 60px;
    align-items: center;
    font-size: 0.65em;
    background-color: rgba(8, 26, 32, 0.35);
    transition: background-color 0.2s ease;
    backdrop-filter: blur(4px);
  }
  .fulfillment-org-block:hover {
    background-color: rgba(46, 51, 53, 0.35);
  }
  .fulfillment-org-block-highlighted {
    border: 2px solid #676b70;
    border-radius: 8px;
    padding: 6px;
    margin: 2px;
    width: 320px;
    min-height: 60px;
    align-items: center;
    font-size: 0.65em;
    background-color: rgba(45, 50, 52, 0.35);
    backdrop-filter: blur(4px);
  }
  .fulfillment-org-block h3, .fulfillment-org-block-highlighted h3 {
    font-size: 1.2em;
  }
  .fulfillment-org-block h5, .fulfillment-org-block-highlighted h5 {
    font-size: 1.1em;
    margin: 0px;
    color: #beb8b1;
  }
  .group-heading {
    display: flex;
    margin-bottom: 4px;
  }
  .group-heading .group-title {
    color:#78b2d9; 
    font-size: 1.8em;
    flex: 0.97;
    padding-left: 2%;
  }
  .group-heading .group-credit-stats-fulfilled {
    font-size: 1.8em;
    font-weight: 700;
    color: #86bea9;
  }
  .group-heading .group-credit-stats-unfulfilled {
    font-size: 1.8em;
    font-weight: 700;
    color: #be8886;
  }
  .course-buttons {
    border: none;
    border-radius: 4px;
    flex: 1;
    padding: 0px;
    width: 99%;
    margin: 1px;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.2s ease;
    text-align: left;
  }
  .course-buttons:hover {
    background-color: rgba(13, 23, 26, 0.78);
  }
  .req-fulfillment-text {
    display:flex;
    margin-left: 4px;
    margin-right: 4px;
    font-size: 1.3em;
    font-weight: 500;
  }
  .req-fulfillment-text .req-fulfillment-name {
    color: rgb(163, 185, 189);
    flex: 1;
  }
  .req-fulfillment-text .req-fulfillment-count {
    font-weight: 650;
    font-size: 1.2em;
  }
  .minimal-fulfillment {
    padding-left: 4px;
    padding-right: 4px;
    padding: 1px;
    margin: 0px;
    border-radius: 4px;
    background-color: #414740;
  }
  .minimal-unfulfilled-fulfillment {
    padding-left: 4px;
    padding-right: 4px;
    padding: 1px;
    margin: 0px;
    border-radius: 4px;
    background-color: #4f433e;
  }
  .req-recommendations {
    margin-bottom: 10px;
  }
  .minimal-course-buttons {
    border: none;
    border-radius: 2px;
    flex: 1;
    padding: 0px;
    margin: 1px;
    margin-right: 5px;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.15s ease;
    text-align: left;
  }
  .minimal-course-buttons:hover {
    background-color: rgba(13, 23, 26, 0.78);
  }
  .minimal-recommendations {
    margin-left: 8px;
  }
  .minimal-recommendations-courses {
    margin-left: 14px;
  }
  .course-remove-button {
    border: none;
    border-radius: 4px;
    flex: 0.1;
    padding: 0px;
    margin: 1px;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.15s ease;
    text-align: center;
  }
  .course-remove-button:hover {
    background-color: rgba(13, 23, 26, 0.78);
  }
  .alternative-buttons {
    border-radius: 4px;
    width: 99%;
    border: none;
    padding: 2px;
    margin: 1px;
    font-size: 11px;
    color:#cfd8d9;
    background-color: #383b3d;
    transition: background-color 0.2s ease;
  }
  .alternative-buttons:hover {
    background-color:#21242b;
  }
  .alternative-buttons-selected {
    border-radius: 4px;
    width: 99%;
    border: 1px solid #c0d6da;
    padding: 1px;
    margin: 1px;
    color:#e9edf1;
    background-color: #575e63;
    font-size: 11px;
    font-weight:650;
    transition: background-color 0.2s ease;
  }
  .alternative-buttons-selected:hover {
    background-color:#74808a;
    color: #f7faff;
    border: 1px solid #c0d6da;
  }
  .recommendations {
    padding: 4px;
    margin: 2px;
    border-radius: 6px;
    background-color: #393b40;
  }
  .recommendations-list {
    color: #e3e8e4;
  }
  .req-fulfilled {
    color: greenyellow;
    background-color: #414740;
  }
  .req-unfulfilled {
    color: rgb(255, 149, 122);
    background-color: #4f433e;
  }

  .details-panel {
    margin: 2px;
    margin-top: 6px;
    padding: 2px;
    border: 2px solid #43494f;
    border-radius: 8px;
    font-size: 13px;
    color: #b7c0c4;
    background-color: rgba(8, 26, 32, 0.35);
  }
  .details-panel h5 {
    font-size: 16px;
  }
  .details-wildcard-title {
    font-size: 10px;
    color: #769eb1;
  }
  .details-info {
    font-size: 10px;
    color: #769eb1;
  }
</style>
  