<template>
    <v-app id="inspire">
        <v-main>
            <v-container class="fill-height" fluid>
                <!-- New section to display all users -->
                <v-row align="center" justify="center" class="mt-5">
                    <v-col cols="12" sm="8" md="6">
                        <v-card class="pa-0 overflow-hidden rounded-lg" width="100%">
                            <v-sheet color="primary" class="py-3 px-4 rounded-t">
                                <div class="text-h6 font-weight-medium text-black">
                                    All Users
                                </div>
                            </v-sheet>
                            <v-card-text class="pa-6">
                                <v-list>
                                    <v-list-item-group>
                                        <v-list-item v-for="user in sortedUsers" :key="user.id">
                                            <v-list-item-content>
                                                <v-list-item-title>{{ user.username }}

                                                </v-list-item-title>
                                                <v-list-item-subtitle>{{ user.email }}

                                                </v-list-item-subtitle>
                                            </v-list-item-content>
                                        </v-list-item>
                                    </v-list-item-group>
                                </v-list>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
export default {
    data() {
        return {
            valid: false,
            users: [],
            selectedUser: null,
            name: '',
            email: '',
            role: '',
            showError: false,
            errorMessage: '',
            nameRules: [
                (v) => !!v || 'Name is required',
                (v) => (v && v.length >= 3) || 'Name must be at least 3 characters'
            ],
            emailRules: [
                (v) => !!v || 'Email is required',
                (v) => /.+@.+\..+/.test(v) || 'E-mail must be valid'
            ],
            roleOptions: [
                { text: 'Admin', value: 'admin' },
                { text: 'Annotator', value: 'annotator' }
            ]
        }
    },
    async created() {
        await this.fetchUsers()
    },
    computed: {
        sortedUsers() {
            return [...this.users].sort((a, b) => a.id - b.id)
        }
    },
    methods: {
        async fetchUsers() {
            try {
                const response = await this.$axios.get('/v1/users/')
                this.users = response.data
            } catch (error) {
                console.error('Error fetching users:', error)
            }
        },
        async fetchUserDetails(userId) {
            try {
                const response = await this.$axios.get(`/api/users/${userId}/`)
                const user = response.data
                this.name = user.username
                this.email = user.email
                this.role = user.role
            } catch (error) {
                console.error('Error fetching user details:', error)
            }
        },
        async submitForm() {
            if (!this.valid) {
                this.showError = true
                this.errorMessage = 'Please fill in all required fields correctly'
                return
            }

            try {
                const userData = {
                    username: this.name,
                    email: this.email,
                    role: this.role
                }
                await this.$axios.put(`/api/users/${this.selectedUser}/`, userData)
                console.log('User updated successfully')
                this.showError = false
            } catch (error) {
                this.showError = true
                let errorDetail = ''
                if (error.response && error.response.data) {
                    for (const [field, messages] of Object.entries(error.response.data)) {
                        if (Array.isArray(messages)) {
                            errorDetail += `<strong>${field}:</strong> ${messages.join(', ')}<br/>`
                        } else {
                            errorDetail += `<strong>${field}:</strong> ${messages}<br/>`
                        }
                    }
                } else {
                    errorDetail = 'User update failed'
                }
                this.errorMessage = errorDetail
                console.error('Update error:', error.response && error.response.data)
            }
        }
    }
}
</script>