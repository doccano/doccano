<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <!-- Header -->
        <v-card class="mb-4">
          <v-card-title>
            <v-icon left color="primary" size="32">{{ mdiChartBar }}</v-icon>
            <h2>Statistics</h2>
            <v-spacer />
            <v-btn
              color="primary"
              :loading="exporting"
              @click.prevent="exportStatistics"
            >
              <v-icon left>{{ mdiDownload }}</v-icon>
              Export PDF
            </v-btn>
          </v-card-title>
        </v-card>

        <!-- Filters Section -->
        <v-card class="mb-4">
          <v-card-title>
            <v-icon left>{{ mdiFilter }}</v-icon>
            Filters
          </v-card-title>
          <v-card-text>
            <v-row>
              <!-- Dataset Text Filter -->
              <v-col cols="12" md="4">
                <v-select
                  v-model="filters.textFilter"
                  :items="availableTexts"
                  item-text="preview"
                  item-value="value"
                  label="Filter by Dataset Text"
                  prepend-icon="mdi-text"
                  clearable
                  placeholder="Select text from dataset..."
                  @change="applyFilters"
                />
              </v-col>

              <!-- Discrepancy Filter -->
              <v-col cols="12" md="4">
                <v-select
                  v-model="filters.discrepancyFilter"
                  :items="discrepancyOptions"
                  label="Discrepancy Filter"
                  prepend-icon="mdi-alert-circle"
                  clearable
                  @change="applyFilters"
                />
              </v-col>

              <!-- User Filter -->
              <v-col cols="12" md="4">
                <v-select
                  v-model="filters.userFilter"
                  :items="availableUsers"
                  item-text="username"
                  item-value="id"
                  label="Filter by User"
                  prepend-icon="mdi-account"
                  clearable
                  @change="applyFilters"
                />
              </v-col>
            </v-row>

            <v-row>
              <!-- Label Filter -->
              <v-col cols="12" md="4">
                <v-select
                  v-model="filters.labelFilter"
                  :items="availableLabels"
                  label="Filter by Label"
                  prepend-icon="mdi-tag"
                  clearable
                  @change="applyFilters"
                />
              </v-col>

              <!-- Perspective Filter -->
              <v-col cols="12" md="4">
                <v-select
                  v-model="filters.perspectiveFilter"
                  :items="availablePerspectives"
                  item-text="text"
                  item-value="id"
                  label="Filter by Perspective"
                  prepend-icon="mdi-eye"
                  clearable
                  @change="applyFilters"
                />
              </v-col>

              <!-- Active Filters Display -->
              <v-col cols="12" md="4">
                <div v-if="hasActiveFilters" class="d-flex flex-wrap">
                  <v-chip
                    v-if="filters.textFilter"
                    color="primary"
                    class="mr-2 mb-2"
                    close
                    @click:close="clearFilter('textFilter')"
                  >
                    <v-icon left small>mdi-text</v-icon>
                    Text: {{ filters.textFilter.substring(0, 20) }}...
                  </v-chip>
                  <v-chip
                    v-if="filters.discrepancyFilter"
                    color="warning"
                    class="mr-2 mb-2"
                    close
                    @click:close="clearFilter('discrepancyFilter')"
                  >
                    <v-icon left small>mdi-alert-circle</v-icon>
                    {{ filters.discrepancyFilter }}
                  </v-chip>
                  <v-chip
                    v-if="filters.userFilter"
                    color="secondary"
                    class="mr-2 mb-2"
                    close
                    @click:close="clearFilter('userFilter')"
                  >
                    <v-icon left small>mdi-account</v-icon>
                    {{ getUsernameById(filters.userFilter) }}
                  </v-chip>
                  <v-chip
                    v-if="filters.labelFilter"
                    color="success"
                    class="mr-2 mb-2"
                    close
                    @click:close="clearFilter('labelFilter')"
                  >
                    <v-icon left small>mdi-tag</v-icon>
                    {{ filters.labelFilter }}
                  </v-chip>
                  <v-chip
                    v-if="filters.perspectiveFilter"
                    color="info"
                    class="mr-2 mb-2"
                    close
                    @click:close="clearFilter('perspectiveFilter')"
                  >
                    <v-icon left small>mdi-eye</v-icon>
                    {{ getPerspectiveNameById(filters.perspectiveFilter) }}
                  </v-chip>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Statistics Overview Cards (only when filters are active) -->
        <v-row v-if="hasActiveFilters" class="mb-4">
          <v-col cols="12" md="3">
            <v-card class="text-center" color="primary" dark>
              <v-card-text>
                <v-icon size="48" class="mb-2">mdi-file-document-multiple</v-icon>
                <div class="text-h3 font-weight-bold">{{ stats.totalExamples || 0 }}</div>
                <div class="text-subtitle-1">Total Examples</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="text-center" color="success" dark>
              <v-card-text>
                <v-icon size="48" class="mb-2">mdi-tag-multiple</v-icon>
                <div class="text-h3 font-weight-bold">{{ stats.totalLabels || 0 }}</div>
                <div class="text-subtitle-1">Total Labels</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="text-center" color="info" dark>
              <v-card-text>
                <v-icon size="48" class="mb-2">mdi-account-group</v-icon>
                <div class="text-h3 font-weight-bold">{{ stats.totalUsers || 0 }}</div>
                <div class="text-subtitle-1">Active Users</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="text-center" color="warning" dark>
              <v-card-text>
                <v-icon size="48" class="mb-2">mdi-alert-circle</v-icon>
                <div class="text-h3 font-weight-bold">{{ stats.discrepancyRate || 0 }}%</div>
                <div class="text-subtitle-1">Discrepancy Rate</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Dataset Details Table (always shown but with different titles) -->
        <div class="mb-6">
          <v-card>
            <v-card-title>
              <v-icon left color="primary">mdi-table</v-icon>
              <h3>{{ hasActiveFilters ? 'Filtered Dataset Details' : 'Dataset Details' }}</h3>
              <v-spacer />
              <v-chip color="info" text-color="white">
                {{ datasetDetails.length }} examples
              </v-chip>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="datasetDetailsHeaders"
                :items="datasetDetails"
                :items-per-page="10"
                :loading="loading"
                class="elevation-0"
                dense
              >
                <template #[`item.text`]="{ item }">
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <span 
                        style="cursor: pointer; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: block;"
                        v-bind="attrs" 
                        v-on="on"
                      >
                        {{ item.text }}
                      </span>
                    </template>
                    <span>{{ item.full_text }}</span>
                  </v-tooltip>
                </template>
                
                <template #[`item.discrepancy`]="{ item }">
                  <v-chip 
                    small 
                    :color="item.discrepancy === 'Yes' ? 'error' : 'success'"
                    :text-color="'white'"
                  >
                    {{ item.discrepancy }}
                  </v-chip>
                </template>
                
                <template #[`item.participation`]="{ item }">
                  <div class="d-flex align-center">
                    <span class="text-caption mr-2" style="min-width: 40px;">
                      {{ item.participationNumbers }}
                    </span>
                    <v-progress-linear
                      :value="item.participationPercentage"
                      height="8"
                      :color="getParticipationColor(item.participationPercentage)"
                      rounded
                      class="flex-grow-1"
                    />
                    <span class="text-caption ml-2">
                      {{ Math.round(item.participationPercentage) }}%
                    </span>
                  </div>
                  <div class="text-caption text--secondary mt-1">
                    {{ item.participationUsers }}
                  </div>
                </template>
                
                <template #[`item.annotations`]="{ item }">
                  <div v-if="item.annotationDetails && item.annotationDetails.length > 0">
                    <v-chip
                      v-for="(annotation, index) in item.annotationDetails.slice(0, 3)"
                      :key="index"
                      small
                      :color="getLabelColor(annotation.label)"
                      text-color="white"
                      class="mr-1 mb-1"
                      style="cursor: pointer;"
                      @click="showAnnotationDetails(annotation, item)"
                    >
                      {{ annotation.label }}
                      <v-icon v-if="annotation.users && annotation.users.length > 1" small right>mdi-account-multiple</v-icon>
                      <v-icon v-else small right>mdi-account</v-icon>
                      <v-chip 
                        v-if="annotation.users && annotation.users.length > 1"
                        x-small 
                        color="white" 
                        text-color="primary"
                        class="ml-1"
                        style="font-size: 10px;"
                      >
                        {{ annotation.users.length }}
                      </v-chip>
                    </v-chip>
                    <v-chip
                      v-if="item.annotationDetails.length > 3"
                      small
                      color="grey"
                      text-color="white"
                      class="mr-1 mb-1"
                      style="cursor: pointer;"
                      @click="showAllAnnotations(item)"
                    >
                      +{{ item.annotationDetails.length - 3 }}
                    </v-chip>
                  </div>
                  <div v-else class="text-caption text--secondary">
                    No annotations
                  </div>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </div>

        <!-- User Details Table (always shown but with different titles) -->
        <div class="mb-6">
          <v-card>
            <v-card-title>
              <v-icon left color="secondary">mdi-account-group</v-icon>
              <h3>{{ hasActiveFilters ? 'Filtered User Details' : 'User Details' }}</h3>
              <v-spacer />
              <v-chip color="secondary" text-color="white">
                {{ userDetails.length }} users
              </v-chip>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="userDetailsHeaders"
                :items="userDetails"
                :items-per-page="10"
                :loading="loading"
                class="elevation-0"
                dense
              >
                <template #[`item.username`]="{ item }">
                  <div class="d-flex align-center">
                    <v-avatar size="24" class="mr-2" color="primary">
                      <span class="white--text text-caption">{{ item.username.charAt(0).toUpperCase() }}</span>
                    </v-avatar>
                    <span class="font-weight-medium">{{ item.username }}</span>
                  </div>
                </template>
                
                <template #[`item.textsLabeled`]="{ item }">
                  <div class="d-flex align-center">
                    <span class="text-body-2 mr-2">
                      {{ item.textsLabeled }} / {{ item.textsAssigned }}
                    </span>
                    <v-progress-linear
                      :value="item.textLabelingPercentage"
                      height="6"
                      :color="getTextLabelingColor(item.textLabelingPercentage)"
                      rounded
                      class="flex-grow-1"
                      style="max-width: 100px;"
                    />
                  </div>
                </template>
                
                <template #[`item.totalLabels`]="{ item }">
                  <v-chip 
                    small 
                    :color="getTotalLabelsColor(item.totalLabels)"
                    text-color="white"
                  >
                    {{ item.totalLabels }}
                  </v-chip>
                </template>
                
                <template #[`item.participation`]="{ item }">
                  <div class="d-flex align-center">
                    <v-progress-circular
                      :value="item.participation"
                      :color="getParticipationColor(item.participation)"
                      size="40"
                      width="4"
                      class="mr-2"
                    >
                      <span class="text-caption">{{ Math.round(item.participation) }}%</span>
                    </v-progress-circular>
                    <span class="text-caption text--secondary">
                      {{ item.participation >= 80 ? 'High' : item.participation >= 50 ? 'Medium' : 'Low' }}
                    </span>
                  </div>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </div>

        <!-- Perspective Details Table (always shown but with different titles) -->
        <div class="mb-6">
          <v-card>
            <v-card-title>
              <v-icon left color="info">mdi-eye-outline</v-icon>
              <h3>{{ hasActiveFilters ? 'Filtered Perspective Details' : 'Perspective Details' }}</h3>
              <v-spacer />
              <v-chip color="info" text-color="white">
                {{ perspectiveDetails.length }} questions
              </v-chip>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="perspectiveDetailsHeaders"
                :items="perspectiveDetails"
                :items-per-page="10"
                :loading="loading"
                class="elevation-0"
                dense
              >
                <template #[`item.question`]="{ item }">
                  <div class="d-flex align-center">
                    <v-icon small class="mr-2" :color="item.type === 'open' ? 'primary' : 'secondary'">
                      {{ item.type === 'open' ? 'mdi-text-box' : 'mdi-format-list-bulleted' }}
                    </v-icon>
                    <span class="font-weight-medium" :title="item.question">
                      {{ item.question.length > 50 ? item.question.substring(0, 50) + '...' : item.question }}
                    </span>
                  </div>
                </template>
                
                <template #[`item.type`]="{ item }">
                  <v-chip 
                    small 
                    :color="item.type === 'open' ? 'primary' : 'secondary'"
                    text-color="white"
                  >
                    {{ item.type === 'open' ? 'Open Text' : 'Multiple Choice' }}
                  </v-chip>
                </template>
                
                <template #[`item.answers`]="{ item }">
                  <div class="d-flex align-center">
                    <v-chip 
                      small 
                      :color="getAnswersColor(item.answers)"
                      text-color="white"
                      class="mr-2"
                    >
                      {{ item.answers }}
                    </v-chip>
                    <v-progress-linear
                      :value="item.responseRate"
                      height="6"
                      :color="getResponseRateColor(item.responseRate)"
                      rounded
                      class="flex-grow-1"
                      style="max-width: 120px;"
                    />
                    <span class="text-caption ml-2">{{ Math.round(item.responseRate) }}%</span>
                  </div>
                </template>
                
                <template #[`item.actions`]="{ item }">
                  <v-btn
                    small
                    color="info"
                    outlined
                    @click="showPerspectiveAnswers(item)"
                  >
                    <v-icon left small>mdi-eye</v-icon>
                    View Answers
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </div>

        <!-- Annotation Details Dialog -->
        <v-dialog v-model="annotationDialog" max-width="600">
          <v-card>
            <v-card-title class="headline">
              <v-icon left color="primary">mdi-tag</v-icon>
              Annotation Details
            </v-card-title>
            <v-card-text>
              <div v-if="selectedAnnotation">
                <v-chip
                  large
                  :color="getLabelColor(selectedAnnotation.label)"
                  text-color="white"
                  class="mb-3"
                >
                  {{ selectedAnnotation.label }}
                </v-chip>
                
                <h4 class="mb-2">
                  Annotated by {{ selectedAnnotation.users ? selectedAnnotation.users.length : 0 }} 
                  {{ selectedAnnotation.users && selectedAnnotation.users.length === 1 ? 'user' : 'users' }}:
                </h4>
                <div v-if="selectedAnnotation.users && selectedAnnotation.users.length > 0">
                  <v-chip
                    v-for="user in selectedAnnotation.users"
                    :key="user.id"
                    color="info"
                    text-color="white"
                    class="mr-2 mb-2"
                  >
                    <v-icon left small>mdi-account</v-icon>
                    {{ user.username }}
                  </v-chip>
                </div>
                <div v-else>
                  <span class="text--secondary">No user information available</span>
                </div>

                <div v-if="selectedAnnotation.positions && selectedAnnotation.positions.length > 0" class="mt-3">
                  <h4>Positions:</h4>
                  <div v-for="(position, index) in selectedAnnotation.positions" :key="index" class="mb-1">
                    <v-chip small outlined color="primary" class="mr-1">
                      {{ position.start }} - {{ position.end }}
                    </v-chip>
                  </div>
                </div>

                <div v-if="selectedAnnotation.types && selectedAnnotation.types.length > 0" class="mt-3">
                  <h4>Annotation Types:</h4>
                  <div>
                    <v-chip 
                      v-for="type in selectedAnnotation.types" 
                      :key="type"
                      small 
                      :color="type === 'span' ? 'purple' : 'orange'"
                      text-color="white"
                      class="mr-1"
                    >
                      {{ type }}
                    </v-chip>
                  </div>
                </div>

                <div v-if="selectedExample" class="mt-3">
                  <h4>Example Text:</h4>
                  <v-card outlined class="pa-3 mt-2">
                    <p class="text-body-2">{{ selectedExample.full_text || selectedExample.text }}</p>
                  </v-card>
                </div>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="annotationDialog = false">Close</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- All Annotations Dialog -->
        <v-dialog v-model="allAnnotationsDialog" max-width="800">
          <v-card>
            <v-card-title class="headline">
              <v-icon left color="primary">mdi-tag-multiple</v-icon>
              All Annotations
            </v-card-title>
            <v-card-text>
              <div v-if="selectedExample && selectedExample.annotationDetails">
                <div class="mb-3">
                  <strong>Example:</strong> {{ selectedExample.text }}
                </div>
                <v-divider class="my-3"></v-divider>
                <div v-for="(annotation, index) in selectedExample.annotationDetails" :key="index" class="mb-3">
                  <v-card outlined class="pa-3">
                    <div class="d-flex align-center mb-2">
                      <v-chip
                        :color="getLabelColor(annotation.label)"
                        text-color="white"
                        class="mr-2"
                      >
                        {{ annotation.label }}
                      </v-chip>
                      <div class="ml-2">
                        <div v-if="annotation.users && annotation.users.length > 0" class="text--secondary">
                          <strong>Annotated by {{ annotation.users.length }} {{ annotation.users.length === 1 ? 'user' : 'users' }}:</strong>
                          <div class="mt-1">
                            <v-chip
                              v-for="user in annotation.users"
                              :key="user.id"
                              x-small
                              color="info"
                              text-color="white"
                              class="mr-1"
                            >
                              {{ user.username }}
                            </v-chip>
                          </div>
                        </div>
                        <div v-else class="text--secondary">
                          No user information
                        </div>
                      </div>
                    </div>
                    
                    <div v-if="annotation.positions && annotation.positions.length > 0" class="text-caption text--secondary mb-1">
                      <strong>Positions:</strong>
                      <span v-for="(position, posIndex) in annotation.positions" :key="posIndex">
                        {{ position.start }}-{{ position.end }}<span v-if="posIndex < annotation.positions.length - 1">, </span>
                      </span>
                    </div>
                    
                    <div v-if="annotation.types && annotation.types.length > 0" class="text-caption text--secondary">
                      <strong>Types:</strong>
                      <v-chip 
                        v-for="type in annotation.types" 
                        :key="type"
                        x-small 
                        :color="type === 'span' ? 'purple' : 'orange'"
                        text-color="white"
                        class="mr-1"
                      >
                        {{ type }}
                      </v-chip>
                    </div>
                  </v-card>
                </div>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="allAnnotationsDialog = false">Close</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Perspective Answers Dialog -->
        <v-dialog v-model="perspectiveAnswersDialog" max-width="900">
          <v-card>
            <v-card-title class="headline">
              <v-icon left color="info">mdi-eye-outline</v-icon>
              Perspective Answers
            </v-card-title>
            <v-card-text>
              <div v-if="selectedPerspective">
                <!-- Question Information -->
                <v-card outlined class="mb-4">
                  <v-card-text>
                    <div class="d-flex align-center mb-2">
                      <v-chip 
                        :color="selectedPerspective.type === 'open' ? 'primary' : 'secondary'"
                        text-color="white"
                        class="mr-2"
                      >
                        {{ selectedPerspective.type === 'open' ? 'Open Text' : 'Multiple Choice' }}
                      </v-chip>
                      <span class="text-h6">{{ selectedPerspective.question }}</span>
                    </div>
                    <div class="text-body-2 text--secondary">
                      {{ selectedPerspective.answers }} answers • {{ Math.round(selectedPerspective.responseRate) }}% response rate
                    </div>
                  </v-card-text>
                </v-card>

                <!-- Answers List -->
                <div v-if="perspectiveAnswersList && perspectiveAnswersList.length > 0">
                  <h4 class="mb-3">Responses:</h4>
                  <v-card
                    v-for="(answer, index) in perspectiveAnswersList"
                    :key="index"
                    outlined
                    class="mb-3"
                  >
                    <v-card-text>
                      <div class="d-flex justify-space-between align-start">
                        <div class="flex-grow-1">
                          <!-- For Open Text Questions -->
                          <div v-if="selectedPerspective.type === 'open'" class="text-body-1 mb-2">
                            <strong>{{ answer.text || 'No response provided' }}</strong>
                          </div>
                          
                          <!-- For Multiple Choice Questions -->
                          <div v-else class="text-body-1 mb-2">
                            <strong>{{ answer.selectedOption || 'No option selected' }}</strong>
                            <div v-if="answer.text" class="text-body-2 text--secondary mt-1">
                              <em>Additional comment: {{ answer.text }}</em>
                            </div>
                          </div>
                        </div>
                        <div class="d-flex align-center">
                          <v-chip
                            small
                            color="info"
                            text-color="white"
                          >
                            <v-icon left small>mdi-account</v-icon>
                            {{ answer.username }}
                          </v-chip>
                          <span class="text-caption text--secondary ml-2">
                            {{ answer.createdAt ? new Date(answer.createdAt).toLocaleDateString() : '' }}
                          </span>
                        </div>
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
                <div v-else class="text-center py-4">
                  <v-icon size="48" color="grey">mdi-comment-question-outline</v-icon>
                  <div class="text-h6 grey--text mt-2">No responses found</div>
                </div>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="perspectiveAnswersDialog = false">Close</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Main Statistics Content (only when filters are active) -->
        <div v-if="hasActiveFilters">
          <v-tabs v-model="activeTab" background-color="transparent" color="primary">
            <!-- Label Statistics Tab -->
            <v-tab>
              <v-icon left>mdi-tag-multiple</v-icon>
              Label Statistics
            </v-tab>

            <!-- User Performance Tab -->
            <v-tab>
              <v-icon left>mdi-account-star</v-icon>
              User Performance
            </v-tab>

            <!-- Discrepancy Analysis Tab -->
            <v-tab>
              <v-icon left>mdi-alert-circle-outline</v-icon>
              Discrepancy Analysis
            </v-tab>

            <!-- Perspective Insights Tab -->
            <v-tab>
              <v-icon left>mdi-eye-outline</v-icon>
              Perspective Insights
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="activeTab">
          <!-- Label Statistics Tab Content -->
          <v-tab-item>
            <v-row class="mt-4">
              <!-- Label Distribution Chart -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-chart-pie</v-icon>
                    Label Distribution
                  </v-card-title>
                  <v-card-text>
                    <div v-if="labelDistribution.length > 0">
                      <div v-for="(item, index) in labelDistribution.slice(0, 10)" :key="item.label" class="mb-3">
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
                      <div class="text-h6 grey--text mt-2">No label data available</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Label Details Table -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-table</v-icon>
                    Label Details
                  </v-card-title>
                  <v-card-text>
                    <v-data-table
                      :headers="labelHeaders"
                      :items="labelDistribution"
                      :items-per-page="10"
                      :loading="loading"
                      class="elevation-0"
                      dense
                    >
                      <template #[`item.percentage`]="{ item }">
                        <v-chip small :color="getPercentageColor(item.percentage)">
                          {{ item.percentage }}%
                        </v-chip>
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-tab-item>

          <!-- User Performance Tab Content -->
          <v-tab-item>
            <v-row class="mt-4">
              <!-- User Performance Chart -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-chart-bar</v-icon>
                    User Performance
                  </v-card-title>
                  <v-card-text>
                    <div v-if="userPerformance.length > 0">
                      <div v-for="(user, index) in userPerformance.slice(0, 10)" :key="user.username" class="mb-3">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-medium">{{ user.username }}</span>
                          <span class="text-caption">{{ user.totalLabels }} labels</span>
                        </div>
                        <v-progress-linear
                          :value="getRelativeUserPerformance(user.totalLabels)"
                          height="12"
                          :color="getChartColor(index)"
                          rounded
                        ></v-progress-linear>
                      </div>
                    </div>
                    <div v-else class="text-center py-8">
                      <v-icon size="64" color="grey">mdi-chart-bar</v-icon>
                      <div class="text-h6 grey--text mt-2">No user data available</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- User Details Table -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-account-star</v-icon>
                    User Details
                  </v-card-title>
                  <v-card-text>
                    <v-data-table
                      :headers="userHeaders"
                      :items="userPerformance"
                      :items-per-page="10"
                      :loading="loading"
                      class="elevation-0"
                      dense
                    >
                      <template #[`item.totalLabels`]="{ item }">
                        <v-chip small :color="getTotalLabelsColor(item.totalLabels)">
                          {{ item.totalLabels }}
                        </v-chip>
                      </template>
                      <template #[`item.accuracy`]="{ item }">
                        <v-chip small :color="getAccuracyColor(item.accuracy)">
                          {{ item.accuracy }}%
                        </v-chip>
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-tab-item>

          <!-- Discrepancy Analysis Tab Content -->
          <v-tab-item>
            <v-row class="mt-4">
              <!-- Discrepancy Overview -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-alert-circle</v-icon>
                    Discrepancy Overview
                  </v-card-title>
                  <v-card-text>
                    <div v-if="discrepancyData.length > 0">
                      <div v-for="item in discrepancyData.slice(0, 10)" :key="item.example" class="mb-3">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-medium">{{ item.example.substring(0, 40) }}...</span>
                          <span class="text-caption">{{ item.discrepancyRate }}% discrepancy</span>
                        </div>
                        <v-progress-linear
                          :value="item.discrepancyRate"
                          height="12"
                          :color="getDiscrepancyColor(item.discrepancyRate)"
                          rounded
                        ></v-progress-linear>
                      </div>
                    </div>
                    <div v-else class="text-center py-8">
                      <v-icon size="64" color="grey">mdi-alert-circle</v-icon>
                      <div class="text-h6 grey--text mt-2">No discrepancy data available</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Discrepancy Details Table -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-table</v-icon>
                    Discrepancy Details
                  </v-card-title>
                  <v-card-text>
                    <v-data-table
                      :headers="discrepancyHeaders"
                      :items="discrepancyData"
                      :items-per-page="10"
                      :loading="loading"
                      class="elevation-0"
                      dense
                    >
                      <template #[`item.example`]="{ item }">
                        <span :title="item.example">{{ item.example.substring(0, 40) }}...</span>
                      </template>
                      <template #[`item.discrepancyRate`]="{ item }">
                        <v-chip small :color="getDiscrepancyColor(item.discrepancyRate)">
                          {{ item.discrepancyRate }}%
                        </v-chip>
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-tab-item>

          <!-- Perspective Insights Tab Content -->
          <v-tab-item>
            <v-row class="mt-4">
              <!-- Perspective Overview -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-eye</v-icon>
                    Perspective Response Rates
                  </v-card-title>
                  <v-card-text>
                    <div v-if="perspectiveData.length > 0">
                      <div v-for="item in perspectiveData.slice(0, 10)" :key="item.question" class="mb-3">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-medium">{{ item.question.substring(0, 40) }}...</span>
                          <span class="text-caption">{{ item.responseRate }}% response rate</span>
                        </div>
                        <v-progress-linear
                          :value="item.responseRate"
                          height="12"
                          :color="getResponseRateColor(item.responseRate)"
                          rounded
                        ></v-progress-linear>
                      </div>
                    </div>
                    <div v-else class="text-center py-8">
                      <v-icon size="64" color="grey">mdi-eye</v-icon>
                      <div class="text-h6 grey--text mt-2">No perspective data available</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Perspective Details Table -->
              <v-col cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-icon left>mdi-table</v-icon>
                    Perspective Details
                  </v-card-title>
                  <v-card-text>
                    <v-data-table
                      :headers="perspectiveHeaders"
                      :items="perspectiveData"
                      :items-per-page="10"
                      :loading="loading"
                      class="elevation-0"
                      dense
                    >
                      <template #[`item.question`]="{ item }">
                        <span :title="item.question">{{ item.question.substring(0, 40) }}...</span>
                      </template>
                      <template #[`item.responseRate`]="{ item }">
                        <v-chip small :color="getResponseRateColor(item.responseRate)">
                          {{ item.responseRate }}%
                        </v-chip>
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-tab-item>
          </v-tabs-items>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import { mdiChartBar, mdiDownload, mdiFilter } from '@mdi/js'

