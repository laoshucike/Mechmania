
//组合
function C(arr, num){
    var r=[];
    (function f(t,a,n){
        if (n==0) return r.push(t);
        for (var i=0,l=a.length; i<=l-n; i++){
            f(t.concat(a[i]), a.slice(i+1), n-1);
        }
    })([],arr,num);
    return r;
}

//排列
function A(arr, num){
    var r=[];
    (function f(t,a,n){
        if (n==0) return r.push(t);
        for (var i=0,l=a.length; i<l; i++){
            f(t.concat(a[i]), a.slice(0,i).concat(a.slice(i+1)), n-1);
        }
    })([],arr,num);
    return r;
}

exports.do = () => {

  let guys = require('./const.js').guys
  guysNames = Object.keys(guys);
  dupGuysNames = guysNames.concat(guysNames.concat(guysNames))
  list = {'Archer' : 'Archer' ,
  'Assassin' : 'Assassin' ,
  'Druid' : 'Druid',
  'Enchanter' : 'Enchanter',
  'Paladin' : 'Paladin',
  'Sorcerer' : 'Sorcerer',
  'Warrior':'Warrior',
  'Wizard':'Wizard' }
  dupGuysNames = dupGuysNames.map(str => list[str])
  // allow dup
  Comb = C(dupGuysNames, 3);
  var UniqComb = [];


  Comb.forEach(comb => {
    UniqComb = UniqComb.filter(function (c) {
      c = c.sort((a,b) => a<b)
      comb = comb.sort((a,b) => a<b)
      return !(c[0] == comb[0] && c[1] == comb[1] && c[2] == comb[2]);
    })
    UniqComb.push(comb)
  })


  return UniqComb
}