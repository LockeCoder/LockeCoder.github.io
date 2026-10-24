var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var hbs = require('hbs');
var fs = require('fs');

var indexRouter = require('./app_server/routes/index');
var travelRouter = require('./app_server/routes/travel');

var app = express();

// view engine setup (points to app_server/views)
app.set('views', path.join(__dirname, 'app_server', 'views'));
app.set('view engine', 'hbs');

// Register partials only if folder exists
var partialsPath = path.join(__dirname, 'app_server', 'views', 'partials');
if (fs.existsSync(partialsPath)) {
  hbs.registerPartials(partialsPath);
}

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

// Static files served from /public
app.use(express.static(path.join(__dirname, 'public')));

// Stop favicon.ico 404 from triggering error rendering noise
app.get('/favicon.ico', function (req, res) {
  res.status(204).end();
});

// Routes
app.use('/travel', travelRouter);
app.use('/', indexRouter);

// Catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// Error handler (renders app_server/views/error.hbs)
app.use(function (err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;