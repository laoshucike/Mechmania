require('shelljs/global');

exports.do = function (way1, way2) {
  var run = (cmd) => exec(cmd, {
    async:false,
    silent:true
  })
  var result = run(`cd ~/2code/Mechmania/ && python2 ./gamerunner.py -c ${way1}/ -c ${way2}/`)
  return (result.stdout.indexOf('Game finished - writing log to file') > -1)
}