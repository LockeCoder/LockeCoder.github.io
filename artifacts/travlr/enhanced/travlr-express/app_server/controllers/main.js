const main = (req, res) => {
  res.render('index', {
    title: 'Travlr Getaways',
    homeClass: 'selected',
    travelClass: '',
    homeFooterClass: 'active',
    travelFooterClass: ''
  });
};

module.exports = {
  main
};