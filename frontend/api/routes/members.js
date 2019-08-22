const fs = require('fs')
const bodyParser = require('body-parser')
const express = require('express')
const router = express.Router()
let db = JSON.parse(fs.readFileSync('./api/db/members.json', 'utf8'))
const users = JSON.parse(fs.readFileSync('./api/db/users.json', 'utf8'))
router.use(bodyParser.json())
router.use(bodyParser.urlencoded({ extended: true }))

// Get project user list.
router.get('/', (req, res) => {
  const q = req.query.q
  if (q) {
    res.json(db.filter(item => item.name.toLowerCase().includes(q.toLowerCase())))
  } else {
    res.json(db)
  }
})

// Add a project user.
router.post('/', (req, res) => {
  const user = users.find(item => item.id === parseInt(req.body.id))
  db.push(user)
  res.json(user)
})

// Update a project user.
router.put('/:userId', (req, res) => {
  const projectIndex = db.findIndex(item => item.id === parseInt(req.params.userId))
  if (projectIndex !== -1) {
    db[projectIndex] = req.body
    res.json(db[projectIndex])
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Delete a project user.
router.delete('/:userId', (req, res, next) => {
  const project = db.find(item => item.id === parseInt(req.params.userId))
  if (project) {
    db = db.filter(item => item.id !== parseInt(req.params.userId))
    res.json(project)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

module.exports = router
