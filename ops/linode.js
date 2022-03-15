const request = require('superagent')
let Linode = {}

if (!process.env.LINODE_TOKEN) {
  console.error('env var LINODE_TOKEN is required');
}

LINODE_TOKEN = process.env.LINODE_TOKEN

Linode.node = {

  list: async () => {
    try {
      res = await request
        .get('https://api.linode.com/v4/linode/instances')
        .set('Authorization', `Bearer ${LINODE_TOKEN}`)
      return res.body.data
    } catch (e) {
      console.error(e);
      throw new Error(e)
    }
  },

  create: async (spec) => {
    try {
      res = await request
        .post('https://api.linode.com/v4/linode/instances')
        .set('Authorization', `Bearer ${LINODE_TOKEN}`)
        .send(spec)
      return res.body
    } catch (e) {
      console.error(e);
      throw new Error(e)
    }
  },

  remove: async (linodeId) => {
    try {
      res = await request
        .delete(`https://api.linode.com/v4/linode/instances/${linodeId}`)
        .set('Authorization', `Bearer ${LINODE_TOKEN}`)
      return res.body
    } catch (e) {
      console.error(e);
      throw new Error(e)
    }
  },
}

Linode.script = {

  list: async () => {
    try {
      res = await request
        .get('https://api.linode.com/v4/linode/stackscripts')
        .set('Authorization', `Bearer ${LINODE_TOKEN}`)
      return res.body.data
    } catch (e) {
      console.error(e);
      throw new Error(e)
    }
  },

  update: async (id, spec) => {
    try {
      res = await request
        .put(`https://api.linode.com/v4/linode/stackscripts/${id}`)
        .set('Authorization', `Bearer ${LINODE_TOKEN}`)
        .send(spec)
      return res.body
    } catch (e) {
      console.error(e);
      throw new Error(e)
    }
  },

  create: async (spec) => {
    try {
      res = await request
        .post('https://api.linode.com/v4/linode/stackscripts')
        .set('Authorization', `Bearer ${LINODE_TOKEN}`)
        .send(spec)
      return res.body
    } catch (e) {
      console.error(e);
      throw new Error(e)
    }
  },

  remove: async (id) => {
    try {
      res = await request
        .delete(`https://api.linode.com/v4/linode/stackscripts/${id}`)
        .set('Authorization', `Bearer ${LINODE_TOKEN}`)
      return res.body
    } catch (e) {
      console.error(e);
      throw new Error(e)
    }
  },
}

module.exports = Linode
