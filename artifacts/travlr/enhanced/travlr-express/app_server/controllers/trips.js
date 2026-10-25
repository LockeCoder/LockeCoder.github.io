const mongoose = require('mongoose');
const Trip = mongoose.model('trips');

const tripsList = async (req, res) => {
  try {
    const trips = await Trip.find({});
    return res.status(200).json(trips);
  } catch (err) {
    return res.status(500).json({
      message: 'Error retrieving trips',
      error: err.message
    });
  }
};

const tripsFindByCode = async (req, res) => {
  try {
    const { tripCode } = req.params;

    if (!tripCode) {
      return res.status(400).json({ message: 'tripCode is required' });
    }

    const trip = await Trip.findOne({ code: tripCode });

    if (!trip) {
      return res.status(404).json({ message: 'Trip not found' });
    }

    return res.status(200).json(trip);
  } catch (err) {
    return res.status(500).json({
      message: 'Error retrieving trip',
      error: err.message
    });
  }
};

const tripsAddTrip = async (req, res) => {
  try {
    const trip = await Trip.create({
      code: req.body.code,
      name: req.body.name,
      length: req.body.length,
      start: req.body.start,
      resort: req.body.resort,
      perPerson: req.body.perPerson,
      image: req.body.image,
      description: req.body.description
    });

    return res.status(201).json(trip);
  } catch (err) {
    return res.status(400).json({
      message: 'Error creating trip',
      error: err.message
    });
  }
};

const tripsUpdateTrip = async (req, res) => {
  try {
    const { tripCode } = req.params;

    if (!tripCode) {
      return res.status(400).json({ message: 'tripCode is required' });
    }

    const trip = await Trip.findOne({ code: tripCode });

    if (!trip) {
      return res.status(404).json({ message: 'Trip not found' });
    }

    trip.code = req.body.code;
    trip.name = req.body.name;
    trip.length = req.body.length;
    trip.start = req.body.start;
    trip.resort = req.body.resort;
    trip.perPerson = req.body.perPerson;
    trip.image = req.body.image;
    trip.description = req.body.description;

    const updatedTrip = await trip.save();
    return res.status(200).json(updatedTrip);
  } catch (err) {
    return res.status(400).json({
      message: 'Error updating trip',
      error: err.message
    });
  }
};

const tripsDeleteTrip = async (req, res) => {
  try {
    const { tripCode } = req.params;

    if (!tripCode) {
      return res.status(400).json({ message: 'tripCode is required' });
    }

    const deletedTrip = await Trip.findOneAndDelete({ code: tripCode });

    if (!deletedTrip) {
      return res.status(404).json({ message: 'Trip not found' });
    }

    return res.status(204).send();
  } catch (err) {
    return res.status(500).json({
      message: 'Error deleting trip',
      error: err.message
    });
  }
};

module.exports = {
  tripsList,
  tripsFindByCode,
  tripsAddTrip,
  tripsUpdateTrip,
  tripsDeleteTrip
};