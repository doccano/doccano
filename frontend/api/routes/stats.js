const fs = require('fs')
const express = require('express')
const router = express.Router()
const db = JSON.parse(fs.readFileSync('./api/db/stats.json', 'utf8'))

// Get statistics.
router.get('/', (req, res) => {
  res.json(db)
})

module.exports = router
