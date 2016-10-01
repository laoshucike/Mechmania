require('shelljs/global');

exports.do = function () {
  var run = (cmd) => exec(cmd, {
    async:false,
    silent: true
  })
  run('cd ..')
  var result = run('python2 ./gamerunner.py')
  return (result.stdout.indexOf('Game finished - writing log to file') > -1)
}