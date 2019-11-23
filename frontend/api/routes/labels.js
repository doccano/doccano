const fs = require('fs')
const express = require('express')
const router = express.Router()
let db = JSON.parse(fs.readFileSync('./api/db/labels.json', 'utf8'))

// Get label list.
router.get('/', (req, res) => {
  const q = req.query.q
  if (q) {
    res.json(db.filter(item => item.text.toLowerCase().includes(q.toLowerCase())))
  } else {
    res.json(db)
  }
})

// Create a label.
router.post('/', (req, res) => {
  const label = {
    id: db.reduce((x, y) => { return x.id > y.id ? x : y }).id + 1,
    text: req.body.text,
    prefix_key: req.body.prefix_key,
    suffix_key: req.body.suffix_key,
    background_color: req.body.background_color,
    text_color: '#ffffff'
  }
  db.push(label)
  res.json(label)
})

// Get a label.
router.get('/:labelId', (req, res) => {
  const label = db.find(item => item.id === parseInt(req.params.labelId, 10))
  if (label) {
    res.json(label)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Update a label.
router.patch('/:labelId', (req, res) => {
  const labelIndex = db.findIndex(item => item.id === parseInt(req.params.labelId, 10))
  if (labelIndex !== -1) {
    // db[labelIndex] = req.body
    Object.assign(db[labelIndex], req.body)
    res.json(db[labelIndex])
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Delete a label.
router.delete('/:labelId', (req, res, next) => {
  const label = db.find(item => item.id === parseInt(req.params.labelId, 10))
  if (label) {
    db = db.filter(item => item.id !== parseInt(req.params.labelId, 10))
    res.json(label)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

module.exports = router
