const fs = require('fs')
const bodyParser = require('body-parser')
const express = require('express')
const router = express.Router()
let db = JSON.parse(fs.readFileSync('./api/db/projects.json', 'utf8'))
router.use(bodyParser.json())
router.use(bodyParser.urlencoded({ extended: true }))

// Get project list.
router.get('/', (req, res) => {
  const q = req.query.q
  if (q) {
    res.json(db.filter(item => item.name.toLowerCase().includes(q.toLowerCase())))
  } else {
    res.json(db)
  }
})

// Create a project.
router.post('/', (req, res) => {
  const project = {
    id: db.reduce((x, y) => { return x.id > y.id ? x : y }).id + 1,
    name: req.body.name,
    description: req.body.description,
    guideline: 'Please write annotation guideline.',
    users: [1],
    project_type: req.body.project_type,
    image: '/static/assets/images/cats/text_classification.jpg',
    updated_at: '2019-08-21T02:49:48.790813Z',
    randomize_document_order: false
  }
  res.json(project)
})

// Get a project.
router.get('/:projectId', (req, res) => {
  const project = db.find(item => item.id === parseInt(req.params.projectId))
  if (project) {
    res.json(project)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Update a project.
router.put('/:projectId', (req, res) => {
  const projectIndex = db.findIndex(item => item.id === parseInt(req.params.projectId))
  if (projectIndex !== -1) {
    db[projectIndex] = req.body
    res.json(db[projectIndex])
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Delete a project.
router.delete('/:projectId', (req, res, next) => {
  const project = db.find(item => item.id === parseInt(req.params.projectId))
  if (project) {
    db = db.filter(item => item.id !== parseInt(req.params.projectId))
    res.json(project)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

module.exports = router
