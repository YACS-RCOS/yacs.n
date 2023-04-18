<template>
    <b-container fluid class="py-3 h-100 main-body">
      <b-row class="h-100">
        <b-col md="4" class="d-flex flex-column">
          <b-card no-body class="h-100">
            <b-tabs card class="h-100 d-flex flex-column flex-grow-1">
              <b-tab
                title="Select Term"
                active
                class="flex-grow-1 w-100"
                data-cy="course-search-tab"
              >
                Select term
              </b-tab>
              <b-tab class="flex-grow-1" data-cy="selected-courses-tab">
                Form
              </b-tab>
            </b-tabs>
          </b-card>
        </b-col>
        <div class="col-md-8">
            Schedule
          <!-- <b-form-select
            v-if="
              !loading &&
              scheduler.scheduleSubsemesters &&
              scheduler.scheduleSubsemesters.length > 1
            "
            v-model="selectedScheduleSubsemester"
            :options="scheduler.scheduleSubsemesters"
            text-field="display_string"
            value-field="display_string"
          ></b-form-select>
          <div id="allScheduleData">
            <div>
              <b-row>
                <b-col class="m-2">
                  <b-button
                    @click="
                      changeSchedule(-1);
                      updateIndexCookie();
                    "
                    size="sm"
                  >
                    Prev
                  </b-button>
                </b-col>
                <b-col cols="8" class="m-2 text-center">
                  <span v-if="scheduleDisplayMessage === 2">
                    Add some sections to generate schedules!
                  </span>
                  <span v-else-if="scheduleDisplayMessage === 3">
                    Can't display because of course conflict!
                  </span>
                  <span v-else>
                    Displaying schedule {{ this.index + 1 }} out of
                    {{ this.possibilities.length }}
                  </span>
                </b-col>
                <b-col class="m-2 text-right">
                  <b-button
                    @click="
                      changeSchedule(1);
                      updateIndexCookie();
                    "
                    size="sm"
                  >
                    Next
                  </b-button>
                </b-col>
              </b-row>
              <Schedule v-if="loading" />
              <Schedule v-else :possibility="possibilities[index]"></Schedule>
  
              <b-row>
                <b-col class="m-2">
                  <h5>CRNs: {{ selectedCrns }}</h5>
                  <h5>Credits: {{ totalCredits }}</h5>
                </b-col>
  
                <b-col md="3" justify="end">
                  <b-row>
                    <b-form-checkbox
                      class="mt-2"
                      size="sm"
                      :checked="$store.state.colorBlindAssist"
                      @change="toggleColors()"
                      switch
                    >
                      Color Blind Assistance
                    </b-form-checkbox>
                  </b-row>
                  <b-row>
                    <b-dropdown text="Export Data" class="mt-2">
                      <b-dropdown-item @click="exportScheduleToIcs">
                        <font-awesome-icon :icon="exportIcon" />
                        Export To ICS
                      </b-dropdown-item>
                      <b-dropdown-item @click="exportScheduleToImage">
                        <font-awesome-icon :icon="exportIcon" />
                        Export To Image
                      </b-dropdown-item>
                    </b-dropdown>
                  </b-row>
                </b-col>
              </b-row>
            </div>
          </div> -->
        </div>
      </b-row>
    </b-container>
  </template>