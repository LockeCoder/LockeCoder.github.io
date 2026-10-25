const express = require('express');
const router = express.Router();

const ctrlTrips = require('../controllers/trips');
const ctrlAuth = require('../controllers/authentication');
const auth = require('../middleware/auth');

router.get('/trips', ctrlTrips.tripsList);
router.get('/trips/:tripCode', ctrlTrips.tripsFindByCode);

router.post('/login', ctrlAuth.login);

router.post('/trips', auth, ctrlTrips.tripsAddTrip);
router.put('/trips/:tripCode', auth, ctrlTrips.tripsUpdateTrip);
router.delete('/trips/:tripCode', auth, ctrlTrips.tripsDeleteTrip);

module.exports = router;