const fs = require('fs');
let generate_zuhe = require('./generate_zuhe')
let generate_pycode = require('./generate_pycode')
let run_code = require('./run_code')
let guys = require('./const.js').guys
let ranking = require('./ranking')
let _ = require('underscore')
require('shelljs/global');

let log = (msg) => console.log('[!!!!!]  ' + msg)

let execOut = (cmd) => exec(cmd, {async : false, silent : true}).stdout.split('\n').filter(s => s.length > 0)

var simulate = (way1, way2, silent) => {
  R = run_code.do(way1, way2)
  if (R.success) {
    if (!silent)
    log(`simulate success with ${way1} ${way2}`)
  } else {
    if (!silent)
    log(`simulate fail with ${way1} ${way2}`)
  }
  return R
}



var newRanking = (feed) => {
  let stringFromArr = (arr) => arr.join('_')
  let ranking = {}

  if (!feed) {
    generate_zuhe.do().forEach((c) => {
      ranking[stringFromArr(c)] = 1000
    })
  } else {
    feed.forEach(teamArrange => {
       ranking[teamArrange] = 1000
    })
  }

  return ranking
}

var biggsetName = () => execOut('ls rankings').sort((a,b) => a < b)[0]
execOut('ls rankings').sort((a,b) => a < b)[0];
var read = () => {
  //var name = biggsetName()
  //log('reading ' + name)
  return JSON.parse(execOut('cat rankings/latest.json'))
}
var write = (rk) => {
  //var name = (parseInt(biggsetName().split('.json')[0]) + 1) + '.json'
  //log(name)
  fs.writeFileSync('rankings/latest.json', JSON.stringify(rk))
}




//process.stdout.write(JSON.stringify(newRanking()))
//fs.writeFileSync('rankings/2.json', JSON.stringify(newRanking()))

function playForXTimes(way1, way2, times) {
  i = times
  count1 = 0, tie=0, count2 = 0;
  while (i) {
    obj = simulate(way1, way2, true)
    if (!obj.success) {
      log(`not success status with ${way1} ${way2}`)
      //log(`from stdout${obj.stdout}`)
    }
    if (obj.tie) tie++;
    if (obj.team1won) count1 ++;
    if (obj.team2won) count2 ++;
    i--;
  }
  //console.log(`${count1}:${count2}`)
  return {
    first_win : count1 > count2,
    win_ratio : count1 > count2 ? count1 / times : count2 / times,
    success : obj.success,
  }
}
function generateAll() {
  Object.keys(newRanking()).forEach(comb => {
    log(generate_pycode.do('base', comb))
  })
}

//generateAll()

//t = new Date()
//console.log(playForXTimes('Warrior_Warrior_Assassin', 'Sorcerer_Druid_Druid', 10))

 //generateAll()
//console.log(Date.now() - t)


function doMatching (rankingObject) {
  var unwritten = 0;
  var latestRanking = rankingObject || read()


  while (true) {
    var players = _.sample(Object.keys(latestRanking),2 )
    var res = playForXTimes(players[0], players[1], 3)
    if (!res.success)
      continue;
    var rk = ranking({
      ranks : players.map(p => latestRanking[p]),
      scores : [res.first_win ? 1 : 0, res.first_win ? 0 : 1,],
      growth : [10, 10]
    });
    var oldRk = players.map(p => latestRanking[p])
    latestRanking[players[0]] += rk[0]
    latestRanking[players[1]] += rk[1]
    var newRk = players.map(p => latestRanking[p])

    log(`${players[0]} : ${oldRk[0]} -> ${newRk[0]}`)
    log(`${players[1]} : ${oldRk[1]} -> ${newRk[1]}`)

    unwritten ++;
    if (unwritten > 6) {
      write(latestRanking);
      log('writting.....');
      unwritten = 0;
    }
  }
}

doMatching()