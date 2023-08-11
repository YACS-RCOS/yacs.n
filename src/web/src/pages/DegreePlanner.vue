<template>
    <b-container fluid>
        <div class="main-loading" v-if="main_loading">
          YACS<h1>&#32; &#32;Degree Planner</h1>
        </div>
        <div @dragover.prevent @drop="schedulerRemove">

        <div ref="searchModalContainer" style="position: absolute; z-index: 9999;">
          <SearchBarModal ref="searchModal" @result="results => modalAdd(activeSemester, results)" @dragover.prevent @courseDrag="schedulerDragFromModal" @setSubjectColors="setSubjectColors" @setSubjectGroupColors="setSubjectGroupColors"></SearchBarModal>
        </div>
        <div class="columns">

          <div class="column-left">
            <div ref="deletionPrompt" class="schedule-deletion-prompt" v-show="scheduleDeletionPrompt">
              Confirm Deletion of {{ schedule_name }}?
              <div class="schedule-deletion-prompt-options">
                <span>
                  <button class="schedule-confirm-delete" @click="commenceDeleteSchedule(schedule_name)">
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
              <button :ref="'renameSchedule'" v-bind:class="{'schedule-selection-button':schedule != schedule_name, 'schedule-selection-button-active':schedule == schedule_name}" v-for="(schedule, index) in schedules" :key="index" @click="setSchedule(schedule)">
                <span class="schedule-button-content">
                  <button class="schedule-selection-delete" @click.stop="promptDeleteSchedule(schedule)">
                    &#10008;
                  </button>
                  <button class="schedule-selection-edit" @click="renameScheduleButton(schedule, index)">
                    &#9998;
                  </button>
                  <span v-show="renaming_schedule != schedule">{{ schedule }}</span>
                  <input :ref="'editScheduleNameInput'" v-show="renaming_schedule == schedule" class="edit-schedule-input" v-model="renaming_schedule_input" @keyup.enter="renameSchedule(schedule, renaming_schedule_input)"/>
                </span>
              </button>
              <input class="new-schedule-input" placeholder="+ new schedule" v-model="new_schedule_input" @keyup.enter="setSchedule(new_schedule_input)"/>
            </div>
            <div class="courses-grid">
              <div v-for="(semester, index) in courses" :key="index" 
                  v-bind:class="{'semester-block':hoverOverSemester!=index, 'semester-block-highlighted':hoverOverSemester==index}" 
                  @dragenter="schedulerDragEnter($event, index)" 
                  @dragleave="schedulerDragLeave()" 
                  @dragover.prevent 
                  @drop="schedulerDrop($event, index)">
                <div class="semester-title-row">
                  <span style="width: 100%;"><h3>Semester {{ index + 1 }}</h3></span>
                  <span style="color:#a1a7a8; margin-top:-8px; margin-right:-8px;" class="schedule-search">
                    <button
                      type="button"
                      :ref="'addButton${index}'"
                      class="search-open"
                      @click="onClick(index)">
                      &#10010;
                    </button>
                  </span>
                </div>

                <div class="schedule-button-container" v-for="(course, course_index) in semester" :key="course_index">
                  <button class="course-buttons" type="button" @click="navigate_to_course_page(course)" draggable="true" @dragstart="schedulerDrag($event, course, index)">
                    <font color="#ffc680">{{ course.substring(0, 10) }}</font> {{ course.substring(10) }}
                  </button>
                  <button class="course-remove-button" type="button" @click="remove(index, course, true, true, true)">
                    <font color="#b05f6e">&#10008;</font>
                  </button>
                </div>

              </div>
            </div>
            
          </div>
          
          <div class="column-center" ref="columnCenter">
            <div v-if="schedule_name != ''">
              <div class="center-top-row">
                <div ref="degreeSelect" style="width: 180px">
                  <button class="toggle-degree-selection-button" @click="toggleDegreeSelectionMenu">Degree Selection</button>
                  <div class="degree-selection-menu" v-if="openedDegreeSelectionMenu">
                    <CatalogTree style="width: 50vw; margin-top: -10px" :nodes="degrees" :label="''" :depth="0" :subjectColors="subjectColors" :subjectGroupColors="subjectGroupColors" :resolutionDict="resolutionDict" :selectedDegree="degree" @setDegree="degree => setDegree(degree)"></CatalogTree>
                  </div>
                </div>
                <div v-if="recommending" style="color: #727d80">
                  ...loading recommendations
                </div>
              </div>

              <div class="requirements-orggrid">
                <div v-bind:class="{'fulfillment-org-block-highlighted':highlightedFulfillment == group.name, 'fulfillment-org-block':highlightedFulfillment != group.name}" v-for="(group, group_index) in requirement_groups" :key="group_index" @click="toggleHighlightFulfillment(group.name)">
                  <div v-if="true">
                    <div class="group-heading">
                      <span class="group-title"> {{ group.name }} </span> 
                      <span v-if="group.minimum_requirements.credits > 0" 
                        v-bind:class="{'group-credit-stats-fulfilled':get_tallied_amount(group.name, 'credits') >= group.minimum_requirements.credits, 'group-credit-stats-unfulfilled':get_tallied_amount(group.name, 'credits') < group.minimum_requirements.credits}">
                        <font color="#707a7a"> credits:&nbsp;&nbsp; </font> {{ get_tallied_amount(group.name, 'credits') }} / {{ group.minimum_requirements.credits }} </span>
                    </div>
                    <div v-for="(requirement, index) in group.requirements" :key="index">
                      
                      <div v-if="Object.keys(requirements[requirement].wildcard_resolutions).length > 0">
                        <div v-for="(alternative_choices, alternative_orig) in requirements[requirement].wildcard_resolutions" :key="alternative_orig">
                          <div v-for="(alternative_choice, alternative_choice_index) in alternative_choices" :key="alternative_choice_index">
                            <button v-bind:class="{'alternative-buttons':chosenAlternative(alternative_orig) != alternative_choice, 'alternative-buttons-selected':chosenAlternative(alternative_orig) == alternative_choice}" type="button" @click.stop="toggleWildcardRequirement(alternative_orig, alternative_choice)">
                              {{ format_alternative(alternative_choice) }}
                            </button>
                          </div>
                        </div>
                      </div>

                      <div v-bind:class="{'minimal-fulfillment':requirements[requirement].actual_count >= requirements[requirement].required_count, 'minimal-unfulfilled-fulfillment':requirements[requirement].actual_count < requirements[requirement].required_count}">
                        <div v-bind:class="{'req-fulfilled':requirements[requirement].actual_count >= requirements[requirement].required_count, 'req-unfulfilled':requirements[requirement].actual_count < requirements[requirement].required_count}">
                          <div class="req-fulfillment-text">
                            <span class="req-fulfillment-name"> {{ format_fulfillment_name(requirements[requirement].name) }} </span> <span class="req-fulfillment-count"> {{ requirements[requirement].actual_count }} / {{ requirements[requirement].required_count }}</span>
                          </div>
                        </div>

                        <div v-for="(course, index) in requirements[requirement].fulfillment_set" :key="index">
                          <button class="course-buttons" type="button" @click="navigate_to_course_page(course)">
                            &#10148; {{ course }}
                          </button>
                        </div>
                      </div>

                      <div class="req-recommendations" v-if="requirement in recommendations && recommendations[requirement].length > 0 && recommendations[requirement][0].fulfillment_set.length > 0">
                        <div class="minimal-recommendations" v-for="(recommendation, recommendation_index) in recommendations[requirement]" :key="recommendation_index">
                          <div v-if="recommendations[requirement].length > 1">
                            <h5>{{ recommendation.specifications }}</h5>
                          </div>
                          <div class="minimal-recommendations-courses" v-for="(course, index) in recommendation.fulfillment_set" :key="index">
                            <button class="minimal-course-buttons" type="button" @click="navigate_to_course_page(course)" draggable="true" @dragstart="schedulerDrag($event, course, -1)">
                              <font color = #a9a9a9> {{ course }} </font>
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
            <div class="schedule-selection">
              <font color="#eb8d75">Schedule:</font> {{ schedule_name }} <br>
              <font color="#e6bc8a">Degree:</font> {{ degree }}
            </div>

            <div v-if="getRequirementGroup(highlightedFulfillment) == null">
              <div style="margin-top: 100px; color: #455050; font-size: 20px; font-weight: 700">
                Click on a Fulfillment Card to View Details!
              </div>
            </div>

            <div v-if="highlightedFulfillment == 'Core'">
              <div style="margin-top: 100px; color: #455050; font-size: 16px; font-weight: 700">
                Your Core Classes, All Info Are Already Displayed On Card
              </div>
            </div>

            <div v-if="getRequirementGroup(highlightedFulfillment) != null">

              <div v-for="(requirement_name, index) in getRequirementGroup(highlightedFulfillment).requirements" :key="index">
                <div v-if="detailsAllTakenCourses[requirement_name] && detailsAllTakenCourses[requirement_name].length != 0" class="details-panel">
                  <p> <font color="#707a7a">Your Taken Courses:</font></p>
                  <h5>{{ requirement_name }}:</h5>
                  <div class="details-wildcard-title" v-for="(fulfillment, fulfillment_index) in detailsAllTakenCourses[requirement_name]" :key="fulfillment_index">
                    {{ fulfillment[0] }}
                    <div class="details-info" v-for="(course, index) in fulfillment[1]" :key="index">
                      <button class="course-buttons" type="button" @click="navigate_to_course_page(course)">
                        &#10148; <font color="#ffc680">{{ course.substring(0, 10) }}</font> {{ course.substring(10) }}
                      </button>
                    </div>
                  </div>
                </div>

                <div v-if="detailsAllPossibleCourses[requirement_name] && detailsAllPossibleCourses[requirement_name].length != 0" class="details-panel">
                  <p> <font color="#707a7a">All Possible Courses:</font></p>
                  <h5>{{ requirement_name }}:</h5>
                  <div class="details-wildcard-title" v-for="(fulfillment, max_fulfillment_index) in detailsAllPossibleCourses[requirement_name]" :key="max_fulfillment_index">
                    {{ fulfillment[0] }}
                    <div class="details-info" v-for="(course, max_index) in fulfillment[1]" :key="max_index">
                      <button class="course-buttons" type="button" @click="navigate_to_course_page(course)">
                        &#10148; <font color="#ffc680">{{ course.substring(0, 10) }}</font> {{ course.substring(10) }}
                      </button>
                    </div>
                  </div>
                </div>
                <br>
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

  export default {
    data() {
        return {
            loading: true,
            main_loading: true,
            userid: 'testuser',
            degree: '',
            degrees: {},
            schedules: [],
            new_schedule_input: '',
            renaming_schedule_input: '',
            renaming_schedule: '',
            schedule_button_index: -1,
            schedule_name: '',
            defaultScheduleName: 'my schedule',
            scheduleDeletionPrompt: false,
            courses: [],
            recommending: false,
            requirement_groups: [],
            tally: {},
            requirements: {},
            recommendations: {},

            detailsAllTakenCourses: {},
            detailsAllPossibleCourses: {},
            SEM_MAX: 12,
            course_inputs: [],
            recommend_pause_token: 1,
            dragElement: null,
            dragFromSemester: 0,
            hoverOverSemester: -1,
            lastDropInsideZone: false,
            hoverCounter: 0, // to fix the problem where hovering over child elements creates a dragenter + dragleave event
            activeSemester: -1,
            showSearchModal: false,
            highlightedFulfillment: null,
            resolutionDict: {},
            openedDegreeSelectionMenu: false,

            subjectColors: {},
            subjectGroupColors: {},

            wildcardRequirements: {},
        };
    },
    methods: {

        getRequirementGroup(name, first_only=true) {
          if (this.requirement_groups.length == 0) {
            return null
          }
          let filteredGroup = this.requirement_groups.filter(group => group.name == name);

          if (filteredGroup.length > 0) {
            //console.log("returning " + JSON.stringify(filteredGroup))
            if (first_only) {
              return filteredGroup[0]
            }
            return filteredGroup
          }
          return null
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
          this.get_fulfillment(this.wildcardRequirements);
        },
        chosenAlternative(alternative_orig) {
          if (alternative_orig in this.wildcardRequirements) {
            return this.wildcardRequirements[alternative_orig]
          }
          return alternative_orig
        },
        
        schedulerDragFromModal(course) {
          this.schedulerDrag(null, course, -1);
        },

        onClick(semester) {
          if (this.showSearchModal && this.activeSemester == semester) {
            this.toggleSearchModal(false);
            return
          }
          this.activeSemester = semester;
          this.toggleSearchModal(true);
          this.$refs.searchModal.onClick(semester);
          document.removeEventListener('click', this.handleClickOutside);
          document.addEventListener('click', this.handleClickOutside);
          this.$nextTick(() => {
            const targetDiv = this.$refs.columnCenter;
            const targetDivRect = targetDiv.getBoundingClientRect();
            const searchModal = this.$refs.searchModalContainer;
            searchModal.style.left = targetDivRect.left + 'px';
            searchModal.style.top = targetDivRect.top - searchModal.offsetHeight + 'px';
            //console.log("search modal: " + searchModal.style.left + ", " + searchModal.style.top);
          });
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
          if (this.schedule_button_index >= 0 && this.$refs['renameSchedule'][this.schedule_button_index] && !this.$refs['renameSchedule'][this.schedule_button_index].contains(event.target)) {
            this.renaming_schedule_input = '';
            this.renaming_schedule = '';
            console.log('clicked outside!!!')
          }
          if (this.$refs.deletionPrompt && !this.$refs.deletionPrompt.contains(event.target)) {
            this.cancelDeleteSchedule();
          }
          if (this.$refs.degreeSelect && !this.$refs.degreeSelect.contains(event.target)) {
            this.openedDegreeSelectionMenu = false;
          }
        },
        toggleSearchModal(on) {
          this.showSearchModal = on;
          this.$refs.searchModal.showDropdown = on;
          if (!on) {
            this.$refs.searchModal.onClose();
          }
        },
        modalAdd(semester, course) {
          if (this.courses[semester].includes(course)) {
            this.remove(semester, course, true, true, true);
          }
          else {
            this.add(semester, course, true, true, true);
          }

          if (this.$refs.searchModal.closeModalOnSelection) {
            this.toggleSearchModal(false);
          }
        },
        // HELPER FUNCTIONS
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
                if (this.dragFromSemester != -1) {
                    this.remove(this.dragFromSemester, this.dragElement, false, false);
                    this.add(dragToSemester, this.dragElement, false, false);
                }
                else {
                    this.add(dragToSemester, this.dragElement, true, true, true);
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
          console.log("remove function scrubbing");
          event.preventDefault();
          if (this.dragElement != null) {
              if (this.dragFromSemester != -1) {
                  this.remove(this.dragFromSemester, this.dragElement, true, true, true);
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
        navigate_to_course_page(course) {
            let page = course.substring(0, 4).toUpperCase() + "/" + course.substring(0, 4).toUpperCase() + "-" + course.substring(5, 9);
            this.$router.push("/explore/" + page);
        },
        format_alternative(str) {
            if (str.includes('*')) {
                str = str.split('*')[0] + " automatically select";
            }
            str = str.replace('.', ': ');
            return str;
        },
        format_fulfillment_name(str) {
            if (str.includes('-')) {
                str = str.substring(str.indexOf('-') + 1);
            }
            return str;
        },
        get_tallied_amount(group_name, tally) {
            if (this.tally[group_name][tally] == null) {
                return 0;
            }
            return this.tally[group_name][tally];
        },

        delayedFinishedLoading() {
          // Calling the method with a delay
          setTimeout(this.finishedLoading, 1200);
        },
        finishedLoading() {
          this.main_loading = false;
        },
        // API CALLING
        async fetch_data(fulfill = true, recommend = true) {
            this.loading = true;
            await this.getSchedules();
            if (this.schedule_name == '') {
              let schedule_name = this.defaultScheduleName;
              let userid = this.userid;
              await fetch('/api/dp/schedule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({userid, schedule_name}),
              });
              await this.getSchedules();
            }
            // fetch fulfillment and recommendations
            this.print();
            if (fulfill) {
              await this.get_fulfillment().then(this.delayedFinishedLoading());
            }
            if (recommend) {
              await this.get_recommendation();
            }
        },
        async newuser() {
            let userid = this.userid;
            const response = await fetch('/api/dp/newuser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userid),
            });
            let data = await response.json();
            this.degrees = data.degrees;
        },
        async get_fulfillment(attributes_replacement = null) {
            let userid = this.userid;
            if (attributes_replacement == null) {
                attributes_replacement = {};
            }
            const response1 = await fetch('/api/dp/fulfillment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userid, attributes_replacement }),
            });
            let fulfillment_tuple = await response1.json();
            this.requirements = fulfillment_tuple[0];
            this.requirement_groups = fulfillment_tuple[1];
            this.tally = fulfillment_tuple[2];
            this.detailsAllTakenCourses = fulfillment_tuple[3];
            this.detailsAllPossibleCourses = fulfillment_tuple[4];
        },
        async get_recommendation() {
            let userid = this.userid;
            this.recommending = true;
            await fetch('/api/dp/recommend/' + userid, {
                method: 'POST'
            });
            const response2 = await fetch('/api/dp/recommend/' + userid);
            this.recommendations = await response2.json().then(this.loading = false);
            this.recommending = false;
        },
        async add_from_input(semester) {
            this.add(semester, this.course_inputs[semester]);
            this.course_inputs[semester] = "";
        },
        async add(semester, course, fulfill = true, recommend = true, autoselect = false) {
            let userid = this.userid;

            if (autoselect) {
              if (course in this.$refs.searchModal.courseSelected) {
                console.log("autoskipping fulfillment & recommend");
                fulfill = false;
                recommend = false;
              }
            }

            await fetch('/api/dp/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userid, semester, course }),
            });
          await this.fetch_data(fulfill, recommend);
        },
        async remove(semester, course, fulfill = true, recommend = true, autoselect = false) {
            let userid = this.userid;

            if (autoselect) {
              if (course in this.$refs.searchModal.courseSelected && this.$refs.searchModal.courseSelected[course].length > 1) {
                console.log("autoskipping fulfillment & recommend");
                fulfill = false;
                recommend = false;
              }
            }
            await fetch('/api/dp/remove', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userid, semester, course }),
            });
            await this.fetch_data(fulfill, recommend);
        },
        async print() {
            let userid = this.userid;
            const response = await fetch('/api/dp/print', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userid),
            });
            let userData = await response.json();
            this.courses = userData['courses'];
            this.degree = userData['degree'];
            if (this.degree.length == 0) {
              this.openedDegreeSelectionMenu = true;
            }
            this.$refs.searchModal.importCourses(this.courses);
        },
        async setDegree(degree_name) {
          let userid = this.userid;
          if (degree_name.toLowerCase() == this.degree.toLowerCase()) {
            return
          }
          this.degree = degree_name;
          if (this.openedDegreeSelectionMenu) {
            this.openedDegreeSelectionMenu = false;
          }
          console.log('setting degree to ' + degree_name)
          await fetch('/api/dp/setdegree', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userid, degree_name}),
          });
          await this.fetch_data();
        },
        promptDeleteSchedule(schedule) {
          document.removeEventListener('click', this.handleClickOutside);
          document.addEventListener('click', this.handleClickOutside);
          this.schedule_name = schedule;
          this.scheduleDeletionPrompt = true;
        },

        cancelDeleteSchedule() {
          this.scheduleDeletionPrompt = false;
        },

        commenceDeleteSchedule(schedule) {
          this.scheduleDeletionPrompt = false;
          this.deleteSchedule(schedule);
        },

        async renameScheduleButton(schedule, index) {
          document.removeEventListener('click', this.handleClickOutside);
          document.addEventListener('click', this.handleClickOutside);
          this.renaming_schedule = schedule;
          this.renaming_schedule_input = schedule;
          this.schedule_button_index = index;
          this.$nextTick(() => {
            if (this.$refs['editScheduleNameInput'][this.schedule_button_index]) {
              this.$refs['editScheduleNameInput'][this.schedule_button_index].focus();
            }
          });
        },

        async getSchedules() {
          let userid = this.userid;
          const response = await fetch('/api/dp/schedules/' + userid);
          let schedule_data = await response.json();
          this.schedules = schedule_data[0];
          this.schedule_name = schedule_data[1];
        },

        async deleteSchedule(schedule_name) {
          let userid = this.userid;
          this.renaming_schedule = '';
          this.renaming_schedule_input = '';
          this.new_schedule_input = '';
          await fetch('/api/dp/scheduledelete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userid, schedule_name}),
          });
          await this.getSchedules();
          if (schedule_name == this.schedule_name && this.schedules.length > 0) {
            await this.setSchedule(this.schedules[0]);
          }
          if (this.schedules.length == 0) {
            this.schedule_name = '';
            this.courses = [];
          }
        },

        async setSchedule(schedule_name) {
          let userid = this.userid;
          if (schedule_name == this.schedule_name) {
            return
          }
          this.renaming_schedule = '';
          this.renaming_schedule_input = '';
          this.new_schedule_input = '';
          await fetch('/api/dp/schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userid, schedule_name}),
          });
          this.new_schedule_input = '';
          await this.fetch_data();
        },

        async renameSchedule(old_schedule_name, new_schedule_name) {
          let userid = this.userid;
          this.renaming_schedule = '';
          this.renaming_schedule_input = '';
          this.new_schedule_input = '';
          await fetch('/api/dp/schedulerename', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userid, old_schedule_name, new_schedule_name}),
          });
          this.schedule_name = new_schedule_name;
          await this.getSchedules();
        },

        setResolutionDict() {
          this.resolutionDict = {
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
        this.main_loading = true;
        await this.newuser();
        await this.fetch_data();
        this.course_inputs = new Array(this.SEM_MAX).fill('');
        this.setResolutionDict();
        document.addEventListener('click', this.handleClickOutside);
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
    flex: 7;
    overflow-y: auto;
    padding: 8px;
    border: 1px solid #171d1a;
    background-color:#272a2c;
    font-size: 0.8em;
    min-width: 400px;
    max-width: 600px;
  }
  .column-left::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .column-center {
    flex: 12;
    overflow-y: auto;
    padding: 6px;
    background-color:rgb(36, 37, 40);
    justify-content: center;
    border: 1px solid #171d1a;
  }
  .column-center::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .column-right {
    flex: 4;
    overflow-y: auto;
    padding: 8px;
    border: 1px solid #171d1a;
    background-color:#272a2c;
    font-size: 0.8em;
    min-width: 280px;
    max-width: 400px;
  }
  .column-right::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .requirements-orggrid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    justify-content: center;
    gap: 2px;
  }
  .courses-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0px;
    position: relative;
  }
  .semester-block {
    border: 2px solid #43494f;
    border-radius: 8px;
    padding: 8px;
    margin: 4px;
    font-size: 0.75em;
    background-color: rgba(8, 26, 32, 0.35);
  }
  .semester-block h3 {
    font-size: 1.5em;
    color: #98bdd4;
  }
  .semester-block-highlighted {
    border: 2px solid #43494f;
    border-radius: 8px;
    padding: 8px;
    margin: 4px;
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
    padding: 8px;
    margin: 2px;
    width: 345px;
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
    padding: 8px;
    margin: 2px;
    width: 345px;
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
    padding: 6px;
    border: 2px solid #43494f;
    border-radius: 8px;
    font-size: 14px;
    color: #b7c0c4;
    background-color: rgba(8, 26, 32, 0.35);
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
  