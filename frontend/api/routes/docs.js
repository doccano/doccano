const fs = require('fs')
const express = require('express')
const router = express.Router()
let db = JSON.parse(fs.readFileSync('./api/db/docs.json', 'utf8'))

// Get doc list.
router.get('/', (req, res) => {
  const q = req.query.q
  if (q) {
    res.json(db.filter(item => item.text.toLowerCase().includes(q.toLowerCase())))
  } else {
    res.json(db)
  }
})

// Create a doc.
router.post('/', (req, res) => {
  const doc = {
    id: db.reduce((x, y) => { return x.id > y.id ? x : y }).id + 1,
    text: req.body.text
  }
  res.json(doc)
})

// Update a document partially.
router.patch('/:docId', (req, res) => {
  const docIndex = db.findIndex(item => item.id === parseInt(req.params.docId))
  if (docIndex !== -1) {
    Object.assign(db[docIndex], req.body)
    res.json(db[docIndex])
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Get a doc.
router.get('/:docId', (req, res) => {
  const doc = db.find(item => item.id === parseInt(req.params.docId))
  if (doc) {
    res.json(doc)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Update a doc.
router.put('/:docId', (req, res) => {
  const docIndex = db.findIndex(item => item.id === parseInt(req.params.docId))
  if (docIndex !== -1) {
    db[docIndex] = req.body
    res.json(db[docIndex])
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Delete a doc.
router.delete('/:docId', (req, res, next) => {
  const doc = db.find(item => item.id === parseInt(req.params.docId))
  if (doc) {
    db = db.filter(item => item.id !== parseInt(req.params.docId))
    res.json(doc)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})
module.exports = router
