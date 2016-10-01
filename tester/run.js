const fs = require('fs');
let generate_zuhe = require('./generate_zuhe')
let generate_pycode = require('./generate_pycode')
let run_code = require('./run_code')
let guys = require('./const.js').guys
require('shelljs/global');

let log = (msg) => console.log('[!!!!!]  ' + msg)

let execOut = (cmd) => exec(cmd, {async : false, silent : true}).stdout.split('\n').filter(s => s.length > 0)

var simulate = (way1, way2) => {
  if (run_code.do(way1, way2)) {
    log(`simulate success with ${way1} ${way2}`)
  } else {
    log(`simulate fail with ${way1} ${way2}`)
  }
}



var newRanking = () => {
  let stringFromArr = (arr) => arr.join('_')
  let ranking = {}
  generate_zuhe.do().forEach((c) => {
    ranking[stringFromArr(c)] = 1000
  })
  return ranking
}

var biggsetName = () => execOut('ls rankings').sort((a,b) => a < b)[0]
execOut('ls rankings').sort((a,b) => a < b)[0];
var read = () => {
  var name = biggsetName()
  return JSON.parse(execOut('cat rankings/' + name))
}
var write = (rk) => {
  var name = (parseInt(biggsetName().split('.json')[0]) + 1) + '.json'
  fs.writeFileSync('rankings/' + name, JSON.stringify(rk))
}

//process.stdout.write(JSON.stringify(newRanking()))
//fs.writeFileSync('rankings/2.json', JSON.stringify(newRanking()))

simulate('default', 'default')
simulate('default', 'default2')
