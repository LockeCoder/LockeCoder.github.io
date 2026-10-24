// app_server/controllers/traveler.controller.js

const trips = [
  {
    name: "Coastal Escape",
    location: "Maui, Hawaii",
    duration: "7 days",
    price: "$1,799",
    description: "Beachfront resort, snorkeling, and guided island tours."
  },
  {
    name: "Mountain Adventure",
    location: "Banff, Canada",
    duration: "5 days",
    price: "$1,249",
    description: "Hiking, lake excursions, and scenic gondola rides."
  },
  {
    name: "City Explorer",
    location: "New York City, USA",
    duration: "3 days",
    price: "$799",
    description: "Downtown hotel, museums, and curated food experiences."
  }
];

exports.home = (req, res) => {
  res.render("index", { title: "Travlr Getaways", activeHome: true });
};

exports.travel = (req, res) => {
  res.render("travel", {
    title: "Travlr Getaways | Travel",
    activeTravel: true,
    trips
  });
};