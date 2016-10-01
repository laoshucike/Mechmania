require('shelljs/global');

exports.do = function (way1, way2) {
  var run = (cmd) => exec(cmd, {
    async:false,
    silent:true
  })
  var result = run(`cd ~/2code/Mechmania/ && python2 ./gamerunner.py -c ${way1}/ -c ${way2}/`)
  return {
    tie : (result.stdout.indexOf('Tie!') > -1),
    team1won : (result.stdout.indexOf('Team 1 Won') > -1),
    team2won : (result.stdout.indexOf('Team 2 Won') > -1),
    success : (result.stdout.indexOf('Game finished - writing log to file') > -1),
  }
}