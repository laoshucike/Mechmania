const replaceTag = '###JSINJECTA###';
const repalceNameTag = '####replacename####'
require('shelljs/global');
const fs = require('fs')
let execOut = (cmd) => exec(cmd, {async : false, silent : true}).stdout.split('\n').filter(s => s.length > 0)


exports.do = (base, team, prefix) => {
  if (!prefix) prefix = '';
  var Injection = '[' + team.split('_').map(name => `{"CharacterName": "${name}}","ClassId": "${name}"}`) + ']'
  exec(`rm -rf ../clients/${prefix + team}`)
  exec(`cp -av ../clients/${base} ../clients/${prefix + team}`, {silent : true})
  
  lines = (execOut(`cat ../clients/${prefix + team}/client.py`))
  lines = lines.map(line => {
    return line.replace(replaceTag, Injection).replace(repalceNameTag, `'${team}'`)
  })

  fs.writeFileSync(`../clients/${prefix + team}/client.py`, lines.join('\n'))
  return team + ' done!!'
}