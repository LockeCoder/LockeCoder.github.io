const fs = require('fs');
const path = require('path');
require('./db');
const mongoose = require('mongoose');
const Trip = mongoose.model('trips');

const tripsPath = path.join(__dirname, '../../data/trips.json');
const trips = JSON.parse(fs.readFileSync(tripsPath, 'utf8'));

const seedDB = async () => {
  try {
    await Trip.deleteMany({});
    console.log('Old trip records removed');

    await Trip.insertMany(trips);
    console.log('New trip records added');

    mongoose.connection.close();
  } catch (err) {
    console.log(err);
    mongoose.connection.close();
  }
};

seedDB();