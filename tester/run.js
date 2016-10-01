const fs = require('fs');
let generate_zuhe = require('./generate_zuhe')
let generate_pycode = require('./generate_pycode')
let run_code = require('./run_code')
let guys = require('./const.js').guys
require('shelljs/global');

let log = (msg) => console.log('[!!!!!]  ' + msg)

let execOut = (cmd) => exec(cmd, {async : false, silent : true}).stdout.split('\n').filter(s => s.length > 0)

var simulate = (way1, way2) => {
  R = run_code.do(way1, way2)
  if (R.success) {
    log(`simulate success with ${way1} ${way2}`)
  } else {
    log(`simulate fail with ${way1} ${way2}`)
  }
  return R
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

/*

// run with random stratage


i = 20
count1 = 0, tie=0, count2 = 0;
while (i) {
  obj = simulate('default', 'Enchanter_Sorcerer_Warrior')
  if (obj.tie) tie++;
  if (obj.team1won) count1 ++;
  if (obj.team2won) count2 ++;
  i--;
}
log (`${count1}/${tie}/${count2}`)




*/

Object.keys(newRanking()).forEach(comb => {
  log(generate_pycode.do('base', comb))
})

