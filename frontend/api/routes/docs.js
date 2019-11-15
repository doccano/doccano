const fs = require('fs')
const express = require('express')
const router = express.Router()
const db = JSON.parse(fs.readFileSync('./api/db/docs.json', 'utf8'))

// Get doc list.
router.get('/', (req, res) => {
  const q = req.query.q
  if (q) {
    // res.json(db.filter(item => item.text.toLowerCase().includes(q.toLowerCase())))
    res.json(db)
  } else {
    res.json(db)
  }
})

// Create a doc.
router.post('/', (req, res) => {
  const doc = {
    id: db.results.reduce((x, y) => { return x.id > y.id ? x : y }).id + 1,
    text: req.body.text
  }
  res.json(doc)
})

// Upload a file.
router.post('/upload', (req, res) => {
  const doc = {
    id: db.results.reduce((x, y) => { return x.id > y.id ? x : y }).id + 1,
    text: 'Uploaded Document',
    meta: JSON.stringify({}),
    annotations: []
  }
  db.results.push(doc)
  res.json(doc)
})

// Download a file.
router.get('/download', (req, res) => {
  res.json(db)
})

// Update a document partially.
router.patch('/:docId', (req, res) => {
  const docIndex = db.results.findIndex(item => item.id === parseInt(req.params.docId, 10))
  if (docIndex !== -1) {
    Object.assign(db.results[docIndex], req.body)
    res.json(db.results[docIndex])
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Get a doc.
router.get('/:docId', (req, res) => {
  const doc = db.results.find(item => item.id === parseInt(req.params.docId, 10))
  if (doc) {
    res.json(doc)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Update a doc.
router.put('/:docId', (req, res) => {
  const docIndex = db.results.findIndex(item => item.id === parseInt(req.params.docId, 10))
  if (docIndex !== -1) {
    db.results[docIndex] = req.body
    res.json(db.results[docIndex])
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Delete a doc.
router.delete('/:docId', (req, res, next) => {
  const doc = db.results.find(item => item.id === parseInt(req.params.docId, 10))
  if (doc) {
    db.results = db.results.filter(item => item.id !== parseInt(req.params.docId, 10))
    res.json(doc)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Add an annotation.
router.post('/:docId/annotations', (req, res, next) => {
  const doc = db.results.find(item => item.id === parseInt(req.params.docId, 10))
  if (doc) {
    const annotation = {
      id: Math.floor(Math.random() * 10000),
      label: req.body.label,
      start_offset: req.body.start_offset,
      end_offset: req.body.end_offset,
      user: 1,
      document: parseInt(req.params.docId, 10),
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
  const doc = db.results.find(item => item.id === parseInt(req.params.docId, 10))
  const docIndex = db.results.findIndex(item => item.id === parseInt(req.params.docId, 10))
  if (doc) {
    const annotation = doc.annotations.find(item => item.id === parseInt(req.params.annotationId, 10))
    doc.annotations = doc.annotations.filter(item => item.id !== parseInt(req.params.annotationId, 10))
    db.results[docIndex] = doc
    res.json(annotation)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

// Update an annotation.
router.patch('/:docId/annotations/:annotationId', (req, res, next) => {
  const docIndex = db.results.findIndex(item => item.id === parseInt(req.params.docId, 10))
  if (docIndex !== -1) {
    const doc = db.results[docIndex]
    const annotationIndex = doc.annotations.findIndex(item => item.id === parseInt(req.params.annotationId, 10))
    Object.assign(db.results[docIndex].annotations[annotationIndex], req.body)
    res.json(db.results[docIndex].annotations[annotationIndex])
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})
module.exports = router
