const replaceTag = '###JSINJECTA###';
require('shelljs/global');
const fs = require('fs')
let execOut = (cmd) => exec(cmd, {async : false, silent : true}).stdout.split('\n').filter(s => s.length > 0)


exports.do = (base, team) => {
  var Injection = '[' + team.split('_').map(name => `{"CharacterName": "${name}}","ClassId": "${name}"}`) + ']'
  exec(`rm -rf ../clients/${team}`)
  exec(`cp -av ../clients/base ../clients/${team}`, {silent : true})
  
  lines = (execOut(`cat ../clients/${team}/client.py`))
  lines = lines.map(line => {
    return line.replace(replaceTag, Injection)
  })

  fs.writeFileSync(`../clients/${team}/client.py`, lines.join('\n'))
  return team + ' done!!'
}