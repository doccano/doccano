const express = require('express')
const app = express()

const docs = require('./routes/docs')
const labels = require('./routes/labels')
const projects = require('./routes/projects')
const members = require('./routes/members')
const users = require('./routes/users')
const stats = require('./routes/stats')
const auth = require('./routes/auth')

app.use('/auth', auth)
app.use('/users', users)
app.use('/projects', projects)
app.use('/projects/:project_id/statistics', stats)
app.use('/projects/:project_id/docs', docs)
app.use('/projects/:project_id/labels', labels)
app.use('/projects/:project_id/users', members)

module.exports = {
  path: '/v1',
  handler: app
}
