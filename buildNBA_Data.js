/* Modules Section
============================================= */

var _ = require("underscore");
var fs = require('fs');
var fast_csv = require("fast-csv");
var async = require("async");

// End of Modules

/* Helper Section
============================================= */

// End of Helper

/* Functions
============================================= */

/**
* Main Function
*/
(function () {

	// Type of stats
	var STATS = ['totals', 'advanced'];

	// Get generate our list of file paths
	var pathList = _.flatten(_.map(STATS, function (stat) {

		return _.map(_.range(1981,2016), function (year) {
			var finalStr = ['./data/csv/',stat,'/leagues_NBA_',
							year,'_',stat,'.csv'].join('');

			return finalStr;
		});
	}));

	// Divider ===================================

	async.each(pathList, function (path, _aCallback) {

		// Create File Stream
		var inputStream = fs.createReadStream(path);

		// Read in CSV file
		fast_csv.fromStream(inputStream,{
			headers: true,
			ignoreEmpty: true
		})
		.transform(function(data){
			// We might need this, im not sure...
			// Foreshadowing!!!!!
			return data;
		})
		.on("data", function(data){
			console.log(data);
		})
		.on("end", function(){
			console.log("done");
			_aCallback();
		});

	}, function (err) {
		console.log('hey were done!!');
	});
})();