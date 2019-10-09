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

// Upload a file.
router.post('/upload', (req, res) => {
  const doc = {
    id: db.reduce((x, y) => { return x.id > y.id ? x : y }).id + 1,
    text: 'Uploaded Document',
    meta: JSON.stringify({}),
    annotations: []
  }
  db.push(doc)
  res.json(doc)
})

// Download a file.
router.get('/download', (req, res) => {
  res.json(db)
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

// Add an annotation.
router.post('/:docId/annotations', (req, res, next) => {
  const doc = db.find(item => item.id === parseInt(req.params.docId))
  if (doc) {
    const annotation = {
      id: Math.floor(Math.random() * 10000),
      label: req.body.label,
      start_offset: req.body.start_offset,
      end_offset: req.body.end_offset,
      user: 1,
      document: parseInt(req.params.docId),
      text: req.body.text
    }
    doc.annotations.push(annotation)
    res.json(annotation)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Delete an annotation.
router.delete('/:docId/annotations/:annotationId', (req, res, next) => {
  const doc = db.find(item => item.id === parseInt(req.params.docId))
  const docIndex = db.findIndex(item => item.id === parseInt(req.params.docId))
  if (doc) {
    const annotation = doc.annotations.find(item => item.id === parseInt(req.params.annotationId))
    doc.annotations = doc.annotations.filter(item => item.id !== parseInt(req.params.annotationId))
    db[docIndex] = doc
    res.json(annotation)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Update an annotation.
router.patch('/:docId/annotations/:annotationId', (req, res, next) => {
  const docIndex = db.findIndex(item => item.id === parseInt(req.params.docId))
  if (docIndex !== -1) {
    const doc = db[docIndex]
    const annotationIndex = doc.annotations.findIndex(item => item.id === parseInt(req.params.annotationId))
    Object.assign(db[docIndex].annotations[annotationIndex], req.body)
    res.json(db[docIndex].annotations[annotationIndex])
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})
module.exports = router
