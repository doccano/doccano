const fs = require('fs')
const express = require('express')
const router = express.Router()
const db = JSON.parse(fs.readFileSync('./api/db/users.json', 'utf8'))

// Get user list.
router.get('/', (req, res) => {
  const q = req.query.q
  if (q) {
    res.json(db.filter(item => item.username.toLowerCase().includes(q.toLowerCase())))
  } else {
    res.json(db)
  }
})

// Get a user.
router.get('/:userId', (req, res) => {
  const user = db.find(item => item.id === parseInt(req.params.userId, 10))
  if (user) {
    res.json(user)
  } else {
    res.status(404).json({ detail: 'Not found.' })
  }
})

module.exports = router
