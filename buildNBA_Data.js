/* Modules Section
============================================= */

var _ = require("underscore");
var fs = require('fs');
var fast_csv = require("fast-csv");
var async = require("async");

// End of Modules

/* Helper Section
============================================= */
var getHeader = function (path) {
	var statObj = {
		'totals': 'Rk,Player,Pos,Age,Tm,G,GS,MP,FG,FGA,FG%,3P,3PA,3P%,2P,2PA,2P%,eFG%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS',
		'advanced': 'Rk,Player,Pos,Age,Tm,G,MP,PER,TS%,3PAr,FTr,ORB%,DRB%,TRB%,AST%,STL%,BLK%,TOV%,USG%,0,OWS,DWS,WS,WS/48,0,OBPM,DBPM,BPM,VORP'
	};
	return _.compact(_.map(statObj, function (val, key) {
		// key = totals || advanced
		// If key exist inside of path
		if (path.indexOf(key) > -1) {
			// Returns the value at statObj[statType]
			return val;
		}
	}))[0];
};
// End of Helper

/* Functions Section
============================================= */

/**
*Function Name: cleanData
*Parameters: array of file paths
*RUN: node misc_NBA_Data.js =CLEAN
*/
var cleanData = function(paths) {

	async.each(paths, function(filePath, callback) {
		// get data from file
		fs.readFile(filePath, function(err, data) {
			if(err) throw err;
			var data_Str = data.toString();
			// Remove double commas
			data_Str = data_Str.replace(/,,/g,',0,');
			var data_Arr = data_Str.split("\n");

			// Check if first row is empty
			if (!data_Arr[0].length) {
				data_Arr.shift();
			}

			data_Arr = _.filter(data_Arr, function (_str) {
				return (_str.indexOf('Rk,Player'));
			});

			var finalHeader = getHeader(filePath);
			console.log(finalHeader);

			data_Arr.unshift(finalHeader);
			var outputPath = filePath.replace(/csv/,'output');

			fs.writeFileSync(outputPath, data_Arr.join('\n'));
			callback();
		});
	},function (err) {
		console.log('*****DONE CLEANING DATA*****');
	});
};


/**
*Function Name: buildData
*Parameters: array of file paths
*RUN: node misc_NBA_Data.js =BUILD
*/
var buildData = function(paths) {
	async.each(paths, function (path, _aCallback) {

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
		console.log('*****DONE BUILDING DATA*****');
	});
};

/**
- Main Function
*/
(function (task, isTest) {


	// Allowed Tasks
	if (['=BUILD','=CLEAN'].indexOf(task) === -1) {
		console.log('You did not pick an available task.');
		return ;
	}

	// Type of stats
	var STATS = ['totals', 'advanced'];

	// If Test is set, only get a few years
	var endYr = (isTest) ? 1982 : 2016;


	// Get generate our list of file paths
	var pathList = function(begPath) {
		return _.flatten(_.map(STATS, function (stat) {

			return _.map(_.range(1981,endYr), function (year) {
				var finalStr = [begPath,stat,'/leagues_NBA_',
								year,'_',stat,'.csv'].join('');

				return finalStr;
			});
		}));
	};


	// Divider ===================================

	//3
	if (task === '=BUILD') {
		console.log('*****BUILDING DATA*****');
		buildData(pathList('./data/output/'));
	}
	else if(task === '=CLEAN'){
		console.log('*****CLEANING DATA*****');
		cleanData(pathList('./data/csv/'));
	} else {
		console.log('*scratching head* how you got here?');
	}

})(process.argv[2], process.argv[3]);
