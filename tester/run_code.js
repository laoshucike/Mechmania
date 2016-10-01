require('shelljs/global');

exports.do = function (way1, way2) {
  var run = (cmd) => exec(cmd, {
    async:false,
    silent:true
  })
  run('kill $(lsof -t -i:1337)')
  var result = run(`cd ~/2code/Mechmania/ && python2 ./gamerunner.py -c ${way1}/ -c ${way2}/`)
  return {
    stdout : (result.stdout),
    tie : (result.stdout.indexOf('Tie!') > -1),
    team1won : (result.stdout.indexOf(way1) > -1),
    team2won : (result.stdout.indexOf(way2) > -1),
    success : (result.stdout.indexOf('Game finished - writing log to file') > -1),
  }
}