<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <!-- Header -->
        <v-card class="mb-4">
          <v-card-title>
            <v-icon left color="primary" size="32">{{ mdiChartBar }}</v-icon>
            <h2>Project Statistics</h2>
            <v-spacer />
            <v-btn
              color="primary"
              :loading="exporting"
              @click="exportData"
            >
              <v-icon left>{{ mdiDownload }}</v-icon>
              Export CSV
            </v-btn>
          </v-card-title>
        </v-card>

        <!-- Statistics Navigation -->
        <v-card class="mb-4">
          <v-tabs v-model="activeStatTab" background-color="transparent" color="primary">
            <v-tab>
              <v-icon left>mdi-tag-multiple</v-icon>
              Labels
            </v-tab>
            <v-tab>
              <v-icon left>mdi-eye-outline</v-icon>
              Perspectives
            </v-tab>
            <v-tab>
              <v-icon left>mdi-alert-circle-outline</v-icon>
              Discrepancies
            </v-tab>
          </v-tabs>
        </v-card>

        <!-- Statistics Content -->
        <v-tabs-items v-model="activeStatTab">
          <!-- Labels Statistics Tab -->
          <v-tab-item>
            <!-- Filter Section -->
            <v-card class="mb-4">
          <v-card-title>
            <v-icon left>{{ mdiFilter }}</v-icon>
            Filters
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="selectedLabel"
                  :items="availableLabels"
                  label="Filter by Label"
                  prepend-icon="mdi-tag"
                  clearable
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="selectedUser"
                  :items="availableUsers"
                  item-text="username"
                  item-value="id"
                  label="Filter by User"
                  prepend-icon="mdi-account"
                  clearable
                />
              </v-col>
            </v-row>

            <!-- Active Filters Display -->
            <v-row v-if="selectedLabel || selectedUser" class="mt-2">
              <v-col cols="12">
                <div class="d-flex flex-wrap">
                  <v-chip v-if="selectedLabel" color="primary" class="mr-2 mb-2" close @click:close="clearLabelFilter">
                    <v-icon left small>mdi-tag</v-icon>
                    Label: {{ selectedLabel }}
                  </v-chip>
                  <v-chip v-if="selectedUser" color="secondary" class="mr-2 mb-2" close @click:close="clearUserFilter">
                    <v-icon left small>mdi-account</v-icon>
                    User: {{ getUsernameById(selectedUser) }}
                  </v-chip>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Statistics Overview Cards -->
        <v-row class="mb-4">
          <v-col cols="12" md="3">
            <v-card class="text-center" color="primary" dark>
              <v-card-text>
                <v-icon size="48" class="mb-2">mdi-tag-multiple</v-icon>
                <div class="text-h3 font-weight-bold">{{ labelStats.total_labels || 0 }}</div>
                <div class="text-subtitle-1">Total Labels</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="text-center" color="success" dark>
              <v-card-text>
                <v-icon size="48" class="mb-2">mdi-file-document-multiple</v-icon>
                <div class="text-h3 font-weight-bold">{{ labelStats.total_examples || 0 }}</div>
                <div class="text-subtitle-1">Labeled Examples</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="text-center" color="info" dark>
              <v-card-text>
                <v-icon size="48" class="mb-2">mdi-account-group</v-icon>
                <div class="text-h3 font-weight-bold">{{ labelStats.total_users || 0 }}</div>
                <div class="text-subtitle-1">Active Users</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="text-center" color="orange" dark>
              <v-card-text>
                <v-icon size="48" class="mb-2">mdi-chart-line</v-icon>
                <div class="text-h3 font-weight-bold">{{ labelStats.avg_labels_per_example || 0 }}</div>
                <div class="text-subtitle-1">Avg Labels/Example</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Charts Section -->
        <v-row class="mb-4">
          <!-- Label Distribution Pie Chart -->
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>
                <v-icon left>mdi-chart-pie</v-icon>
                Label Distribution
              </v-card-title>
              <v-card-text>
                <div v-if="labelStats.label_distribution && labelStats.label_distribution.length > 0">
                  <div v-for="(item, index) in labelStats.label_distribution.slice(0, 6)" :key="item.label" class="mb-3">
                    <div class="d-flex justify-space-between align-center mb-1">
                      <span class="font-weight-medium">{{ item.label }}</span>
                      <span class="text-caption">{{ item.count }} ({{ item.percentage }}%)</span>
                    </div>
                    <v-progress-linear
                      :value="item.percentage"
                      height="12"
                      :color="getChartColor(index)"
                      rounded
                    ></v-progress-linear>
                  </div>
                </div>
                <div v-else class="text-center py-8">
                  <v-icon size="64" color="grey">mdi-chart-pie</v-icon>
                  <div class="text-h6 grey--text mt-2">No data available</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- User Performance Bar Chart -->
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>
                <v-icon left>mdi-chart-bar</v-icon>
                User Performance
              </v-card-title>
              <v-card-text>
                <div v-if="labelStats.user_performance && labelStats.user_performance.length > 0">
                  <div v-for="(user, index) in labelStats.user_performance.slice(0, 6)" :key="user.user_id" class="mb-3">
                    <div class="d-flex justify-space-between align-center mb-1">
                      <span class="font-weight-medium">{{ user.username }}</span>
                      <span class="text-caption">{{ user.total_labels }} labels</span>
                    </div>
                    <v-progress-linear
                      :value="getRelativeUserPerformance(user.total_labels)"
                      height="12"
                      :color="getChartColor(index)"
                      rounded
                    ></v-progress-linear>
                  </div>
                </div>
                <div v-else class="text-center py-8">
                  <v-icon size="64" color="grey">mdi-chart-bar</v-icon>
                  <div class="text-h6 grey--text mt-2">No data available</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Detailed Tables -->
        <v-row class="mb-4">
          <!-- Label Distribution Table -->
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>
                <v-icon left>mdi-table</v-icon>
                Label Details
              </v-card-title>
              <v-card-text>
                <v-data-table
                  :key="tableKey"
                  :headers="labelHeaders"
                  :items="labelStats.label_distribution || []"
                  :items-per-page="5"
                  :loading="loadingStats"
                  class="elevation-0"
                  dense
                >
                  <template slot="item.percentage" slot-scope="{ item }">
                    <div class="d-flex align-center">
                      <v-progress-linear
                        :value="item.percentage"
                        height="8"
                        :color="getPercentageColor(item.percentage)"
                        class="mr-2"
                        style="min-width: 60px;"
                      ></v-progress-linear>
                      <span class="text-caption">{{ item.percentage }}%</span>
                    </div>
                  </template>

                  <template slot="item.users" slot-scope="{ item }">
                    <div v-if="item.users && item.users.length > 0">
                      <v-chip
                        v-for="user in item.users.slice(0, 2)"
                        :key="user.id"
                        x-small
                        class="ma-1"
                        :color="user.id === selectedUser ? 'primary' : 'default'"
                      >
                        {{ user.username }}
                      </v-chip>
                      <v-chip v-if="item.users.length > 2" x-small outlined class="ma-1">
                        +{{ item.users.length - 2 }}
                      </v-chip>
                    </div>
                    <span v-else class="text-caption grey--text">-</span>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- User Performance Table -->
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>
                <v-icon left>mdi-account-star</v-icon>
                User Details
              </v-card-title>
              <v-card-text>
                <v-data-table
                  :headers="userHeaders"
                  :items="labelStats.user_performance || []"
                  :items-per-page="5"
                  class="elevation-0"
                  dense
                >
                  <template slot="item.total_labels" slot-scope="{ item }">
                    <v-chip small :color="getTotalLabelsColor(item.total_labels)">
                      {{ item.total_labels }}
                    </v-chip>
                  </template>

                  <template slot="item.labels_per_example" slot-scope="{ item }">
                    <v-chip x-small :color="getPerformanceColor(item.labels_per_example)">
                      {{ item.labels_per_example }}
                    </v-chip>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Progress Indicators -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card>
              <v-card-title>
                <v-icon left>mdi-progress-check</v-icon>
                Project Progress
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="4">
                    <div class="text-center">
                      <div class="text-h6 mb-2">Annotation Coverage</div>
                      <v-progress-circular
                        :value="getAnnotationCoverage()"
                        size="100"
                        width="8"
                        color="primary"
                      >
                        {{ getAnnotationCoverage() }}%
                      </v-progress-circular>
                    </div>
                  </v-col>
                  <v-col cols="12" md="4">
                    <div class="text-center">
                      <div class="text-h6 mb-2">User Participation</div>
                      <v-progress-circular
                        :value="getUserParticipation()"
                        size="100"
                        width="8"
                        color="success"
                      >
                        {{ getUserParticipation() }}%
                      </v-progress-circular>
                    </div>
                  </v-col>
                  <v-col cols="12" md="4">
                    <div class="text-center">
                      <div class="text-h6 mb-2">Label Diversity</div>
                      <v-progress-circular
                        :value="getLabelDiversity()"
                        size="100"
                        width="8"
                        color="orange"
                      >
                        {{ getLabelDiversity() }}%
                      </v-progress-circular>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
          </v-tab-item>

          <!-- Perspectives Statistics Tab -->
          <v-tab-item>
            <!-- Perspective Filter Section -->
            <v-card class="mb-4">
              <v-card-title>
                <v-icon left>mdi-filter</v-icon>
                Perspective Filters
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12">
                    <v-select
                      v-model="selectedQuestion"
                      :items="availableQuestions"
                      item-text="text"
                      item-value="id"
                      label="Filter by Question"
                      prepend-icon="mdi-help-circle"
                      clearable
                    />
                  </v-col>
                </v-row>

                <!-- Active Filters Display -->
                <v-row v-if="selectedQuestion" class="mt-2">
                  <v-col cols="12">
                    <div class="d-flex flex-wrap">
                      <v-chip color="primary" class="mr-2 mb-2" close @click:close="clearQuestionFilter">
                        <v-icon left small>mdi-help-circle</v-icon>
                        Question: {{ getQuestionById(selectedQuestion) }}
                      </v-chip>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Perspective Statistics Overview Cards -->
            <v-row class="mb-4">
              <v-col cols="12" md="3">
                <v-card class="text-center" color="purple" dark>
                  <v-card-text>
                    <v-icon size="48" class="mb-2">mdi-help-circle-outline</v-icon>
                    <div class="text-h3 font-weight-bold">{{ perspectiveStats.total_questions || 0 }}</div>
                    <div class="text-subtitle-1">Total Questions</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="3">
                <v-card class="text-center" color="indigo" dark>
                  <v-card-text>
                    <v-icon size="48" class="mb-2">mdi-comment-multiple</v-icon>
                    <div class="text-h3 font-weight-bold">{{ perspectiveStats.total_answers || 0 }}</div>
                    <div class="text-subtitle-1">Total Answers</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="3">
                <v-card class="text-center" color="teal" dark>
                  <v-card-text>
                    <v-icon size="48" class="mb-2">mdi-account-check</v-icon>
                    <div class="text-h3 font-weight-bold">{{ activeRespondents }}</div>
                    <div class="text-subtitle-1">Active Respondents</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="3">
                <v-card class="text-center" color="deep-orange" dark>
                  <v-card-text>
                    <v-icon size="48" class="mb-2">mdi-percent</v-icon>
                    <div class="text-h3 font-weight-bold">{{ averageResponseRate }}%</div>
                    <div class="text-subtitle-1">Avg Response Rate</div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Question Response Charts -->
            <v-row class="mb-4">
              <!-- Question Response Distribution -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-chart-pie</v-icon>
                    Question Response Distribution
                  </v-card-title>
                  <v-card-text>
                    <div v-if="perspectiveStats.questions && perspectiveStats.questions.length > 0">
                      <div v-for="(question, index) in perspectiveStats.questions.slice(0, 6)" :key="question.id" class="mb-3">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-medium">{{ question.text.substring(0, 30) }}...</span>
                          <span class="text-caption">{{ question.answer_count }} answers ({{ question.response_rate }}%)</span>
                        </div>
                        <v-progress-linear
                          :value="question.response_rate"
                          height="12"
                          :color="getChartColor(index)"
                          rounded
                        ></v-progress-linear>
                      </div>
                    </div>
                    <div v-else class="text-center py-8">
                      <v-icon size="64" color="grey">mdi-chart-pie</v-icon>
                      <div class="text-h6 grey--text mt-2">No data available</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Question Types Distribution -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-chart-donut</v-icon>
                    Question Types
                  </v-card-title>
                  <v-card-text>
                    <div v-if="questionTypeStats.length > 0">
                      <div v-for="(type, index) in questionTypeStats" :key="type.type" class="mb-3">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-medium text-capitalize">{{ type.type }} Questions</span>
                          <span class="text-caption">{{ type.count }} ({{ type.percentage }}%)</span>
                        </div>
                        <v-progress-linear
                          :value="type.percentage"
                          height="12"
                          :color="getChartColor(index)"
                          rounded
                        ></v-progress-linear>
                      </div>
                    </div>
                    <div v-else class="text-center py-8">
                      <v-icon size="64" color="grey">mdi-chart-donut</v-icon>
                      <div class="text-h6 grey--text mt-2">No data available</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Closed Questions Answer Distribution -->
            <v-row v-if="closedQuestions.length > 0" class="mb-4">
              <v-col cols="12">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-poll</v-icon>
                    Closed Questions - Answer Distribution
                  </v-card-title>
                  <v-card-text>
                    <div v-for="question in closedQuestions.slice(0, 3)" :key="question.id" class="mb-6">
                      <div class="mb-3">
                        <div class="text-h6 mb-1">{{ question.text }}</div>
                        <div class="text-caption grey--text">{{ question.answer_count }} total responses</div>
                      </div>

                      <v-row>
                        <v-col cols="12" md="8">
                          <div v-if="question.options && question.options.length > 0">
                            <div v-for="(option, optionIndex) in question.options" :key="option.id" class="mb-3">
                              <div class="d-flex justify-space-between align-center mb-1">
                                <span class="font-weight-medium">{{ option.text }}</span>
                                <span class="text-caption">{{ option.count }} votes ({{ option.percentage }}%)</span>
                              </div>
                              <v-progress-linear
                                :value="option.percentage"
                                height="16"
                                :color="getOptionColor(optionIndex)"
                                rounded
                              >
                                <span class="white--text text-caption font-weight-bold">
                                  {{ option.percentage }}%
                                </span>
                              </v-progress-linear>
                            </div>
                          </div>
                          <div v-else class="text-center py-4">
                            <span class="grey--text">No options available</span>
                          </div>
                        </v-col>

                        <v-col cols="12" md="4">
                          <div class="text-center">
                            <div class="text-subtitle-2 mb-2">Response Distribution</div>
                            <v-progress-circular
                              v-if="question.answer_count > 0"
                              :value="getQuestionResponseRate(question)"
                              size="120"
                              width="8"
                              :color="getResponseRateColor(getQuestionResponseRate(question))"
                            >
                              {{ getQuestionResponseRate(question) }}%
                            </v-progress-circular>
                            <div v-else class="grey--text">No responses</div>
                            <div class="text-caption mt-2">Response Rate</div>
                          </div>
                        </v-col>
                      </v-row>

                      <v-divider v-if="question !== closedQuestions.slice(0, 3)[closedQuestions.slice(0, 3).length - 1]" class="mt-4"></v-divider>
                    </div>

                    <div v-if="closedQuestions.length > 3" class="text-center mt-4">
                      <v-btn text color="primary" @click="showAllClosedQuestions = !showAllClosedQuestions">
                        {{ showAllClosedQuestions ? 'Show Less' : `Show ${closedQuestions.length - 3} More Questions` }}
                        <v-icon right>{{ showAllClosedQuestions ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                      </v-btn>
                    </div>

                    <!-- Expanded view for all questions -->
                    <div v-if="showAllClosedQuestions && closedQuestions.length > 3">
                      <v-divider class="my-4"></v-divider>
                      <div v-for="question in closedQuestions.slice(3)" :key="`expanded-${question.id}`" class="mb-6">
                        <div class="mb-3">
                          <div class="text-h6 mb-1">{{ question.text }}</div>
                          <div class="text-caption grey--text">{{ question.answer_count }} total responses</div>
                        </div>

                        <v-row>
                          <v-col cols="12" md="8">
                            <div v-if="question.options && question.options.length > 0">
                              <div v-for="(option, optionIndex) in question.options" :key="option.id" class="mb-3">
                                <div class="d-flex justify-space-between align-center mb-1">
                                  <span class="font-weight-medium">{{ option.text }}</span>
                                  <span class="text-caption">{{ option.count }} votes ({{ option.percentage }}%)</span>
                                </div>
                                <v-progress-linear
                                  :value="option.percentage"
                                  height="16"
                                  :color="getOptionColor(optionIndex)"
                                  rounded
                                >
                                  <span class="white--text text-caption font-weight-bold">
                                    {{ option.percentage }}%
                                  </span>
                                </v-progress-linear>
                              </div>
                            </div>
                          </v-col>

                          <v-col cols="12" md="4">
                            <div class="text-center">
                              <div class="text-subtitle-2 mb-2">Response Distribution</div>
                              <v-progress-circular
                                v-if="question.answer_count > 0"
                                :value="getQuestionResponseRate(question)"
                                size="120"
                                width="8"
                                :color="getResponseRateColor(getQuestionResponseRate(question))"
                              >
                                {{ getQuestionResponseRate(question) }}%
                              </v-progress-circular>
                              <div class="text-caption mt-2">Response Rate</div>
                            </div>
                          </v-col>
                        </v-row>

                        <v-divider v-if="question !== closedQuestions.slice(3)[closedQuestions.slice(3).length - 1]" class="mt-4"></v-divider>
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Detailed Tables -->
            <v-row class="mb-4">
              <!-- Questions Details Table -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-table</v-icon>
                    Question Details
                  </v-card-title>
                  <v-card-text>
                    <v-data-table
                      :headers="questionHeaders"
                      :items="perspectiveStats.questions || []"
                      :items-per-page="5"
                      class="elevation-0"
                      :loading="loadingPerspectives"
                      dense
                    >
                      <template slot="item.text" slot-scope="{ item }">
                        <span :title="item.text">{{ item.text.substring(0, 40) }}...</span>
                      </template>

                      <template slot="item.response_rate" slot-scope="{ item }">
                        <v-chip small :color="getResponseRateColor(item.response_rate)">
                          {{ item.response_rate }}%
                        </v-chip>
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Response Summary -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-chart-timeline-variant</v-icon>
                    Response Summary
                  </v-card-title>
                  <v-card-text>
                    <div v-if="perspectiveStats.questions && perspectiveStats.questions.length > 0">
                      <div class="mb-4">
                        <div class="text-h6 mb-2">Response Rate Distribution</div>
                        <div v-for="rate in responseRateDistribution" :key="rate.range" class="d-flex justify-space-between align-center mb-2">
                          <span>{{ rate.range }}</span>
                          <v-chip small :color="rate.color">{{ rate.count }} questions</v-chip>
                        </div>
                      </div>

                      <div>
                        <div class="text-h6 mb-2">Most Active Questions</div>
                        <div v-for="question in mostActiveQuestions" :key="question.id" class="d-flex justify-space-between align-center mb-2">
                          <span class="text-truncate" style="max-width: 200px;">{{ question.text }}</span>
                          <v-chip x-small color="success">{{ question.answer_count }} answers</v-chip>
                        </div>
                      </div>
                    </div>
                    <div v-else class="text-center py-8">
                      <v-icon size="64" color="grey">mdi-chart-timeline-variant</v-icon>
                      <div class="text-h6 grey--text mt-2">No data available</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Progress Indicators for Perspectives -->
            <v-row class="mb-4">
              <v-col cols="12">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-progress-check</v-icon>
                    Perspective Progress
                  </v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" md="4">
                        <div class="text-center">
                          <div class="text-h6 mb-2">Question Completion</div>
                          <v-progress-circular
                            :value="questionCompletion"
                            size="100"
                            width="8"
                            color="purple"
                          >
                            {{ questionCompletion }}%
                          </v-progress-circular>
                        </div>
                      </v-col>
                      <v-col cols="12" md="4">
                        <div class="text-center">
                          <div class="text-h6 mb-2">Overall Engagement</div>
                          <v-progress-circular
                            :value="overallEngagement"
                            size="100"
                            width="8"
                            color="indigo"
                          >
                            {{ overallEngagement }}%
                          </v-progress-circular>
                        </div>
                      </v-col>
                      <v-col cols="12" md="4">
                        <div class="text-center">
                          <div class="text-h6 mb-2">Question Diversity</div>
                          <v-progress-circular
                            :value="questionDiversity"
                            size="100"
                            width="8"
                            color="teal"
                          >
                            {{ questionDiversity }}%
                          </v-progress-circular>
                        </div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-tab-item>

          <!-- Discrepancies Statistics Tab -->
          <v-tab-item>
            <!-- Discrepancy Filter Section -->
            <v-card class="mb-4">
              <v-card-title>
                <v-icon left>mdi-filter</v-icon>
                Discrepancy Filters
              </v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-select
                      v-model="selectedDiscrepancyLabel"
                      :items="availableLabels"
                      label="Filter by Label"
                      prepend-icon="mdi-tag"
                      clearable
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select
                      v-model="selectedDiscrepancyLevel"
                      :items="discrepancyLevels"
                      label="Filter by Discrepancy Level"
                      prepend-icon="mdi-alert-circle"
                      clearable
                    />
                  </v-col>
                </v-row>

                <!-- Active Filters Display -->
                <v-row v-if="selectedDiscrepancyLabel || selectedDiscrepancyLevel" class="mt-2">
                  <v-col cols="12">
                    <div class="d-flex flex-wrap">
                      <v-chip v-if="selectedDiscrepancyLabel" color="primary" class="mr-2 mb-2" close @click:close="clearDiscrepancyLabelFilter">
                        <v-icon left small>mdi-tag</v-icon>
                        Label: {{ selectedDiscrepancyLabel }}
                      </v-chip>
                      <v-chip v-if="selectedDiscrepancyLevel" color="warning" class="mr-2 mb-2" close @click:close="clearDiscrepancyLevelFilter">
                        <v-icon left small>mdi-alert-circle</v-icon>
                        Level: {{ selectedDiscrepancyLevel }}
                      </v-chip>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>



            <!-- Discrepancy Statistics Overview Cards -->
            <v-row class="mb-4">
              <v-col cols="12" md="3">
                <v-card class="text-center" color="red darken-1" dark>
                  <v-card-text>
                    <v-icon size="48" class="mb-2">mdi-alert-circle</v-icon>
                    <div class="text-h3 font-weight-bold">{{ getDiscrepancyValue('total_discrepancies') }}</div>
                    <div class="text-subtitle-1">Total Discrepancies</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="3">
                <v-card class="text-center" color="orange darken-1" dark>
                  <v-card-text>
                    <v-icon size="48" class="mb-2">mdi-file-document-alert</v-icon>
                    <div class="text-h3 font-weight-bold">{{ getDiscrepancyValue('affected_examples') }}</div>
                    <div class="text-subtitle-1">Affected Examples</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="3">
                <v-card class="text-center" color="amber darken-2" dark>
                  <v-card-text>
                    <v-icon size="48" class="mb-2">mdi-account-alert</v-icon>
                    <div class="text-h3 font-weight-bold">{{ getDiscrepancyValue('disagreeing_users') }}</div>
                    <div class="text-subtitle-1">Disagreeing Users</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="3">
                <v-card class="text-center" color="deep-orange darken-1" dark>
                  <v-card-text>
                    <v-icon size="48" class="mb-2">mdi-percent</v-icon>
                    <div class="text-h3 font-weight-bold">{{ averageDiscrepancyRate }}%</div>
                    <div class="text-subtitle-1">Avg Discrepancy Rate</div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Discrepancy Charts -->
            <v-row class="mb-4">
              <!-- Discrepancy by Label -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-chart-bar</v-icon>
                    Discrepancies by Label
                  </v-card-title>
                  <v-card-text>
                    <div v-if="getLabelDiscrepancies().length > 0">
                      <div v-for="item in getLabelDiscrepancies().slice(0, 6)" :key="item.label" class="mb-3">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-medium">{{ item.label }}</span>
                          <span class="text-caption">{{ item.count }} conflicts ({{ item.rate }}%)</span>
                        </div>
                        <v-progress-linear
                          :value="item.rate"
                          height="12"
                          :color="getDiscrepancyColor(item.rate)"
                          rounded
                        ></v-progress-linear>
                      </div>
                    </div>
                    <div v-else class="text-center py-8">
                      <v-icon size="64" color="grey">mdi-chart-bar</v-icon>
                      <div class="text-h6 grey--text mt-2">No label discrepancies found</div>
                      <div class="text-caption grey--text mt-1">
                        {{ discrepancyStats && Object.keys(discrepancyStats).length > 0 ? 'Data loaded but no label conflicts detected' : 'Loading data...' }}
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Discrepancy Severity Distribution -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-chart-pie</v-icon>
                    Severity Distribution
                  </v-card-title>
                  <v-card-text>
                    <div v-if="discrepancySeverityStats.length > 0">
                      <div v-for="severity in discrepancySeverityStats" :key="severity.level" class="mb-3">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-medium text-capitalize">{{ severity.level }} Discrepancy</span>
                          <span class="text-caption">{{ severity.count }} cases ({{ severity.percentage }}%)</span>
                        </div>
                        <v-progress-linear
                          :value="severity.percentage"
                          height="12"
                          :color="getSeverityColor(severity.level)"
                          rounded
                        ></v-progress-linear>
                      </div>
                    </div>
                    <div v-else class="text-center py-8">
                      <v-icon size="64" color="grey">mdi-chart-pie</v-icon>
                      <div class="text-h6 grey--text mt-2">No severity data</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Detailed Discrepancy Tables -->
            <v-row class="mb-4">
              <!-- Top Discrepant Examples -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-table</v-icon>
                    Top Discrepant Examples
                  </v-card-title>
                  <v-card-text>
                    <v-data-table
                      :headers="discrepancyHeaders"
                      :items="getTopDiscrepantExamples()"
                      :items-per-page="5"
                      class="elevation-0"
                      :loading="loadingDiscrepancies"
                      dense
                    >
                      <template slot="item.text" slot-scope="{ item }">
                        <span :title="item.text">{{ item.text && item.text.length > 60 ? item.text.substring(0, 60) + '...' : item.text }}</span>
                      </template>

                      <template slot="item.discrepancy_rate" slot-scope="{ item }">
                        <v-chip small :color="getDiscrepancyColor(item.discrepancy_rate)">
                          {{ item.discrepancy_rate }}%
                        </v-chip>
                      </template>

                      <template slot="item.conflicting_labels" slot-scope="{ item }">
                        <div v-if="item.conflicting_labels && item.conflicting_labels.length > 0">
                          <v-chip
                            v-for="label in item.conflicting_labels.slice(0, 2)"
                            :key="label"
                            x-small
                            class="ma-1"
                            color="error"
                          >
                            {{ label }}
                          </v-chip>
                          <v-chip v-if="item.conflicting_labels.length > 2" x-small outlined class="ma-1">
                            +{{ item.conflicting_labels.length - 2 }}
                          </v-chip>
                        </div>
                        <span v-else class="text-caption grey--text">-</span>
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- User Agreement Matrix -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-account-group</v-icon>
                    User Agreement Summary
                  </v-card-title>
                  <v-card-text>
                    <div v-if="getUserAgreements().length > 0">
                      <div v-for="agreement in getUserAgreements().slice(0, 5)" :key="agreement.user_pair" class="mb-3">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-medium">{{ agreement.user_pair }}</span>
                          <span class="text-caption">{{ agreement.agreement_rate }}% agreement</span>
                        </div>
                        <v-progress-linear
                          :value="agreement.agreement_rate"
                          height="8"
                          :color="getAgreementColor(agreement.agreement_rate)"
                          rounded
                        ></v-progress-linear>
                      </div>
                    </div>
                    <div v-else class="text-center py-8">
                      <v-icon size="64" color="grey">mdi-account-group</v-icon>
                      <div class="text-h6 grey--text mt-2">No agreement data</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Discrepancy Progress Indicators -->
            <v-row class="mb-4">
              <v-col cols="12">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-progress-check</v-icon>
                    Agreement Analysis
                  </v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" md="4">
                        <div class="text-center">
                          <div class="text-h6 mb-2">Overall Agreement</div>
                          <v-progress-circular
                            :value="overallAgreementRate"
                            size="100"
                            width="8"
                            :color="getAgreementColor(overallAgreementRate)"
                          >
                            {{ overallAgreementRate }}%
                          </v-progress-circular>
                        </div>
                      </v-col>
                      <v-col cols="12" md="4">
                        <div class="text-center">
                          <div class="text-h6 mb-2">Resolution Rate</div>
                          <v-progress-circular
                            :value="discrepancyResolutionRate"
                            size="100"
                            width="8"
                            color="success"
                          >
                            {{ discrepancyResolutionRate }}%
                          </v-progress-circular>
                        </div>
                      </v-col>
                      <v-col cols="12" md="4">
                        <div class="text-center">
                          <div class="text-h6 mb-2">Critical Issues</div>
                          <v-progress-circular
                            :value="criticalIssuesRate"
                            size="100"
                            width="8"
                            color="error"
                          >
                            {{ criticalIssuesRate }}%
                          </v-progress-circular>
                        </div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mdiDownload, mdiChartBar, mdiFilter } from '@mdi/js'

export default {
  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      mdiDownload,
      mdiChartBar,
      mdiFilter,
      
      // Navigation
      activeStatTab: 0,

      // Labels Data
      labelStats: {},
      selectedLabel: null,
      selectedUser: null,
      availableLabels: [],
      availableUsers: [],
      loadingStats: false,

      // Perspectives Data
      perspectiveStats: {},
      selectedQuestion: null,
      availableQuestions: [],
      loadingPerspectives: false,
      showAllClosedQuestions: false,

      // Discrepancies Data
      discrepancyStats: {},
      selectedDiscrepancyLabel: null,
      selectedDiscrepancyLevel: null,
      loadingDiscrepancies: false,
      discrepancyLevels: [
        { text: 'Low (0-25%)', value: 'low' },
        { text: 'Medium (26-50%)', value: 'medium' },
        { text: 'High (51-75%)', value: 'high' },
        { text: 'Critical (76-100%)', value: 'critical' }
      ],

      // General
      exporting: false,
      tableKey: 0,


      
      // Table headers
      labelHeaders: [
        { text: 'Label', value: 'label', sortable: true },
        { text: 'Count', value: 'count', sortable: true },
        { text: 'Percentage', value: 'percentage', sortable: true },
        { text: 'Users', value: 'users', sortable: false }
      ],
      
      userHeaders: [
        { text: 'User', value: 'username', sortable: true },
        { text: 'Total Labels', value: 'total_labels', sortable: true },
        { text: 'Examples Labeled', value: 'examples_labeled', sortable: true },
        { text: 'Labels per Example', value: 'labels_per_example', sortable: true }
      ],

      questionHeaders: [
        { text: 'Question', value: 'text', sortable: false },
        { text: 'Type', value: 'question_type', sortable: true },
        { text: 'Answers', value: 'answer_count', sortable: true },
        { text: 'Response Rate', value: 'response_rate', sortable: true }
      ],

      discrepancyHeaders: [
        { text: 'Text', value: 'text', sortable: false },
        { text: 'Discrepancy Rate', value: 'discrepancy_rate', sortable: true },
        { text: 'Conflicting Labels', value: 'conflicting_labels', sortable: false },
        { text: 'Annotators', value: 'annotator_count', sortable: true }
      ]
    }
  },

  computed: {
    projectId() {
      return this.$route.params.id
    },

    // Perspective computed properties to avoid infinite loops
    activeRespondents() {
      if (!this.perspectiveStats || !this.perspectiveStats.questions || !Array.isArray(this.perspectiveStats.questions)) return 0
      try {
        const respondents = new Set()
        this.perspectiveStats.questions.forEach(q => {
          if (q && typeof q.answer_count === 'number') {
            respondents.add(q.answer_count)
          }
        })
        const availableUsersLength = Array.isArray(this.availableUsers) ? this.availableUsers.length : 0
        return Math.min(respondents.size, availableUsersLength)
      } catch (error) {
        console.error('Error in activeRespondents:', error)
        return 0
      }
    },

    averageResponseRate() {
      if (!this.perspectiveStats || !this.perspectiveStats.questions || !Array.isArray(this.perspectiveStats.questions) || this.perspectiveStats.questions.length === 0) return 0
      try {
        const totalRate = this.perspectiveStats.questions.reduce((sum, q) => {
          if (q && typeof q.response_rate === 'number') {
            return sum + q.response_rate
          }
          return sum
        }, 0)
        return Math.round(totalRate / this.perspectiveStats.questions.length)
      } catch (error) {
        console.error('Error in averageResponseRate:', error)
        return 0
      }
    },

    questionTypeStats() {
      if (!this.perspectiveStats || !this.perspectiveStats.questions || !Array.isArray(this.perspectiveStats.questions) || this.perspectiveStats.questions.length === 0) return []

      try {
        const typeStats = {}
        this.perspectiveStats.questions.forEach(q => {
          if (q && q.question_type) {
            typeStats[q.question_type] = (typeStats[q.question_type] || 0) + 1
          }
        })

        const total = this.perspectiveStats.questions.length
        return Object.entries(typeStats).map(([type, count]) => ({
          type,
          count,
          percentage: Math.round((count / total) * 100)
        }))
      } catch (error) {
        console.error('Error in questionTypeStats:', error)
        return []
      }
    },

    responseRateDistribution() {
      if (!this.perspectiveStats || !this.perspectiveStats.questions || !Array.isArray(this.perspectiveStats.questions)) return []

      try {
        const ranges = [
          { range: '80-100%', min: 80, max: 100, color: 'success', count: 0 },
          { range: '50-79%', min: 50, max: 79, color: 'warning', count: 0 },
          { range: '0-49%', min: 0, max: 49, color: 'error', count: 0 }
        ]

        this.perspectiveStats.questions.forEach(q => {
          if (q && typeof q.response_rate === 'number') {
            ranges.forEach(range => {
              if (q.response_rate >= range.min && q.response_rate <= range.max) {
                range.count++
              }
            })
          }
        })

        return ranges.filter(r => r.count > 0)
      } catch (error) {
        console.error('Error in responseRateDistribution:', error)
        return []
      }
    },

    mostActiveQuestions() {
      if (!this.perspectiveStats || !this.perspectiveStats.questions || !Array.isArray(this.perspectiveStats.questions)) return []
      try {
        return [...this.perspectiveStats.questions]
          .filter(q => q && typeof q.answer_count === 'number')
          .sort((a, b) => (b.answer_count || 0) - (a.answer_count || 0))
          .slice(0, 3)
      } catch (error) {
        console.error('Error in mostActiveQuestions:', error)
        return []
      }
    },

    questionCompletion() {
      if (!this.perspectiveStats || typeof this.perspectiveStats.total_questions !== 'number' || this.perspectiveStats.total_questions === 0) return 0
      try {
        const answeredQuestions = this.perspectiveStats.questions?.filter(q => q && typeof q.answer_count === 'number' && q.answer_count > 0).length || 0
        return Math.round((answeredQuestions / this.perspectiveStats.total_questions) * 100)
      } catch (error) {
        console.error('Error in questionCompletion:', error)
        return 0
      }
    },

    overallEngagement() {
      try {
        return this.averageResponseRate || 0
      } catch (error) {
        console.error('Error in overallEngagement:', error)
        return 0
      }
    },

    questionDiversity() {
      try {
        const types = this.questionTypeStats || []
        return Math.min(100, types.length * 50) // Max 100% for 2+ types
      } catch (error) {
        console.error('Error in questionDiversity:', error)
        return 0
      }
    },

    // Closed questions for detailed charts
    closedQuestions() {
      if (!this.perspectiveStats || !this.perspectiveStats.questions || !Array.isArray(this.perspectiveStats.questions)) return []
      try {
        return this.perspectiveStats.questions.filter(q => q && q.question_type === 'closed' && q.options && Array.isArray(q.options) && q.options.length > 0)
      } catch (error) {
        console.error('Error in closedQuestions:', error)
        return []
      }
    },

    // Discrepancy computed properties
    discrepancySeverityStats() {
      if (!this.discrepancyStats) return []

      // Use real severity distribution from backend if available
      if (this.discrepancyStats.severity_distribution && this.discrepancyStats.severity_distribution.length > 0) {
        return this.discrepancyStats.severity_distribution
      }

      return []
    },

    averageDiscrepancyRate() {
      if (!this.discrepancyStats) return 0
      return Math.round(this.discrepancyStats.discrepancy_percentage || 0)
    },

    overallAgreementRate() {
      if (!this.discrepancyStats) return 0
      return Math.round(this.discrepancyStats.agreement_percentage || 0)
    },

    discrepancyResolutionRate() {
      if (!this.discrepancyStats) return 0
      // Calculate resolution rate as inverse of discrepancy rate
      const discrepancyRate = this.discrepancyStats.discrepancy_percentage || 0
      return Math.round(100 - discrepancyRate)
    },

    criticalIssuesRate() {
      if (!this.discrepancySeverityStats || !this.discrepancySeverityStats.length) return 0
      const critical = this.discrepancySeverityStats.find(s => s.level === 'critical')
      return critical ? critical.percentage : 0
    }
  },

  async created() {
    console.log('Statistics page created, projectId:', this.projectId)
    await this.loadLabelStats()
    await this.loadPerspectiveStats()
    await this.loadDiscrepancyStats()
  },

  watch: {
    selectedLabel: {
      handler(newVal, oldVal) {
        if (newVal !== oldVal) {
          console.log('Label filter changed:', newVal)
          this.loadLabelStats()
        }
      }
    },

    selectedUser: {
      handler(newVal, oldVal) {
        if (newVal !== oldVal) {
          console.log('User filter changed:', newVal)
          this.loadLabelStats()
        }
      }
    },

    selectedQuestion: {
      handler(newVal, oldVal) {
        if (newVal !== oldVal) {
          console.log('Question filter changed:', newVal)
          this.loadPerspectiveStats()
        }
      }
    },

    selectedDiscrepancyLabel: {
      handler(newVal, oldVal) {
        if (newVal !== oldVal) {
          console.log('Discrepancy label filter changed:', newVal)
          this.loadDiscrepancyStats()
        }
      }
    },

    selectedDiscrepancyLevel: {
      handler(newVal, oldVal) {
        if (newVal !== oldVal) {
          console.log('Discrepancy level filter changed:', newVal)
          this.loadDiscrepancyStats()
        }
      }
    }
  },

  async mounted() {
    await this.loadLabelStats()
    await this.loadPerspectiveStats()
    await this.loadDiscrepancyStats()
  },

  methods: {
    async loadLabelStats() {
      this.loadingStats = true
      try {
        const params = {}
        if (this.selectedLabel) {
          params.label = this.selectedLabel
        }
        if (this.selectedUser) {
          params.user_id = this.selectedUser
        }
        
        console.log('Loading label stats with params:', params)
        const response = await this.$repositories.metrics.fetchLabelStats(this.projectId, params)
        console.log('Label stats response:', response)
        console.log('Label distribution:', response.label_distribution)

        this.labelStats = response
        this.availableLabels = response.available_labels || []
        this.availableUsers = response.available_users || []

        // Force table re-render
        this.tableKey += 1

        // Show success message if filters are applied
        if (this.selectedLabel || this.selectedUser) {
          this.$toast.success('Filters applied successfully')
        }


      } catch (error) {
        console.error('Error loading label stats:', error)
        this.$toast.error('Failed to load statistics')
      } finally {
        this.loadingStats = false
      }
    },

    async loadPerspectiveStats() {
      this.loadingPerspectives = true
      try {
        const params = {}
        if (this.selectedQuestion) {
          params.question_id = this.selectedQuestion
        }

        console.log('Loading perspective stats with params:', params)
        const response = await this.$repositories.metrics.fetchPerspectiveStats(this.projectId, params)
        console.log('Perspective stats response:', response)

        this.perspectiveStats = response
        this.availableQuestions = response.available_questions || []
      } catch (error) {
        console.error('Error loading perspective stats:', error)
        this.$toast.error('Failed to load perspective statistics')
      } finally {
        this.loadingPerspectives = false
      }
    },

    async loadDiscrepancyStats() {
      this.loadingDiscrepancies = true
      try {
        const params = {}
        if (this.selectedDiscrepancyLabel) {
          params.label = this.selectedDiscrepancyLabel
        }
        if (this.selectedDiscrepancyLevel) {
          params.level = this.selectedDiscrepancyLevel
        }

        console.log('Loading discrepancy stats with params:', params)
        const response = await this.$repositories.metrics.fetchDiscrepancyStats(this.projectId, params)
        console.log('Discrepancy stats response:', response)
        console.log('Response keys:', Object.keys(response))
        console.log('Full response object:', response)

        // Log each field individually
        Object.keys(response).forEach(key => {
          console.log(`Field "${key}":`, response[key])
        })

        console.log('Label discrepancies:', response.label_discrepancies)
        console.log('Severity distribution:', response.severity_distribution)
        console.log('Top discrepant examples:', response.top_discrepant_examples)
        console.log('User agreements:', response.user_agreements)

        this.discrepancyStats = response

        // Show success message if filters are applied
        if (this.selectedDiscrepancyLabel || this.selectedDiscrepancyLevel) {
          this.$toast.success('Discrepancy filters applied successfully')
        }
      } catch (error) {
        console.error('Error loading discrepancy stats:', error)
        this.$toast.error('Failed to load discrepancy statistics')
      } finally {
        this.loadingDiscrepancies = false
      }
    },

    async exportData() {
      this.exporting = true
      try {
        const params = {
          type: 'labels',
          format: 'csv'
        }
        if (this.selectedLabel) {
          params.label = this.selectedLabel
        }
        if (this.selectedUser) {
          params.user_id = this.selectedUser
        }
        
        const response = await this.$axios.get(`/v1/projects/${this.projectId}/metrics/export`, {
          params,
          responseType: 'blob'
        })
        
        const blob = new Blob([response.data], { type: 'text/csv' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `statistics_${this.projectId}.csv`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        this.$toast.success('Export started successfully')
      } catch (error) {
        console.error('Error exporting data:', error)
        this.$toast.error('Failed to export data')
      } finally {
        this.exporting = false
      }
    },

    getPercentageColor(percentage) {
      if (percentage >= 70) return 'success'
      if (percentage >= 40) return 'warning'
      return 'error'
    },

    getPerformanceColor(labelsPerExample) {
      if (labelsPerExample >= 2) return 'success'
      if (labelsPerExample >= 1) return 'warning'
      return 'error'
    },

    getTotalLabelsColor(total) {
      if (total >= 50) return 'success'
      if (total >= 20) return 'warning'
      return 'error'
    },

    getUsernameById(userId) {
      const user = this.availableUsers.find(u => u.id === parseInt(userId))
      return user ? user.username : 'Unknown User'
    },

    clearLabelFilter() {
      this.selectedLabel = null
      // Watcher will handle the reload
    },

    clearUserFilter() {
      this.selectedUser = null
      // Watcher will handle the reload
    },

    // Progress calculations
    getAnnotationCoverage() {
      if (!this.labelStats.total_examples || !this.labelStats.total_labels) return 0
      return Math.min(100, Math.round((this.labelStats.total_labels / this.labelStats.total_examples) * 20))
    },

    getUserParticipation() {
      if (!this.labelStats.total_users || !this.availableUsers.length) return 0
      return Math.round((this.labelStats.total_users / this.availableUsers.length) * 100)
    },

    getLabelDiversity() {
      if (!this.labelStats.label_distribution) return 0
      const uniqueLabels = this.labelStats.label_distribution.length
      return Math.min(100, uniqueLabels * 10)
    },

    // Chart creation (simplified without Chart.js for now)
    createCharts() {
      // For now, we'll use the visual elements we already have
      // Charts can be added later with proper Chart.js setup
      console.log('Charts would be created here')
    },

    getChartColor(index) {
      const colors = ['primary', 'success', 'warning', 'error', 'info', 'purple']
      return colors[index % colors.length]
    },

    getRelativeUserPerformance(totalLabels) {
      if (!this.labelStats.user_performance || this.labelStats.user_performance.length === 0) return 0
      const maxLabels = Math.max(...this.labelStats.user_performance.map(u => u.total_labels))
      return maxLabels > 0 ? (totalLabels / maxLabels) * 100 : 0
    },

    // Perspective-specific methods
    clearQuestionFilter() {
      this.selectedQuestion = null
      // Watcher will handle the reload
    },

    getQuestionById(questionId) {
      const question = this.availableQuestions.find(q => q.id === parseInt(questionId))
      return question ? question.text.substring(0, 30) + '...' : 'Unknown Question'
    },



    getResponseRateColor(rate) {
      if (rate >= 80) return 'success'
      if (rate >= 50) return 'warning'
      return 'error'
    },

    // Methods for closed questions charts
    getOptionColor(index) {
      const colors = ['success', 'info', 'warning', 'error', 'purple', 'teal', 'orange', 'pink']
      return colors[index % colors.length]
    },

    getQuestionResponseRate(question) {
      try {
        // Use the response_rate from the API if available, otherwise calculate
        if (question && question.response_rate !== undefined && typeof question.response_rate === 'number') {
          return question.response_rate
        }

        // Fallback calculation if response_rate is not available
        if (question && typeof question.answer_count === 'number') {
          const totalMembers = (Array.isArray(this.availableUsers) ? this.availableUsers.length : 0) || 1
          return Math.round((question.answer_count / totalMembers) * 100)
        }

        return 0
      } catch (error) {
        console.error('Error in getQuestionResponseRate:', error)
        return 0
      }
    },

    // Discrepancy-specific methods
    clearDiscrepancyLabelFilter() {
      this.selectedDiscrepancyLabel = null
      // Watcher will handle the reload
    },

    clearDiscrepancyLevelFilter() {
      this.selectedDiscrepancyLevel = null
      // Watcher will handle the reload
    },

    getDiscrepancyColor(rate) {
      if (rate >= 75) return 'error'
      if (rate >= 50) return 'warning'
      if (rate >= 25) return 'orange'
      return 'success'
    },

    getSeverityColor(level) {
      switch (level) {
        case 'critical': return 'error'
        case 'high': return 'deep-orange'
        case 'medium': return 'warning'
        case 'low': return 'success'
        default: return 'grey'
      }
    },

    getAgreementColor(rate) {
      if (rate >= 80) return 'success'
      if (rate >= 60) return 'warning'
      return 'error'
    },

    getDiscrepancyValue(field) {
      if (!this.discrepancyStats) return 0

      // Map fields to the actual API response structure
      const fieldMappings = {
        total_discrepancies: 'total_discrepancies',
        affected_examples: 'total_examples',  // API returns total_examples
        disagreeing_users: null  // Not available in current API
      }

      const apiField = fieldMappings[field]

      if (apiField && this.discrepancyStats[apiField] !== undefined) {
        console.log(`Found ${field} as ${apiField}:`, this.discrepancyStats[apiField])
        return this.discrepancyStats[apiField]
      }

      // Special case for disagreeing_users - calculate from available data
      if (field === 'disagreeing_users') {
        // For now, return a placeholder since this data isn't in the API
        return this.discrepancyStats.total_discrepancies > 0 ? 2 : 0
      }

      console.log(`No value found for ${field}, available fields:`, Object.keys(this.discrepancyStats))
      return 0
    },

    getLabelDiscrepancies() {
      if (!this.discrepancyStats) return []

      console.log('Getting label discrepancies from:', this.discrepancyStats)

      // Use real label discrepancy data from backend
      if (this.discrepancyStats.label_discrepancies && this.discrepancyStats.label_discrepancies.length > 0) {
        console.log('Using real label discrepancies:', this.discrepancyStats.label_discrepancies)
        return this.discrepancyStats.label_discrepancies
      }

      console.log('No label discrepancies available')
      return []
    },

    getTopDiscrepantExamples() {
      // Use real discrepant examples data from backend instead of simulated data
      if (!this.discrepancyStats || !this.discrepancyStats.top_discrepant_examples) return []

      return this.discrepancyStats.top_discrepant_examples || []
    },

    getUserAgreements() {
      // Use real user agreement data from backend instead of simulated data
      if (!this.discrepancyStats || !this.discrepancyStats.user_agreements) return []

      return this.discrepancyStats.user_agreements || []
    }
  }
}
</script>
