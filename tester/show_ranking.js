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

var newRanking = (feed) => {
  let stringFromArr = (arr) => arr.join('_')
  let ranking = {}

  if (!feed) {
    generate_zuhe.do().forEach((c) => {
      ranking[stringFromArr(c)] = 1000
    })
  } else {
    feed.forEach(teamArrange => {
        //teamArrange : 'Druid_Paladin_Sorcerer'

    })
  }

  return ranking
}

var biggsetName = () => execOut('ls rankings').sort((a,b) => a < b)[0]
execOut('ls rankings').sort((a,b) => a < b)[0];

var fname = process.argv[process.argv.length - 1]


var read = () => {
  //var name = biggsetName()
  //log('reading ' + name)
  return JSON.parse(execOut('cat rankings/' + fname))
}
var write = (rk) => {
  //var name = (parseInt(biggsetName().split('.json')[0]) + 1) + '.json'
  //log(name)
  fs.writeFileSync('rankings/' + fname, JSON.stringify(rk))
}


var latestRanking = read()
var unwritten = 0;

var win = 0, lose = 0;

var rk = [];

Object.keys(latestRanking).forEach(k => {
  rk.push({
    name : k,
    elo : latestRanking[k],
  })
})


rk = rk.sort((a, b) => {
  return a.elo < b.elo ? 1 : -1
})

console.log(rk)

/*
  unwritten ++;
  if (unwritten > 10) {
    //write(latestRanking);
    log('writting.....');
    unwritten = 0;
  }*/
