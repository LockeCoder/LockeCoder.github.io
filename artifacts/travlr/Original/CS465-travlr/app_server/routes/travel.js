const express = require("express");
const router = express.Router();
const traveler = require("../controllers/traveler.controller");

router.get("/", traveler.travel);

module.exports = router;