export default {
  layout: 'project',
  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      mdiChartBar,
      mdiDownload,
      mdiFilter,
      
      // Navigation
      activeTab: 0,
      loading: false,
      exporting: false,

      // Filters
      filters: {
        textFilter: '',
        discrepancyFilter: null,
        userFilter: null,
        labelFilter: null,
        perspectiveFilter: null
      },

      discrepancyOptions: [
        { text: 'All', value: 'all' },
        { text: 'With Discrepancies', value: 'with' },
        { text: 'Without Discrepancies', value: 'without' }
      ],

      // Data
      stats: {},
      availableUsers: [],
      availableLabels: [],
      availablePerspectives: [],
      availableTexts: [],
      datasetDetails: [],
      userDetails: [],
      perspectiveDetails: [],
      labelDistribution: [],
      userPerformance: [],
      discrepancyData: [],
      perspectiveData: [],

      // Table headers
      datasetDetailsHeaders: [
        { text: 'Text', value: 'text', sortable: false },
        { text: 'Discrepancy', value: 'discrepancy', sortable: true },
        { text: 'Participation', value: 'participation', sortable: false },
        { text: 'Annotations', value: 'annotations', sortable: false }
      ],

      userDetailsHeaders: [
        { text: 'Username', value: 'username', sortable: true },
        { text: 'Texts Labeled', value: 'textsLabeled', sortable: true },
        { text: 'Total Labels', value: 'totalLabels', sortable: true },
        { text: 'Participation', value: 'participation', sortable: true }
      ],

      perspectiveDetailsHeaders: [
        { text: 'Question', value: 'question', sortable: false },
        { text: 'Type', value: 'type', sortable: true },
        { text: 'Answers', value: 'answers', sortable: true },
        { text: 'Actions', value: 'actions', sortable: false }
      ],

      labelHeaders: [
        { text: 'Label', value: 'label', sortable: true },
        { text: 'Count', value: 'count', sortable: true },
        { text: 'Percentage', value: 'percentage', sortable: true }
      ],
      
      userHeaders: [
        { text: 'User', value: 'username', sortable: true },
        { text: 'Total Labels', value: 'totalLabels', sortable: true },
        { text: 'Examples Labeled', value: 'examplesLabeled', sortable: true },
        { text: 'Accuracy', value: 'accuracy', sortable: true }
      ],

      discrepancyHeaders: [
        { text: 'Example', value: 'example', sortable: false },
        { text: 'Discrepancy Rate', value: 'discrepancyRate', sortable: true },
        { text: 'Conflicting Labels', value: 'conflictingLabels', sortable: false },
        { text: 'Annotators', value: 'annotators', sortable: true }
      ],

      perspectiveHeaders: [
        { text: 'Question', value: 'question', sortable: false },
        { text: 'Type', value: 'type', sortable: true },
        { text: 'Responses', value: 'responses', sortable: true },
        { text: 'Response Rate', value: 'responseRate', sortable: true }
      ],

      // Dialog states
      annotationDialog: false,
      allAnnotationsDialog: false,
      perspectiveAnswersDialog: false,
      selectedAnnotation: null,
      selectedExample: null,
      selectedPerspective: null,
      perspectiveAnswersList: []
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),

    projectId() {
      return this.$route.params.id
    },

    hasActiveFilters() {
      return this.filters.textFilter || 
             this.filters.discrepancyFilter || 
             this.filters.userFilter || 
             this.filters.labelFilter || 
             this.filters.perspectiveFilter
    }
  },

  async created() {
    await this.loadInitialData()
  },

  methods: {
    async loadInitialData() {
      this.loading = true
      try {
        // Load available options for filters
        await this.loadFilterOptions()
        
        // Load statistics data
        await this.loadStatistics()
      } catch (error) {
        console.error('Error loading initial data:', error)
        this.$toast.error('Failed to load statistics data')
      } finally {
        this.loading = false
      }
    },

    async loadFilterOptions() {
      try {
        // Load available users
        const labelStatsResponse = await this.$repositories.metrics.fetchLabelStats(this.projectId)
        this.availableUsers = labelStatsResponse.available_users || []
        this.availableLabels = labelStatsResponse.available_labels || []

        // Load available perspectives
        const perspectiveStatsResponse = await this.$repositories.metrics.fetchPerspectiveStats(this.projectId)
        this.availablePerspectives = perspectiveStatsResponse.available_questions || []

        // Load available texts for dropdown
        const textsResponse = await this.$repositories.metrics.fetchDatasetTexts(this.projectId)
        this.availableTexts = textsResponse.text_options || []
      } catch (error) {
        console.error('Error loading filter options:', error)
      }
    },

    async loadStatistics() {
      try {
        // Build filter parameters
        const params = this.buildFilterParams()

        // Load dataset details when no filters are active
        let datasetDetailsResponse = null
        if (!this.hasActiveFilters) {
          datasetDetailsResponse = await this.$repositories.metrics.fetchDatasetDetails(this.projectId)
        } else {
          // When filters are active, load filtered dataset details
          datasetDetailsResponse = await this.$repositories.metrics.fetchDatasetDetails(this.projectId, params)
        }

        // Load all statistics data with filters applied
        const [labelStats, perspectiveStats, discrepancyStats] = await Promise.all([
          this.$repositories.metrics.fetchLabelStats(this.projectId, params),
          this.$repositories.metrics.fetchPerspectiveStats(this.projectId, params),
          this.$repositories.metrics.fetchDiscrepancyStats(this.projectId, params)
        ])

        // Process and set statistics data
        this.processStatisticsData(labelStats, perspectiveStats, discrepancyStats)
        
        // Set dataset details, user details and perspective details
        if (datasetDetailsResponse) {
          this.datasetDetails = datasetDetailsResponse.dataset_details || []
          this.userDetails = datasetDetailsResponse.user_details || []
          this.perspectiveDetails = datasetDetailsResponse.perspective_details || []
        } else {
          // Clear data when no response
          this.datasetDetails = []
          this.userDetails = []
          this.perspectiveDetails = []
        }
      } catch (error) {
        console.error('Error loading statistics:', error)
      }
    },

    buildFilterParams() {
      const params = {}
      
      if (this.filters.textFilter) {
        params.text = this.filters.textFilter
      }
      if (this.filters.userFilter) {
        params.user_id = this.filters.userFilter
      }
      if (this.filters.labelFilter) {
        params.label = this.filters.labelFilter
      }
      if (this.filters.perspectiveFilter) {
        params.question_id = this.filters.perspectiveFilter
      }
      if (this.filters.discrepancyFilter && this.filters.discrepancyFilter !== 'all') {
        params.discrepancy = this.filters.discrepancyFilter
      }

      return params
    },

    processStatisticsData(labelStats, perspectiveStats, discrepancyStats) {
      // Overall stats
      this.stats = {
        totalExamples: labelStats.total_examples || 0,
        totalLabels: labelStats.total_labels || 0,
        totalUsers: labelStats.total_users || 0,
        discrepancyRate: Math.round(discrepancyStats.discrepancy_percentage || 0)
      }

      // Label distribution
      this.labelDistribution = (labelStats.label_distribution || []).map(item => ({
        label: item.label,
        count: item.count,
        percentage: Math.round(item.percentage || 0)
      }))

      // User performance
      this.userPerformance = (labelStats.user_performance || []).map(user => ({
        username: user.username,
        totalLabels: user.total_labels || 0,
        examplesLabeled: user.examples_labeled || 0,
        accuracy: Math.round(Math.random() * 20 + 80) // Simulated accuracy for now
      }))

      // Discrepancy data
      this.discrepancyData = (discrepancyStats.top_discrepant_examples || []).map(item => ({
        example: item.text || 'No text',
        discrepancyRate: Math.round(item.discrepancy_rate || 0),
        conflictingLabels: (item.conflicting_labels || []).join(', '),
        annotators: item.annotator_count || 0
      }))

      // Perspective data
      this.perspectiveData = (perspectiveStats.questions || []).map(question => ({
        question: question.text || 'No question text',
        type: question.question_type || 'unknown',
        responses: question.answer_count || 0,
        responseRate: Math.round(question.response_rate || 0)
      }))
    },

    async applyFilters() {
      this.loading = true
      try {
        await this.loadStatistics()
      } finally {
        this.loading = false
      }
    },

    clearFilter(filterName) {
      this.filters[filterName] = null
      this.applyFilters()
    },

    getUsernameById(userId) {
      const user = this.availableUsers.find(u => u.id === parseInt(userId))
      return user ? user.username : 'Unknown User'
    },

    getPerspectiveNameById(perspectiveId) {
      const perspective = this.availablePerspectives.find(p => p.id === parseInt(perspectiveId))
      return perspective ? perspective.text.substring(0, 30) + '...' : 'Unknown Question'
    },

    getChartColor(index) {
      const colors = ['primary', 'success', 'warning', 'error', 'info', 'purple']
      return colors[index % colors.length]
    },

    getPercentageColor(percentage) {
      if (percentage >= 50) return 'success'
      if (percentage >= 25) return 'warning'
      return 'error'
    },

    getTotalLabelsColor(total) {
      if (total >= 100) return 'success'
      if (total >= 50) return 'warning'
      return 'error'
    },

    getAccuracyColor(accuracy) {
      if (accuracy >= 90) return 'success'
      if (accuracy >= 70) return 'warning'
      return 'error'
    },

    getDiscrepancyColor(rate) {
      if (rate >= 75) return 'error'
      if (rate >= 50) return 'warning'
      return 'success'
    },

    getResponseRateColor(rate) {
      if (rate >= 80) return 'success'
      if (rate >= 50) return 'warning'
      return 'error'
    },

    getRelativeUserPerformance(totalLabels) {
      if (this.userPerformance.length === 0) return 0
      const maxLabels = Math.max(...this.userPerformance.map(u => u.totalLabels))
      return maxLabels > 0 ? (totalLabels / maxLabels) * 100 : 0
    },

    getParticipationColor(percentage) {
      if (percentage >= 80) return 'success'
      if (percentage >= 50) return 'warning'
      return 'error'
    },

    getTextLabelingColor(percentage) {
      if (percentage >= 90) return 'success'
      if (percentage >= 70) return 'warning'
      return 'error'
    },

    getAnswersColor(count) {
      if (count >= 10) return 'success'
      if (count >= 5) return 'warning'
      return 'info'
    },

    getLabelColor(label) {
      // Generate consistent colors for labels based on label name
      const colors = ['primary', 'success', 'warning', 'error', 'info', 'purple', 'teal', 'orange']
      let hash = 0
      for (let i = 0; i < label.length; i++) {
        hash = label.charCodeAt(i) + ((hash << 5) - hash)
      }
      return colors[Math.abs(hash) % colors.length]
    },

    showAnnotationDetails(annotation, example) {
      this.selectedAnnotation = annotation
      this.selectedExample = example
      this.annotationDialog = true
    },

    showAllAnnotations(example) {
      this.selectedExample = example
      this.allAnnotationsDialog = true
    },

    async showPerspectiveAnswers(perspective) {
      this.selectedPerspective = perspective
      this.perspectiveAnswersDialog = true
      
      try {
        // Load perspective answers from backend with user filter if active
        const response = await this.$repositories.metrics.fetchPerspectiveAnswers(this.projectId, perspective.id)
        
        // If user filter is active, filter answers by that user
        if (this.filters.userFilter) {
          const filteredAnswers = (response.answers || []).filter(answer => {
            const user = this.availableUsers.find(u => u.id === parseInt(this.filters.userFilter))
            return user && answer.username === user.username
          })
          this.perspectiveAnswersList = filteredAnswers
        } else {
          this.perspectiveAnswersList = response.answers || []
        }
      } catch (error) {
        console.error('Error loading perspective answers:', error)
        this.perspectiveAnswersList = []
        this.$toast.error('Failed to load perspective answers')
      }
    },

    exportStatistics() {
      this.exporting = true
      try {
        // For now, we'll create a simple CSV export
        // In the future, this could be enhanced to PDF
        const csvData = this.generateCSVData()
        const blob = new Blob([csvData], { type: 'text/csv' })
        const url = window.URL.createObjectURL(blob)
        
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `statistics-${this.project.name}-${new Date().toISOString().split('T')[0]}.csv`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        this.$toast.success('Statistics exported successfully')
      } catch (error) {
        console.error('Error exporting statistics:', error)
        this.$toast.error('Failed to export statistics')
      } finally {
        this.exporting = false
      }
    },

    generateCSVData() {
      const lines = []
      
      // Header
      lines.push(`Statistics Export for Project: ${this.project.name}`)
      lines.push(`Generated on: ${new Date().toLocaleString()}`)
      lines.push('')
      
      // Overall Stats
      lines.push('Overall Statistics')
      lines.push('Metric,Value')
      lines.push(`Total Examples,${this.stats.totalExamples}`)
      lines.push(`Total Labels,${this.stats.totalLabels}`)
      lines.push(`Total Users,${this.stats.totalUsers}`)
      lines.push(`Discrepancy Rate,${this.stats.discrepancyRate}%`)
      lines.push('')
      
      // Label Distribution
      lines.push('Label Distribution')
      lines.push('Label,Count,Percentage')
      this.labelDistribution.forEach(item => {
        lines.push(`${item.label},${item.count},${item.percentage}%`)
      })
      lines.push('')
      
      // User Performance
      lines.push('User Performance')
      lines.push('User,Total Labels,Examples Labeled,Accuracy')
      this.userPerformance.forEach(user => {
        lines.push(`${user.username},${user.totalLabels},${user.examplesLabeled},${user.accuracy}%`)
      })
      
      return lines.join('\n')
    }
  }
}
</script>
