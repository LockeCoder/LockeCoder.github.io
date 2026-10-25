const mongoose = require('mongoose');
const Trip = mongoose.model('trips');

const tripsList = async (req, res) => {
  try {
    const trips = await Trip.find({});
    res.status(200).json(trips);
  } catch (err) {
    res.status(500).json(err);
  }
};

const tripsFindByCode = async (req, res) => {
  try {
    const trip = await Trip.findOne({ code: req.params.tripCode });

    if (!trip) {
      return res.status(404).json({ message: 'Trip not found' });
    }

    res.status(200).json(trip);
  } catch (err) {
    res.status(500).json(err);
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

    res.status(201).json(trip);
  } catch (err) {
    res.status(400).json(err);
  }
};

const tripsUpdateTrip = async (req, res) => {
  try {
    const trip = await Trip.findOne({ code: req.params.tripCode });

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
    res.status(200).json(updatedTrip);
  } catch (err) {
    res.status(400).json(err);
  }
};

const tripsDeleteTrip = async (req, res) => {
  try {
    const deletedTrip = await Trip.findOneAndDelete({ code: req.params.tripCode });

    if (!deletedTrip) {
      return res.status(404).json({ message: 'Trip not found' });
    }

    res.status(204).send();
  } catch (err) {
    res.status(500).json(err);
  }
};

module.exports = {
  tripsList,
  tripsFindByCode,
  tripsAddTrip,
  tripsUpdateTrip,
  tripsDeleteTrip
};