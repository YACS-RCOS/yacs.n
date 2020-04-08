const request = require('superagent')
const fs = require('fs')
const Linode = require('./linode.js')
const path = require('path')

SETTINGS = {
  SSH_PUB_KEY: process.env.SSH_PUB_KEY,
  SERVER_ROOT_PASS: process.env.SERVER_ROOT_PASS || "some_pass",
  BRANCH: process.env.BRANCH || "master"
}

const infraSync = async () => {

  console.info(`Deploying Branch: ${SETTINGS.BRANCH}`)
  console.info('--- manage script ---')
  console.info('[INFO] updating #yacs-rcos scripts')

  script = await Linode.script.update(639784, {
    images: ["linode/ubuntu18.04"],
    label: 'yacs-rcos',
    is_public: false,
    script: fs.readFileSync(path.join(__dirname, './scripts/configure.sh'), 'utf8'),
    description: "Start YACS with some branch"
  })

  // ------------ VMS

  console.info('--- manage vm ---')
  console.info('[INFO] fetching all #yacs-rcos vms')
  vms = await Linode.node.list()

  // fetch current to delete later
  rcosVmIds = vms
    .filter(vm => vm.tags.includes('yacs-rcos'))
    .map(vm => vm.id)

  // create a new vm
  console.info('[INFO] creating #yacs-rcos node')
  info = await Linode.node.create({
    image: "linode/ubuntu18.04", // or "linode/ubuntu16.04lts"
    root_pass: SETTINGS.SERVER_ROOT_PASS,
    authorized_keys: [ SETTINGS.SSH_PUB_KEY ],
    type: "g6-nanode-1",
    region: "us-east",
    tags: ["yacs-rcos"],
    stackscript_id: script.id,
    stackscript_data: {
      branch: SETTINGS.BRANCH
    }
  })

  // delete existing vm(s) after creation
  console.info('[INFO] deleting old vm(s) by tag #yacs-rcos')
  for (linodeId of rcosVmIds) {
    console.info(`[INFO] deleting vm: ${linodeId}`)
    await Linode.node.remove(linodeId)
  }

  // print ip for use.
  // USED IN GITHUB ACTIONS PIPELINE TO SHOW MESSAGE IN PR
  // DO NOT REFORMAT
  console.log(`http://${info.ipv4[0]}/`)

}
infraSync()
