const request = require('superagent')
const fs = require('fs')
const Linode = require('./linode.js')
const path = require('path')

const dropInfra = async () => {
  console.info('[INFO] dropping all vms by #yacs-rcos tag')

  // fetch all vms
  vms = await Linode.node.list()

  // filter by containing tag yacs-rcos
  rcosVmIds = vms
    .filter(vm => vm.tags.includes('yacs-rcos'))
    .map(vm => vm.id)

  // drop all
  for (let id of rcosVmIds) {
    console.info(`[INFO] deleting vm: ${id}`)
    await Linode.node.remove(id)
  }
}
dropInfra()
