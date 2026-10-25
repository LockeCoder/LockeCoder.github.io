const tripsEndpoint = 'http://localhost:3000/api/trips';

const travel = async (req, res) => {
  try {
    const response = await fetch(tripsEndpoint);
    const trips = await response.json();

    res.render('travel', {
      title: 'Travlr Getaways',
      trips: trips,
      homeClass: '',
      travelClass: 'selected',
      homeFooterClass: '',
      travelFooterClass: 'active'
    });
  } catch (err) {
    res.render('travel', {
      title: 'Travlr Getaways',
      trips: [],
      message: 'Unable to load trips',
      homeClass: '',
      travelClass: 'selected',
      homeFooterClass: '',
      travelFooterClass: 'active'
    });
  }
};

module.exports = {
  travel
};