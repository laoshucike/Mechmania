let generate_zuhe = require('./generate_zuhe')
let generate_pycode = require('./generate_pycode')
let run_code = require('./run_code')


let log = (msg) => console.log('[!!!!!]  ' + msg)

if (run_code.do()) {
  log('simulate success')
}