const fs = require('fs')
const Linode = require('./linode.js')
const path = require('path')

SETTINGS = {
  SSH_PUB_KEY: process.env.SSH_PUB_KEY,
  SERVER_ROOT_PASS: process.env.SERVER_ROOT_PASS || "some_pass",
  BRANCH: process.env.BRANCH || "master",
  ACTIVE_SERVER_COUNT: Number(process.env.ACTIVE_SERVER_COUNT) || 3
}

const infraSync = async () => {

  console.info(`Deploying: ${SETTINGS.BRANCH}`)
  console.info('--- manage script ---')
  console.info('[INFO] updating #yacs-rcos script')

  script = await Linode.script.update(639784, {
    images: ["linode/ubuntu18.04"],
    label: 'yacs-rcos',
    is_public: false,
    script: fs.readFileSync(path.join(__dirname, './scripts/configure.sh'), 'utf8'),
    description: "Start YACS with some branch"
  })

  // ------------ VMS

  console.info('--- manage vm(s) ---')
  console.info('[INFO] fetching all #yacs-rcos vms')
  vms = await Linode.node.list()
  console.log(`[INFO] currently, ${vms.length} vms are running/active`)

  // fetch current to delete later
  rcosVmIds = vms
    .filter(vm => vm.tags.includes('yacs-rcos'))
    .sort((a,b) => Date(a.created) - Date(b.created)) // sort by date created, earliest created first
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
  let amountToRemove = (rcosVmIds.length + 1) - SETTINGS.ACTIVE_SERVER_COUNT // plus one since we just added one

  // after drop-all, no need to remove any so will be negative
  if (amountToRemove < 0) {
    amountToRemove = 0;
  }

  console.info(`[INFO] deleting old vm(s) by tag #yacs-rcos that surpass server allotment of ${SETTINGS.ACTIVE_SERVER_COUNT}`)
  console.info(`[INFO] amount to remove: ${amountToRemove}`)
  // rcosVmIds is sorted, this allows us to remove the oldest server(s)
  for (let i = 0; i < amountToRemove; i++) {
    console.info(`[INFO] deleting vm: ${rcosVmIds[i]}`)
    await Linode.node.remove(rcosVmIds[i])
  }

  // print ip
  // USED IN GITHUB ACTIONS PIPELINE TO SHOW MESSAGE IN PR
  // Changing it to HTTPS instead of HTTP
  console.log(`https://${info.ipv4[0]}`)

}
infraSync()
