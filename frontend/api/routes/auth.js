const express = require('express')
const router = express.Router()

// Get a token.
router.get('/api-token-auth', (req, res) => {
  res.json({
    token: '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
  })
})

module.exports = router
