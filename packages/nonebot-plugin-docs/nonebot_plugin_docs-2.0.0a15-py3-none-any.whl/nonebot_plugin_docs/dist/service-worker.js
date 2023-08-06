/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a10/advanced/export-and-require.html",
    "revision": "edd55671c8bed375653fde1e36443741"
  },
  {
    "url": "2.0.0a10/advanced/index.html",
    "revision": "99213193b558b73c50e20a67a1f79b99"
  },
  {
    "url": "2.0.0a10/advanced/overloaded-handlers.html",
    "revision": "b5219f235329c564d302aa514c5029a7"
  },
  {
    "url": "2.0.0a10/advanced/permission.html",
    "revision": "b0d1b4bbd41ff6b435ef6ca42dd15a3b"
  },
  {
    "url": "2.0.0a10/advanced/publish-plugin.html",
    "revision": "937df2933231a56b7ae0d8ccb1974610"
  },
  {
    "url": "2.0.0a10/advanced/runtime-hook.html",
    "revision": "02099a4d82b4694eb2ae8a820ba3f916"
  },
  {
    "url": "2.0.0a10/advanced/scheduler.html",
    "revision": "01049fb7eceaa2a8bfe453e093c86054"
  },
  {
    "url": "2.0.0a10/api/adapters/cqhttp.html",
    "revision": "35cad388cc8c0b38e3c97ce874bc938a"
  },
  {
    "url": "2.0.0a10/api/adapters/ding.html",
    "revision": "7a9c536164a19caefe823c59abe63aed"
  },
  {
    "url": "2.0.0a10/api/adapters/index.html",
    "revision": "f29f1191499cd60c43d8970ab59dd7ff"
  },
  {
    "url": "2.0.0a10/api/adapters/mirai.html",
    "revision": "01ec0104fab06547ff99f803aa79b3a8"
  },
  {
    "url": "2.0.0a10/api/config.html",
    "revision": "54dbd0a201613f21bac781bf6f9c1c7e"
  },
  {
    "url": "2.0.0a10/api/drivers/fastapi.html",
    "revision": "23f42ac97026f7d87ea47f88f11b4abf"
  },
  {
    "url": "2.0.0a10/api/drivers/index.html",
    "revision": "94033a5e6c18d0b2032fcf6e3dcc7df1"
  },
  {
    "url": "2.0.0a10/api/drivers/quart.html",
    "revision": "778b8113ef4ad4e77de42fa676c2eba3"
  },
  {
    "url": "2.0.0a10/api/exception.html",
    "revision": "63087775b1f0d753cf20317c333c9291"
  },
  {
    "url": "2.0.0a10/api/index.html",
    "revision": "0cd95341e0517fbb3625871aae24c21b"
  },
  {
    "url": "2.0.0a10/api/log.html",
    "revision": "21fedc121781cfe3aec865e80caa18f1"
  },
  {
    "url": "2.0.0a10/api/matcher.html",
    "revision": "9e0bad9bf0f66ce7cd2c9a479fa7856a"
  },
  {
    "url": "2.0.0a10/api/message.html",
    "revision": "1c180481f040149f0b1539ce7da947d2"
  },
  {
    "url": "2.0.0a10/api/nonebot.html",
    "revision": "93716496522936ce8c0da986961f07e9"
  },
  {
    "url": "2.0.0a10/api/permission.html",
    "revision": "6bd3fd6234460ac88f48a541f7c4e54c"
  },
  {
    "url": "2.0.0a10/api/plugin.html",
    "revision": "bb2d1597b7818af34a4a97f26d0f0b63"
  },
  {
    "url": "2.0.0a10/api/rule.html",
    "revision": "4a634a5d0e73e44d383f2f7cf4c08243"
  },
  {
    "url": "2.0.0a10/api/typing.html",
    "revision": "9f9776d2503686c80498dbd0413e1db2"
  },
  {
    "url": "2.0.0a10/api/utils.html",
    "revision": "c1316793c00888a36ce99e3a5cef2609"
  },
  {
    "url": "2.0.0a10/guide/basic-configuration.html",
    "revision": "f86d7e98fb3973fa48970bdd9357fa93"
  },
  {
    "url": "2.0.0a10/guide/cqhttp-guide.html",
    "revision": "39714cbc577fb208320d2fdf60105014"
  },
  {
    "url": "2.0.0a10/guide/creating-a-handler.html",
    "revision": "6bcda31ea95d09018c6db6a5adacbd7b"
  },
  {
    "url": "2.0.0a10/guide/creating-a-matcher.html",
    "revision": "d8095c9c0c36a0b2e2e1b321295383e9"
  },
  {
    "url": "2.0.0a10/guide/creating-a-plugin.html",
    "revision": "44a82ddb23f05a4a37d30d851e56f0a1"
  },
  {
    "url": "2.0.0a10/guide/creating-a-project.html",
    "revision": "0a4a9ab75f5922ad56eab2202a7bce80"
  },
  {
    "url": "2.0.0a10/guide/ding-guide.html",
    "revision": "cc1591164a1c75cae3957872412cd14c"
  },
  {
    "url": "2.0.0a10/guide/end-or-start.html",
    "revision": "5f5441ae8a4cacbdb9167b108fae80a7"
  },
  {
    "url": "2.0.0a10/guide/getting-started.html",
    "revision": "3846dde3415519a5ede14cc7dd765912"
  },
  {
    "url": "2.0.0a10/guide/index.html",
    "revision": "59d8164d15aec1fdb116c9d98417f66e"
  },
  {
    "url": "2.0.0a10/guide/installation.html",
    "revision": "04a6996ecc51d5d12abdff8c81188874"
  },
  {
    "url": "2.0.0a10/guide/loading-a-plugin.html",
    "revision": "54d6182dae54f0bfa8999f06ebcb14f1"
  },
  {
    "url": "2.0.0a10/guide/mirai-guide.html",
    "revision": "7edd4f8ad57ff6036cca954dc8b7edf9"
  },
  {
    "url": "2.0.0a10/index.html",
    "revision": "10212dc4e16e46b397c94d43ad808bbd"
  },
  {
    "url": "2.0.0a13.post1/advanced/export-and-require.html",
    "revision": "c9a099091efa47d77ba8d7b9a45334bd"
  },
  {
    "url": "2.0.0a13.post1/advanced/index.html",
    "revision": "2285be9ab6e445bcdf4482708b9fbfd7"
  },
  {
    "url": "2.0.0a13.post1/advanced/overloaded-handlers.html",
    "revision": "0ca8f6f3f808b4c0c6ed02003f02c5f9"
  },
  {
    "url": "2.0.0a13.post1/advanced/permission.html",
    "revision": "23dccf67dbd8f6d127f83cb9a1aba2ab"
  },
  {
    "url": "2.0.0a13.post1/advanced/publish-plugin.html",
    "revision": "8350afa5eacca8766c8d55375b1b45b5"
  },
  {
    "url": "2.0.0a13.post1/advanced/runtime-hook.html",
    "revision": "c785a0a38083c277ad6191102909d0b9"
  },
  {
    "url": "2.0.0a13.post1/advanced/scheduler.html",
    "revision": "fbd2a7b3bfb474ced6633fcb340392a6"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/cqhttp.html",
    "revision": "07b835b9f5dbdbcc09557841bbe61ce3"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/ding.html",
    "revision": "04606d78a06b4fb9d7a9f701854e26be"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/index.html",
    "revision": "8fee8433f4e96226158c28097d50089d"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/mirai.html",
    "revision": "979c041c93c435d732c0d968fa86a39d"
  },
  {
    "url": "2.0.0a13.post1/api/config.html",
    "revision": "d88aec6555db3cd1c146e202fd50ea37"
  },
  {
    "url": "2.0.0a13.post1/api/drivers/fastapi.html",
    "revision": "086b3f5481f05d69b2ae6fd55f1a1fac"
  },
  {
    "url": "2.0.0a13.post1/api/drivers/index.html",
    "revision": "ba956759ee11927a452d531ac4ca59b0"
  },
  {
    "url": "2.0.0a13.post1/api/drivers/quart.html",
    "revision": "be20c5d5064fa2f2718048c4eceeedb8"
  },
  {
    "url": "2.0.0a13.post1/api/exception.html",
    "revision": "a064ced1097c30d17df58172a624cf95"
  },
  {
    "url": "2.0.0a13.post1/api/handler.html",
    "revision": "d8acaec47136df95011d81467a1d57df"
  },
  {
    "url": "2.0.0a13.post1/api/index.html",
    "revision": "2c42d038bba3852ce3bf3cafe557219b"
  },
  {
    "url": "2.0.0a13.post1/api/log.html",
    "revision": "c2ff41588a3dc99e3825193649610187"
  },
  {
    "url": "2.0.0a13.post1/api/matcher.html",
    "revision": "4d281208872a2634788c4071f43a4783"
  },
  {
    "url": "2.0.0a13.post1/api/message.html",
    "revision": "c423f9f4b574107f43be5d2f5785512e"
  },
  {
    "url": "2.0.0a13.post1/api/nonebot.html",
    "revision": "9f1f3a542d4ddb1fffe92668ac2e2e25"
  },
  {
    "url": "2.0.0a13.post1/api/permission.html",
    "revision": "08afa2f4f445c3495b62140d8fe588d1"
  },
  {
    "url": "2.0.0a13.post1/api/plugin.html",
    "revision": "c7afea95b79cb1fe43fa253f5e388d43"
  },
  {
    "url": "2.0.0a13.post1/api/rule.html",
    "revision": "3934566578a337c4563c7aecddbb6594"
  },
  {
    "url": "2.0.0a13.post1/api/typing.html",
    "revision": "7de0afa8e080b647e075695cba1853c9"
  },
  {
    "url": "2.0.0a13.post1/api/utils.html",
    "revision": "729dd9415100ab84b3da03c9ad17be6f"
  },
  {
    "url": "2.0.0a13.post1/guide/basic-configuration.html",
    "revision": "f470a229a1f50edde9c95ebb767f8e6c"
  },
  {
    "url": "2.0.0a13.post1/guide/cqhttp-guide.html",
    "revision": "fd4e8c6cb68abf0674e6c4b9b0cb8468"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-handler.html",
    "revision": "70d599749846b85cd866bf441e7a65d2"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-matcher.html",
    "revision": "935ba668e9bba53e1db562dbdede737e"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-plugin.html",
    "revision": "e24ebc17e497049471961e194022e3fe"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-project.html",
    "revision": "b4a86081a93daa27594cb758384395a9"
  },
  {
    "url": "2.0.0a13.post1/guide/ding-guide.html",
    "revision": "f85ebd9c6f190eb1b5b5150ffbf25f08"
  },
  {
    "url": "2.0.0a13.post1/guide/end-or-start.html",
    "revision": "24ef436bbcba1ab8f8095b0e509729d8"
  },
  {
    "url": "2.0.0a13.post1/guide/getting-started.html",
    "revision": "42e1a4241a35f7e0cacc5316c050a955"
  },
  {
    "url": "2.0.0a13.post1/guide/index.html",
    "revision": "2041488384ef90c5ba76675fec71ac5c"
  },
  {
    "url": "2.0.0a13.post1/guide/installation.html",
    "revision": "fc8d3bb00d95590a8fa96794b34204b4"
  },
  {
    "url": "2.0.0a13.post1/guide/loading-a-plugin.html",
    "revision": "d44e75f62d63f2ceaae2c77c52b0dd37"
  },
  {
    "url": "2.0.0a13.post1/guide/mirai-guide.html",
    "revision": "7dbbd3c09825ee073acbf33f24c476b8"
  },
  {
    "url": "2.0.0a13.post1/index.html",
    "revision": "a377fdc7ab77c8b94ee960babda28a2f"
  },
  {
    "url": "2.0.0a7/advanced/export-and-require.html",
    "revision": "b0ae8f6601ba88e8ca5043b096139788"
  },
  {
    "url": "2.0.0a7/advanced/index.html",
    "revision": "18d032de4e04a96ab80c8b192bffd06b"
  },
  {
    "url": "2.0.0a7/advanced/permission.html",
    "revision": "0164b6fb4a6767f53b421f6be7b516b2"
  },
  {
    "url": "2.0.0a7/advanced/publish-plugin.html",
    "revision": "6ab111dab8d6b8601bf84e21d22b041a"
  },
  {
    "url": "2.0.0a7/advanced/runtime-hook.html",
    "revision": "08c327d37a5cfd665be9e11df4070fed"
  },
  {
    "url": "2.0.0a7/advanced/scheduler.html",
    "revision": "276a9fc8a8560e86edf4c0c91a5cd218"
  },
  {
    "url": "2.0.0a7/api/adapters/cqhttp.html",
    "revision": "189046bf55cdcb81bf35098637f32286"
  },
  {
    "url": "2.0.0a7/api/adapters/ding.html",
    "revision": "662f18d7d864e39f987f8a80e42366a9"
  },
  {
    "url": "2.0.0a7/api/adapters/index.html",
    "revision": "6c918334b76a7536c3b7a414024a4ece"
  },
  {
    "url": "2.0.0a7/api/config.html",
    "revision": "8765a26ec9127973daaf090b24e980e7"
  },
  {
    "url": "2.0.0a7/api/drivers/fastapi.html",
    "revision": "6e90e67583530c0f3a6c9f73aef66f43"
  },
  {
    "url": "2.0.0a7/api/drivers/index.html",
    "revision": "86c139e134c19b4de6842166c1d5e10d"
  },
  {
    "url": "2.0.0a7/api/exception.html",
    "revision": "88cb07aaaaa57d78a483a774f628ed5d"
  },
  {
    "url": "2.0.0a7/api/index.html",
    "revision": "029abd11124883f507433918c4e6ccb2"
  },
  {
    "url": "2.0.0a7/api/log.html",
    "revision": "14e81c00f9796f5bdbd857920cb5915a"
  },
  {
    "url": "2.0.0a7/api/matcher.html",
    "revision": "4d37a154e5718642c94901eb24d65297"
  },
  {
    "url": "2.0.0a7/api/message.html",
    "revision": "bba9dbe298cda4a3433c6ee1628ac921"
  },
  {
    "url": "2.0.0a7/api/nonebot.html",
    "revision": "a273de844d3d317434a93df5d2112db0"
  },
  {
    "url": "2.0.0a7/api/permission.html",
    "revision": "25384a4d140b9e0c74c9cd4769b2bca6"
  },
  {
    "url": "2.0.0a7/api/plugin.html",
    "revision": "b8f26d325e6f3da27dddc44a77c08726"
  },
  {
    "url": "2.0.0a7/api/rule.html",
    "revision": "21600f5fd37c59a3c1d655b8aa307ea1"
  },
  {
    "url": "2.0.0a7/api/typing.html",
    "revision": "e2ec28f804a6f1597075e3f0af72d8f0"
  },
  {
    "url": "2.0.0a7/api/utils.html",
    "revision": "812673ada5d8ff3c6968177e7e4b76c2"
  },
  {
    "url": "2.0.0a7/guide/basic-configuration.html",
    "revision": "cb93d682393f496f26e1db7aee681ab1"
  },
  {
    "url": "2.0.0a7/guide/creating-a-handler.html",
    "revision": "8377278161805231647d7b220ddb80d6"
  },
  {
    "url": "2.0.0a7/guide/creating-a-matcher.html",
    "revision": "424f39c032a0fa750c7bb1e7ffa3745e"
  },
  {
    "url": "2.0.0a7/guide/creating-a-plugin.html",
    "revision": "8fdda5cb5d2e165d82acf7528e15bce4"
  },
  {
    "url": "2.0.0a7/guide/creating-a-project.html",
    "revision": "6dad3dc5e5b7db934495656f4a3555f1"
  },
  {
    "url": "2.0.0a7/guide/end-or-start.html",
    "revision": "b36cebf4c06627cec1dbab261609b454"
  },
  {
    "url": "2.0.0a7/guide/getting-started.html",
    "revision": "1ae96ebd15aaec13c1f1601e1bfc89d0"
  },
  {
    "url": "2.0.0a7/guide/index.html",
    "revision": "4a2d8b73ca8b2fd37e283447ebaf606a"
  },
  {
    "url": "2.0.0a7/guide/installation.html",
    "revision": "8ce661096b2495c64b7aa5c319ae68a1"
  },
  {
    "url": "2.0.0a7/guide/loading-a-plugin.html",
    "revision": "50af6567f1c2903ac084c7852974b218"
  },
  {
    "url": "2.0.0a7/index.html",
    "revision": "7ee3202dc01208d88256ffdf291a1d71"
  },
  {
    "url": "2.0.0a8.post2/advanced/export-and-require.html",
    "revision": "e72f499c22e8b71008ae4b2684b913db"
  },
  {
    "url": "2.0.0a8.post2/advanced/index.html",
    "revision": "5668aa12f2dee0bb8154128b78f89e1f"
  },
  {
    "url": "2.0.0a8.post2/advanced/overloaded-handlers.html",
    "revision": "6a3f489d683befe432a7f1a83cdee998"
  },
  {
    "url": "2.0.0a8.post2/advanced/permission.html",
    "revision": "bda6e0e48ac7bcac579ba3fabab0fa92"
  },
  {
    "url": "2.0.0a8.post2/advanced/publish-plugin.html",
    "revision": "cd2f550917b1e4ed064d3bbffe206676"
  },
  {
    "url": "2.0.0a8.post2/advanced/runtime-hook.html",
    "revision": "471f464ff2df63f9827dbea9d5605e18"
  },
  {
    "url": "2.0.0a8.post2/advanced/scheduler.html",
    "revision": "c27336c37ac27d15a30f5f9ed3766c6c"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/cqhttp.html",
    "revision": "e324505078724ee771a1c4f74f9d1eee"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/ding.html",
    "revision": "d94716a449151709d1678f50bd3d4ce6"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/index.html",
    "revision": "0c0bb44ade77f76b4621fff81e455648"
  },
  {
    "url": "2.0.0a8.post2/api/config.html",
    "revision": "45a5efc0ccdf699a0228120e23d705a6"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/fastapi.html",
    "revision": "08cfc882fe45f84671201f0b120279f9"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/index.html",
    "revision": "766ea0fe87b579334539a26458d0999f"
  },
  {
    "url": "2.0.0a8.post2/api/exception.html",
    "revision": "d07874c85e99e6acc02a3eff828010f7"
  },
  {
    "url": "2.0.0a8.post2/api/index.html",
    "revision": "b7da1fbaa6143fb6bf4af457b4404a87"
  },
  {
    "url": "2.0.0a8.post2/api/log.html",
    "revision": "6f56c1d630f5750194e02abb3ab70cce"
  },
  {
    "url": "2.0.0a8.post2/api/matcher.html",
    "revision": "d1ffb2321c0bb723e239c02d93d129e5"
  },
  {
    "url": "2.0.0a8.post2/api/message.html",
    "revision": "fc49a07238042b9f2ad2e790badae09f"
  },
  {
    "url": "2.0.0a8.post2/api/nonebot.html",
    "revision": "903f981c94d133caac80474f0193a4f2"
  },
  {
    "url": "2.0.0a8.post2/api/permission.html",
    "revision": "446aa361d306cdfd52a06a836548f828"
  },
  {
    "url": "2.0.0a8.post2/api/plugin.html",
    "revision": "3f3a1c8063786e541a588b821edc61c4"
  },
  {
    "url": "2.0.0a8.post2/api/rule.html",
    "revision": "2afaa4aa9d8b6ca4647af09159877d29"
  },
  {
    "url": "2.0.0a8.post2/api/typing.html",
    "revision": "f512a1bce88e06a25bfb46c7a9ee34d6"
  },
  {
    "url": "2.0.0a8.post2/api/utils.html",
    "revision": "565471f6d95de5db595c90d9692c3b29"
  },
  {
    "url": "2.0.0a8.post2/guide/basic-configuration.html",
    "revision": "0b168a7deb6d062e938cb2bc0e14f63f"
  },
  {
    "url": "2.0.0a8.post2/guide/cqhttp-guide.html",
    "revision": "41e411ae33ac81e4ecd9b5f0753e0562"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-handler.html",
    "revision": "3f2d613a99bcff3355779261d311a2ae"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-matcher.html",
    "revision": "f0c8540b039716cf8757473ab3520425"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-plugin.html",
    "revision": "ac09d8ab9a4c7d35a924c555bdf03faf"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-project.html",
    "revision": "36c608a5f32836daf9ff080d6428528a"
  },
  {
    "url": "2.0.0a8.post2/guide/ding-guide.html",
    "revision": "4ed0265336c60e24a9a66811fdb40ebc"
  },
  {
    "url": "2.0.0a8.post2/guide/end-or-start.html",
    "revision": "6e1ed7599b8fbd9fbf07d6ca35b67f47"
  },
  {
    "url": "2.0.0a8.post2/guide/getting-started.html",
    "revision": "a1cc58a596d448b9cb97a668a6b2f0e1"
  },
  {
    "url": "2.0.0a8.post2/guide/index.html",
    "revision": "cde859bdc8ae1612237946cce7b620e8"
  },
  {
    "url": "2.0.0a8.post2/guide/installation.html",
    "revision": "397a5294beee0117f0c1a9ec08564603"
  },
  {
    "url": "2.0.0a8.post2/guide/loading-a-plugin.html",
    "revision": "6a8b0c3d11c24cb66e1f578a2d7f94cd"
  },
  {
    "url": "2.0.0a8.post2/index.html",
    "revision": "5346c69c982f2b2e9c12cc1b4fff1f50"
  },
  {
    "url": "404.html",
    "revision": "83dfbabbd8acfee608169cc3aaf14081"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "38255f47857760b7edef924c57a7e18e"
  },
  {
    "url": "advanced/index.html",
    "revision": "20a1547afa5067bff1d07258c8e73da8"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "40fbc08de6d44fa430fb04c4e0eb82f9"
  },
  {
    "url": "advanced/permission.html",
    "revision": "d4267b31b06df816293fb76a48e5cd5f"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "e2b415398578e79e0e66f24facbe531e"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "68b2dc0a56225d73f373eacc72f784b4"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "02eaf949bd2679dbc1dfe316af216d27"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "13cf9fd4ff51dcd4ee562adaea631360"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "07986615b6c7d0aefb05a7b859366977"
  },
  {
    "url": "api/adapters/feishu.html",
    "revision": "68f51b9c750885a0b5b9b0281f811abc"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "46c5c36a8716174900b450784afaaa9e"
  },
  {
    "url": "api/adapters/mirai.html",
    "revision": "d105e14c8b021452d57cba66eb5b04c9"
  },
  {
    "url": "api/config.html",
    "revision": "87ca3f90bfbbdc37f0644967d37f4f9e"
  },
  {
    "url": "api/drivers/aiohttp.html",
    "revision": "fb26ca9f7f0bc8222f08dd5a82549452"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "f32900a3b375e00e1d6cdaf366902ec1"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "d1dee09ede2afc94d78a3d2f1c1031e9"
  },
  {
    "url": "api/drivers/quart.html",
    "revision": "5d45881bc9682e9f671c1394ec3f0e02"
  },
  {
    "url": "api/exception.html",
    "revision": "9503e98baf6a56593dece44e0944f515"
  },
  {
    "url": "api/handler.html",
    "revision": "c6491c668b285cf1a5cc1c3bc061fc1b"
  },
  {
    "url": "api/index.html",
    "revision": "4ebbe536e52f6dee7633e5f89d3077a8"
  },
  {
    "url": "api/log.html",
    "revision": "08cd24bcee44971ddb47b73e3a4a18e6"
  },
  {
    "url": "api/matcher.html",
    "revision": "354b85409c2cdb6fd9438b22d66117cf"
  },
  {
    "url": "api/message.html",
    "revision": "8d9178acaebe3e23558df69699ac8692"
  },
  {
    "url": "api/nonebot.html",
    "revision": "3c7cfaf81ea0cad52b4ecd454fcf330d"
  },
  {
    "url": "api/permission.html",
    "revision": "2573b183e77e13bb8041604f7eb06a29"
  },
  {
    "url": "api/plugin.html",
    "revision": "9eefdf50a03c2ac1d911d89bd0baa6b5"
  },
  {
    "url": "api/rule.html",
    "revision": "e870b79ffe86e52016492c7639bb8b09"
  },
  {
    "url": "api/typing.html",
    "revision": "dcf0b706a978dc3e4c1342f05f6e175c"
  },
  {
    "url": "api/utils.html",
    "revision": "cae96143b8c3ed5b6041ffdee54365b8"
  },
  {
    "url": "assets/css/0.styles.92d96405.css",
    "revision": "5a3d1d298d6ccc32ea2699b83042f28b"
  },
  {
    "url": "assets/img/Handle-Event.1e964e39.png",
    "revision": "1e964e39a1e302bc36072da2ffe9f509"
  },
  {
    "url": "assets/img/jiaqian.9b09040e.png",
    "revision": "9b09040ed4e5e35000247aa00e6dceac"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/img/webhook.479198ed.png",
    "revision": "479198ed677c8ba4bbdf72d0a60497c9"
  },
  {
    "url": "assets/js/1.8e2cffa6.js",
    "revision": "6161217f3277108ab73e1b88c22f8180"
  },
  {
    "url": "assets/js/10.ff920d22.js",
    "revision": "2cadad26f9b8de2d7989e6c4326079b3"
  },
  {
    "url": "assets/js/100.5ba754f1.js",
    "revision": "5734bcb39a3ab218d1a1cd0dfea2080a"
  },
  {
    "url": "assets/js/101.a609c170.js",
    "revision": "f8d71cbb2284ba7e81142dce84cb6eee"
  },
  {
    "url": "assets/js/102.dea855ef.js",
    "revision": "e90ce5b9904ce08ebda166f71a656cc1"
  },
  {
    "url": "assets/js/103.d63c28f8.js",
    "revision": "0684551703a5794be1677aeb313b751e"
  },
  {
    "url": "assets/js/104.1aedd497.js",
    "revision": "a1b1cf3544abc3f44e393d4811d1bfd9"
  },
  {
    "url": "assets/js/105.e6f285da.js",
    "revision": "ac7d3034aedc479bde1871755fdd2b7c"
  },
  {
    "url": "assets/js/106.807eff0c.js",
    "revision": "39bad748ba86322a0bf7d0f53d735cd7"
  },
  {
    "url": "assets/js/107.534ad15a.js",
    "revision": "13aba9db9d9d60efa355f9e31c5a0bdb"
  },
  {
    "url": "assets/js/108.28089def.js",
    "revision": "e08d372118f29d5a166eb2bddd762413"
  },
  {
    "url": "assets/js/109.d958d0dc.js",
    "revision": "5257dee72d93b5308bcbbfd14f7ac6f3"
  },
  {
    "url": "assets/js/11.e968b61d.js",
    "revision": "59e37d04c569e1808cf4ba6b05317fed"
  },
  {
    "url": "assets/js/110.af945857.js",
    "revision": "6700b71e555b10709c5f524960beaf01"
  },
  {
    "url": "assets/js/111.3311abb1.js",
    "revision": "962d12d754c1f9d7a3cee105772419c0"
  },
  {
    "url": "assets/js/112.015664b1.js",
    "revision": "b9c259ef441194ca7363d62d7118e604"
  },
  {
    "url": "assets/js/113.f5bede10.js",
    "revision": "bd7d48bb305afc16e1d12a0a35cb469f"
  },
  {
    "url": "assets/js/114.88b75277.js",
    "revision": "e08a06769951609ba79401c73e0d955c"
  },
  {
    "url": "assets/js/115.978c7e83.js",
    "revision": "263f4d36f98a499ed3cc4c05e0786196"
  },
  {
    "url": "assets/js/116.c6f32ae7.js",
    "revision": "34111df6c41f5c376d7e6c46c73ac826"
  },
  {
    "url": "assets/js/117.9e5b4274.js",
    "revision": "76c1451e112e41887a967b973be76d2f"
  },
  {
    "url": "assets/js/118.25086f31.js",
    "revision": "d425c6e7b2190e9fbd2fb547bc3ccb81"
  },
  {
    "url": "assets/js/119.0a41aac2.js",
    "revision": "3c4d080973d971b8155de339a1049f17"
  },
  {
    "url": "assets/js/12.d86967eb.js",
    "revision": "a099cf27d806101d8214fae0134e9f31"
  },
  {
    "url": "assets/js/120.e073a4c2.js",
    "revision": "69b9a725ccb4ec63fab7b6880ba942c5"
  },
  {
    "url": "assets/js/121.a0e0e354.js",
    "revision": "9efe06db8a3e3aa4e93ebac75614b2be"
  },
  {
    "url": "assets/js/122.e80f540b.js",
    "revision": "7a358687bae23d05c78025d3d6a6176b"
  },
  {
    "url": "assets/js/123.681870d6.js",
    "revision": "f64d1879812ca3e1af4627bfdb716536"
  },
  {
    "url": "assets/js/124.7c0cb28d.js",
    "revision": "04a0554ab3fbeac294f99a0b997360ab"
  },
  {
    "url": "assets/js/125.f014a98c.js",
    "revision": "891bfc46a40fe081ff1b0c3ccac90151"
  },
  {
    "url": "assets/js/126.fb5c1bee.js",
    "revision": "6fe85c4be6ec68edc51f5fd565361f39"
  },
  {
    "url": "assets/js/127.92e7e608.js",
    "revision": "27844418a66cb802d9a12022088958b4"
  },
  {
    "url": "assets/js/128.f1536520.js",
    "revision": "e9a181eda845210b750714b7310dd04c"
  },
  {
    "url": "assets/js/129.9a641220.js",
    "revision": "62548af7b4bbd67ec26dc992797884e3"
  },
  {
    "url": "assets/js/13.8c271a1e.js",
    "revision": "393280a57a51bfedf7108a096475efab"
  },
  {
    "url": "assets/js/130.9893672c.js",
    "revision": "9287e6fdc81d98e6c780b1218695a0bc"
  },
  {
    "url": "assets/js/131.ccb020c4.js",
    "revision": "6901ccead2b52724a14c61213956cdbf"
  },
  {
    "url": "assets/js/132.2bbdc3c9.js",
    "revision": "13791760d5ba947014b9c3c670ffb14f"
  },
  {
    "url": "assets/js/133.52e90cf6.js",
    "revision": "0b033d272264b935321d88eec7710fee"
  },
  {
    "url": "assets/js/134.ed497cc6.js",
    "revision": "acfe0d7ada631101996dd26f7ac7162a"
  },
  {
    "url": "assets/js/135.f9d3b858.js",
    "revision": "5c9fec8e5dce50816ab17d5b9a9b815b"
  },
  {
    "url": "assets/js/136.dfce1453.js",
    "revision": "3f95b12418b6e41e27776466d0ecf37a"
  },
  {
    "url": "assets/js/137.19b9358b.js",
    "revision": "d87983e76ec25049636422719e14eb5e"
  },
  {
    "url": "assets/js/138.4628222f.js",
    "revision": "30af8820b427437ad7290a8de8ea1c40"
  },
  {
    "url": "assets/js/139.e048fd96.js",
    "revision": "28d00face1b910fa9610cad6f53b8b15"
  },
  {
    "url": "assets/js/14.f9ba4c72.js",
    "revision": "7529f41ede7af955960ce6c13789f87a"
  },
  {
    "url": "assets/js/140.0d0066fc.js",
    "revision": "00cdaa792720288a62eb9cc1d795603e"
  },
  {
    "url": "assets/js/141.c797adcf.js",
    "revision": "d59bf664c53428b94b7f26ea36d0e2b8"
  },
  {
    "url": "assets/js/142.5d1f3e06.js",
    "revision": "f63d6ad5c31103f13c9beec6c0cf8791"
  },
  {
    "url": "assets/js/143.1ff35cca.js",
    "revision": "200515b65e58eb23ef52eeb10770dcdc"
  },
  {
    "url": "assets/js/144.972bdca1.js",
    "revision": "e9127b964714dbfb7ab2637397e0cab9"
  },
  {
    "url": "assets/js/145.1cd179bb.js",
    "revision": "cd6c353b215e48d2f43d0a3d9428f47b"
  },
  {
    "url": "assets/js/146.9fbdd928.js",
    "revision": "2666d378951969f7d35da54b7fa96445"
  },
  {
    "url": "assets/js/147.f9b0cca8.js",
    "revision": "e521810195a85835575659b3f1632a0b"
  },
  {
    "url": "assets/js/148.22528477.js",
    "revision": "36f4e6993ff956b95b80204aa168b2fc"
  },
  {
    "url": "assets/js/149.6939e2e9.js",
    "revision": "d8ccb150337b4a401b786cdb6b32b2f9"
  },
  {
    "url": "assets/js/15.992fe3d9.js",
    "revision": "bb32c69cab8efc0b432c1bbbe47fbc75"
  },
  {
    "url": "assets/js/150.67520d0e.js",
    "revision": "ffa41bb8f3cc3b49dfa39eca09e45aa5"
  },
  {
    "url": "assets/js/151.e6a59faf.js",
    "revision": "87dbaa83ba235461a97edd674491a19a"
  },
  {
    "url": "assets/js/152.6553619a.js",
    "revision": "8757439b6577912de7cceaa54d0a4edb"
  },
  {
    "url": "assets/js/153.c2ad7863.js",
    "revision": "00bfaf71bac256241e3a63b6d4c5c2ec"
  },
  {
    "url": "assets/js/154.ad50a312.js",
    "revision": "d9ea6bd818b4b3909f8b4a95e1cb88fa"
  },
  {
    "url": "assets/js/155.328903d3.js",
    "revision": "ecbdc1991b6313d5c9c9d24e0dffa005"
  },
  {
    "url": "assets/js/156.183446c8.js",
    "revision": "be9e6c21a9449cb49bcfc251e5cf5363"
  },
  {
    "url": "assets/js/157.3b4cda49.js",
    "revision": "5ab1c233d3fe601303ccc355c3136ae2"
  },
  {
    "url": "assets/js/158.b5bbdc0e.js",
    "revision": "e6ebfed15fece2be9a491c301e908b33"
  },
  {
    "url": "assets/js/159.f7d39921.js",
    "revision": "4f6ef1e701e0974e4caad1d6cb532ea8"
  },
  {
    "url": "assets/js/16.bcdcb467.js",
    "revision": "e34e09edc343fa3d0d214dec3c83580c"
  },
  {
    "url": "assets/js/160.2cd9ade1.js",
    "revision": "72150f20b1eaa6f919ca182b65c5aafc"
  },
  {
    "url": "assets/js/161.9cbeac08.js",
    "revision": "72eeff276b65f120ead6f5e6abdef1d0"
  },
  {
    "url": "assets/js/162.fb37a531.js",
    "revision": "735e8b12bbb60bdb2d3147b6dd2b575a"
  },
  {
    "url": "assets/js/163.443226af.js",
    "revision": "dc05c049a306a155a2a1a635fd7632f3"
  },
  {
    "url": "assets/js/164.c589e0fe.js",
    "revision": "5ce55abfc2fadd50d428cf5e8797c6df"
  },
  {
    "url": "assets/js/165.9572c3e9.js",
    "revision": "c5a0fa37c7d120fbd20c21efb7057bd8"
  },
  {
    "url": "assets/js/166.fa839f30.js",
    "revision": "ae8065861f8c779a297d6d89947d04f9"
  },
  {
    "url": "assets/js/167.7c3a88cf.js",
    "revision": "34d70af0a05dcabdb99570be57196a20"
  },
  {
    "url": "assets/js/168.68d5bfc6.js",
    "revision": "0ee9970638881141d7b598ebdf260095"
  },
  {
    "url": "assets/js/169.a579c78a.js",
    "revision": "b38910106db3609be4b8ff9e6df812b5"
  },
  {
    "url": "assets/js/17.478b9cbc.js",
    "revision": "67d74bb5d964911ceb72479ad4e8024f"
  },
  {
    "url": "assets/js/170.c8b15be9.js",
    "revision": "efd59f223e9f9bfce17cad271df30759"
  },
  {
    "url": "assets/js/171.a2d06493.js",
    "revision": "109bcc5e00a5905b2d0f4d2fd40faf3a"
  },
  {
    "url": "assets/js/172.acba45d0.js",
    "revision": "5c8372d1d507bc60c4a2c146f23dbeb2"
  },
  {
    "url": "assets/js/173.1081032c.js",
    "revision": "561b4db26b30444ce3d2b9d66c9b84b4"
  },
  {
    "url": "assets/js/174.4e0de1ca.js",
    "revision": "9ed5090aaac19c4064356d7833b26645"
  },
  {
    "url": "assets/js/175.a30c4351.js",
    "revision": "6cbc4d04d5e3e5a89215043759a221e3"
  },
  {
    "url": "assets/js/176.1403f2eb.js",
    "revision": "40f0afdc249ed28260d035ba5b45c015"
  },
  {
    "url": "assets/js/177.3fde5517.js",
    "revision": "4ba447c067c03e691f24180c1d872e6c"
  },
  {
    "url": "assets/js/178.b57f9665.js",
    "revision": "85025779f116a449393085b7b19f1a25"
  },
  {
    "url": "assets/js/179.187bec29.js",
    "revision": "cb3e1616bfb2cb627e0df53cf6532cc8"
  },
  {
    "url": "assets/js/18.4e6f8f57.js",
    "revision": "5279f524b5d94fe7b1ad39962888200a"
  },
  {
    "url": "assets/js/180.90025091.js",
    "revision": "b88ad9995b2b96a555f5c520dca97792"
  },
  {
    "url": "assets/js/181.72fc6300.js",
    "revision": "260b6484ba85aa59ea42cefab2cc396e"
  },
  {
    "url": "assets/js/182.b2725faa.js",
    "revision": "2ac80acf312d128fe0f368ad95de8318"
  },
  {
    "url": "assets/js/183.a3e456f2.js",
    "revision": "37b074f5b49e8ef0771add2f34b86361"
  },
  {
    "url": "assets/js/184.c23a1ca1.js",
    "revision": "f8bd2a6d162b034f24f36d339cf41b1b"
  },
  {
    "url": "assets/js/185.c0736cab.js",
    "revision": "3d83c43b1d53e1610943ba980d1945be"
  },
  {
    "url": "assets/js/186.ddee830a.js",
    "revision": "1707df5efddafaee422df5128e9f50c8"
  },
  {
    "url": "assets/js/187.1bbff6f5.js",
    "revision": "9e16b6e331d0b952113ed3d35e272aef"
  },
  {
    "url": "assets/js/188.a5ea22ae.js",
    "revision": "7a6d88bd03dd35cdd6f8acbc863b40a8"
  },
  {
    "url": "assets/js/189.958bec88.js",
    "revision": "f552a4240fd82572f71471d340545500"
  },
  {
    "url": "assets/js/19.49a103b6.js",
    "revision": "c4e50dd8faf2ccd8ea6df2d5948081a6"
  },
  {
    "url": "assets/js/190.c28d4588.js",
    "revision": "1a858cc99c9d86f9236d6658b87bc36d"
  },
  {
    "url": "assets/js/191.f7939d07.js",
    "revision": "be48d4bb2659f7742b42f137dbf1b4c6"
  },
  {
    "url": "assets/js/192.a7fcfbf6.js",
    "revision": "468b5ea38a431f03050b776e79224df1"
  },
  {
    "url": "assets/js/193.f286bcf7.js",
    "revision": "ae32d1b5f612c084debfdd66d846b5b3"
  },
  {
    "url": "assets/js/194.b87e3ada.js",
    "revision": "95571a37057b5b9fa6fac3cf8d6be15a"
  },
  {
    "url": "assets/js/195.5d43c445.js",
    "revision": "44d58911c8081536348e80d9b364f69a"
  },
  {
    "url": "assets/js/196.189e725e.js",
    "revision": "e52b003f514af0aa4a2c56a914af8fdc"
  },
  {
    "url": "assets/js/197.374e5424.js",
    "revision": "8d1aad6be007c1cd70fe74eb7a1fd6b4"
  },
  {
    "url": "assets/js/198.d6caea2b.js",
    "revision": "7900c8e2cefb7f5555f509e7063c51be"
  },
  {
    "url": "assets/js/199.fce42211.js",
    "revision": "3742e9cce31baac1cb69a792a0b30113"
  },
  {
    "url": "assets/js/20.5468a3ce.js",
    "revision": "6bbf351196d50ae752e3884e232884f0"
  },
  {
    "url": "assets/js/200.d2d832ee.js",
    "revision": "20454d152ca9964fecb153149c9acd1e"
  },
  {
    "url": "assets/js/201.f49a50d8.js",
    "revision": "9f47cd01a2c668269c03bf71e4145280"
  },
  {
    "url": "assets/js/202.30b71f79.js",
    "revision": "48f799e21151643f287b3e84dd6e701b"
  },
  {
    "url": "assets/js/203.f6ad6a83.js",
    "revision": "cac9128e083976703afda51b5dc4437e"
  },
  {
    "url": "assets/js/204.0c3a9899.js",
    "revision": "5ad1110dd0b840506b9da3dfee6ef65f"
  },
  {
    "url": "assets/js/205.b37f719b.js",
    "revision": "2bd5b497108410f8bd8fa2e453b1b1bb"
  },
  {
    "url": "assets/js/206.f421ce3d.js",
    "revision": "6c9fefaeb0fd9d4f42b87367006d6b55"
  },
  {
    "url": "assets/js/207.547f4269.js",
    "revision": "3edeff146035872f96f280f9a87a4cdc"
  },
  {
    "url": "assets/js/208.b5d501bb.js",
    "revision": "a8fa2540c49b8ce59b622653052d71b4"
  },
  {
    "url": "assets/js/209.d9853e32.js",
    "revision": "e308fac4f3430269ea79a0403c12baf8"
  },
  {
    "url": "assets/js/21.673ee967.js",
    "revision": "22aa0558e5b610006b246a25070419ce"
  },
  {
    "url": "assets/js/210.f72c2d6f.js",
    "revision": "19f1b2a709999a1be9bd1ae5f69104ba"
  },
  {
    "url": "assets/js/211.062af830.js",
    "revision": "d6a893ce5b65dfed4f064ca75ae85383"
  },
  {
    "url": "assets/js/212.31860a45.js",
    "revision": "db29fadd145995873bc31de654b74bf0"
  },
  {
    "url": "assets/js/213.8d7c3997.js",
    "revision": "3b3b1b710be73c86e5f3eb6e21d07e6d"
  },
  {
    "url": "assets/js/214.bd72dba2.js",
    "revision": "a226d547b9adfc8b2ef34e4b0bcebe7f"
  },
  {
    "url": "assets/js/215.9f662bfe.js",
    "revision": "3b2fc024944a597936c3fbc3b7150b2a"
  },
  {
    "url": "assets/js/216.2f34fbb3.js",
    "revision": "4e2d77f281a3161fb040132e120210a4"
  },
  {
    "url": "assets/js/217.693c7894.js",
    "revision": "66eb73b3a462508e733b056fbd79a544"
  },
  {
    "url": "assets/js/218.a42fa434.js",
    "revision": "f9c5c9415ae3df635293c9b44a5c9d65"
  },
  {
    "url": "assets/js/219.f27149cd.js",
    "revision": "1f35702e90c207442970e3bfdd8d4124"
  },
  {
    "url": "assets/js/22.6a304c43.js",
    "revision": "7e3726c44ae88d354b3fd3fe677a863f"
  },
  {
    "url": "assets/js/220.d998a37f.js",
    "revision": "05c10c1502aad4fdda58c14baa5e7412"
  },
  {
    "url": "assets/js/221.a1cb6e69.js",
    "revision": "e2aee30e19708d1f9f0df10ff7bded41"
  },
  {
    "url": "assets/js/222.b77b6a63.js",
    "revision": "fcd52e94d5b015a4260e588b7010c503"
  },
  {
    "url": "assets/js/223.f3fd8934.js",
    "revision": "3e78c4407333d622afff1693379da90c"
  },
  {
    "url": "assets/js/224.39ba7138.js",
    "revision": "03c7cbc3524693e65022d231bc873205"
  },
  {
    "url": "assets/js/225.35885378.js",
    "revision": "d73719e582e958cfb3f139cce02d6bc8"
  },
  {
    "url": "assets/js/226.cd921f26.js",
    "revision": "e6935a1e15cefcfb99085e2a05d7467c"
  },
  {
    "url": "assets/js/227.95216b8d.js",
    "revision": "771402eb4ff383d7c98cf82b6efc1326"
  },
  {
    "url": "assets/js/228.8de24483.js",
    "revision": "c7cf2d6a3a8196dd365671fe58bfffee"
  },
  {
    "url": "assets/js/229.a6374252.js",
    "revision": "f092a2762c7f480c5235a429f335f282"
  },
  {
    "url": "assets/js/23.5f807091.js",
    "revision": "db49f5a6d11822d4ae1e548c78a6ff12"
  },
  {
    "url": "assets/js/230.2a173121.js",
    "revision": "9823d6da46f794b298244c649294ea3c"
  },
  {
    "url": "assets/js/231.891ee601.js",
    "revision": "0ba5260fb655154445d106be1cfa0847"
  },
  {
    "url": "assets/js/232.de608836.js",
    "revision": "e3c8584b529bb5b3ece3330f507ce254"
  },
  {
    "url": "assets/js/233.49d14c27.js",
    "revision": "f8b38cd05f05d8d25008c039743201e7"
  },
  {
    "url": "assets/js/234.106bf797.js",
    "revision": "e17c40727d8a6f5f166c592009e04838"
  },
  {
    "url": "assets/js/235.1f28fb42.js",
    "revision": "28a27fa44c5a5d30f00ee7e59e899509"
  },
  {
    "url": "assets/js/236.e3e83aaf.js",
    "revision": "e83ecb747a1382b99b0caa8122d3ddce"
  },
  {
    "url": "assets/js/237.e30fdf94.js",
    "revision": "150624abde40de989ca484bc542c6340"
  },
  {
    "url": "assets/js/238.7ecbd987.js",
    "revision": "1a0f152173bf13b211a4b2c0489d6144"
  },
  {
    "url": "assets/js/239.5e26542c.js",
    "revision": "e62e76c958704c149d2bedee529f7508"
  },
  {
    "url": "assets/js/24.5a089fe4.js",
    "revision": "47b684d9fff2db494f05cd5d5199be59"
  },
  {
    "url": "assets/js/240.360d9c23.js",
    "revision": "c30e749bc8c5239fcad9a40027cd44ed"
  },
  {
    "url": "assets/js/241.ffa3b067.js",
    "revision": "6d3970eaa175c3af0a5b2385404eeeca"
  },
  {
    "url": "assets/js/242.b780a7a3.js",
    "revision": "d083f5c8af1a74cdb660de1698482841"
  },
  {
    "url": "assets/js/243.83499c28.js",
    "revision": "59de6d709d0bd24ceeaf724a7773f7a2"
  },
  {
    "url": "assets/js/244.c6aa1302.js",
    "revision": "1c58f43eea89ee2c6c78a1196a2565f4"
  },
  {
    "url": "assets/js/245.99080dd8.js",
    "revision": "a2082762a4f6dd94511b8e4c90136d72"
  },
  {
    "url": "assets/js/246.7f3e201f.js",
    "revision": "c8e174373c7d0b9fa5c0595d576cd671"
  },
  {
    "url": "assets/js/247.7ed04c54.js",
    "revision": "c087ded6c2c3ba80bc0d4e4415024b5f"
  },
  {
    "url": "assets/js/248.83fb986f.js",
    "revision": "bbb0aca7b7590233299ffbd8616d3456"
  },
  {
    "url": "assets/js/249.e78c265f.js",
    "revision": "e75f0d8507da7329bd3c1735385d172b"
  },
  {
    "url": "assets/js/25.692f4d49.js",
    "revision": "08c6c5f59113b8e796af3b0321ebb8c7"
  },
  {
    "url": "assets/js/250.83475ecd.js",
    "revision": "1fd9ef348da604ed1b35ea3b556df1d2"
  },
  {
    "url": "assets/js/251.3fc98285.js",
    "revision": "0d29d323ba036c54292345d37906b298"
  },
  {
    "url": "assets/js/252.4296942d.js",
    "revision": "a45c94f8422b17b1258b1e08b8a98766"
  },
  {
    "url": "assets/js/253.cae8e6e4.js",
    "revision": "3bb90b997f3446cb92df0632bb3a80b9"
  },
  {
    "url": "assets/js/254.57de4e53.js",
    "revision": "8e5eec9bdeb1e8c45b95e50f7095aa98"
  },
  {
    "url": "assets/js/255.20a4b6ae.js",
    "revision": "5f5fe7f65850f1ee13475627a4593df1"
  },
  {
    "url": "assets/js/256.df4aafd1.js",
    "revision": "514c03060a36e72c5021637657ed7088"
  },
  {
    "url": "assets/js/26.e9eee22c.js",
    "revision": "cf46e24104851aa15580df55e1c8cd97"
  },
  {
    "url": "assets/js/27.4e0cf912.js",
    "revision": "1e8c71dda6aff0281f6c954b436d4f76"
  },
  {
    "url": "assets/js/28.2ded3eaa.js",
    "revision": "edc5543d3492ac54baa66d0e34e48960"
  },
  {
    "url": "assets/js/29.3e2368e5.js",
    "revision": "aece5ee812956b1936a183c3c2b07f4e"
  },
  {
    "url": "assets/js/30.4bbc5af3.js",
    "revision": "505d99b035af971689860d430d17e04a"
  },
  {
    "url": "assets/js/31.45b7b6a6.js",
    "revision": "9106f84902ba17cd6191331e157fd481"
  },
  {
    "url": "assets/js/32.69ab0407.js",
    "revision": "75bd1cec35c43891ecbe7e57513d1ec4"
  },
  {
    "url": "assets/js/33.39c86a9b.js",
    "revision": "5bfce0d80790762542acab60ef2fc949"
  },
  {
    "url": "assets/js/34.254f7d6f.js",
    "revision": "858876a1ba28efd340caa4103853f955"
  },
  {
    "url": "assets/js/35.4918eea5.js",
    "revision": "2917974111d569409cbc0f697b2023ae"
  },
  {
    "url": "assets/js/36.97e6b083.js",
    "revision": "27ba4c61b30c641c45b52597bc89b9dd"
  },
  {
    "url": "assets/js/37.cd6f06f3.js",
    "revision": "d78d8e5cc091e9e333547cfa0cf1072a"
  },
  {
    "url": "assets/js/38.a4f1f250.js",
    "revision": "ac0dd9824a3f3394ee6c00be76c530dd"
  },
  {
    "url": "assets/js/39.4d35e0bd.js",
    "revision": "02bc733fdd228134fd5d1687af7abae2"
  },
  {
    "url": "assets/js/4.c6478e1c.js",
    "revision": "a0cdccecd2173b58c750dad3257a4950"
  },
  {
    "url": "assets/js/40.43e6d215.js",
    "revision": "dc356888371469a6d001271921697681"
  },
  {
    "url": "assets/js/41.e40dbe00.js",
    "revision": "044ab4a381cf58f874b1913b5c626870"
  },
  {
    "url": "assets/js/42.df765cb2.js",
    "revision": "6208ea4b2a021314d9b4244df916c2f6"
  },
  {
    "url": "assets/js/43.8975fa0a.js",
    "revision": "94070a38dc14b18ac3c3d37999c70847"
  },
  {
    "url": "assets/js/44.0eaf013d.js",
    "revision": "7c6cb60234f79d25352216cfec4fd1f7"
  },
  {
    "url": "assets/js/45.58bb5f6d.js",
    "revision": "b04115a08afd66fd83ca80d2e8faa00b"
  },
  {
    "url": "assets/js/46.1ef18f90.js",
    "revision": "842a1e74c046474d13183987980c8ef6"
  },
  {
    "url": "assets/js/47.4ad41ec6.js",
    "revision": "adaaa7a9b8c036cc7c0663e5442ac131"
  },
  {
    "url": "assets/js/48.de82f6f9.js",
    "revision": "b3de84363a931f6c8b6045978e5a31f0"
  },
  {
    "url": "assets/js/49.77147adc.js",
    "revision": "2c187cc62b748ac722161a3471022106"
  },
  {
    "url": "assets/js/5.d2205e80.js",
    "revision": "4699096864fb0ad1b2a753e30400c4da"
  },
  {
    "url": "assets/js/50.6820eb1d.js",
    "revision": "338a6e062fc96129be6d9e4d13c6ab06"
  },
  {
    "url": "assets/js/51.ede260be.js",
    "revision": "585514e300a60da9dde2df069e34928d"
  },
  {
    "url": "assets/js/52.8eff543e.js",
    "revision": "cefc1e142697875317e4d37fa4d12aae"
  },
  {
    "url": "assets/js/53.c7553d91.js",
    "revision": "752b9d38de8921108e06f0143fa8695d"
  },
  {
    "url": "assets/js/54.959a5e47.js",
    "revision": "afa9ec435d6d6e38cbf277b804e7b621"
  },
  {
    "url": "assets/js/55.69761532.js",
    "revision": "a79d687b4c4f765cea5d7df230d01a4c"
  },
  {
    "url": "assets/js/56.e39c4a02.js",
    "revision": "8dd3b1927754261111a26909fc156af1"
  },
  {
    "url": "assets/js/57.12368602.js",
    "revision": "ebdccdca08168d6b3a4d3105dc8cb541"
  },
  {
    "url": "assets/js/58.ee3a2925.js",
    "revision": "15825f2bed78562510658069e6b5f993"
  },
  {
    "url": "assets/js/59.db7ecd7f.js",
    "revision": "f36c10d3e741d0eb7d1d89e5a1989d1d"
  },
  {
    "url": "assets/js/6.6c842c61.js",
    "revision": "b325aca78542bb6269243a4f055427dd"
  },
  {
    "url": "assets/js/60.0ca8b191.js",
    "revision": "2e11e6dc67a0595d68aafd23f3bef47b"
  },
  {
    "url": "assets/js/61.de1a34cd.js",
    "revision": "7d183eb18924b0499a8a9284a85eb09d"
  },
  {
    "url": "assets/js/62.156eeacb.js",
    "revision": "dff5891b1fdd50c3eed65989f07194fa"
  },
  {
    "url": "assets/js/63.382088d0.js",
    "revision": "9de10ce2c16095ecb1f01a97f8ff79a3"
  },
  {
    "url": "assets/js/64.7e3af515.js",
    "revision": "37021b0cca246cccb2f1e7ee2ca75ff8"
  },
  {
    "url": "assets/js/65.ed1a240d.js",
    "revision": "3d502c64cb1b560f97a06e3af767dc73"
  },
  {
    "url": "assets/js/66.60dc53c5.js",
    "revision": "c52a2e051d4b62fc339fef423057802e"
  },
  {
    "url": "assets/js/67.756b66f5.js",
    "revision": "4b5fabc93755f6ef2350007bcb1d47f3"
  },
  {
    "url": "assets/js/68.6df6f4b0.js",
    "revision": "16a31524a8e8acad44b27b4f9c5f29e0"
  },
  {
    "url": "assets/js/69.ce426eb0.js",
    "revision": "738e61fef4af0351d84fcbf671eadcb1"
  },
  {
    "url": "assets/js/7.740246ac.js",
    "revision": "6a45dba50e8a299298cb76989c055982"
  },
  {
    "url": "assets/js/70.18c88869.js",
    "revision": "8644e5878bf53c74561b9d0ca61b38b6"
  },
  {
    "url": "assets/js/71.f107a4fc.js",
    "revision": "f69be344a7210fda9d1c2c97ba90af2b"
  },
  {
    "url": "assets/js/72.c7b47378.js",
    "revision": "33e9ff16ba21c7f248882100e293f0bb"
  },
  {
    "url": "assets/js/73.2b4409db.js",
    "revision": "a53ec790fee15e7d49f598ed75696481"
  },
  {
    "url": "assets/js/74.c7adc88a.js",
    "revision": "743b4f65217a8784d338216bd0e0359c"
  },
  {
    "url": "assets/js/75.0ccf628b.js",
    "revision": "a961d348308d0182ca368db1e8e32704"
  },
  {
    "url": "assets/js/76.2f6d45d2.js",
    "revision": "21fa66c05b064dd135e2c7c3956be784"
  },
  {
    "url": "assets/js/77.b2a9ca03.js",
    "revision": "02bb645db2921d76cc138d232560986f"
  },
  {
    "url": "assets/js/78.47ec1fbd.js",
    "revision": "f619530dcc8f71c50aa4ddd9f2729792"
  },
  {
    "url": "assets/js/79.2ac9b08b.js",
    "revision": "7483cd7a13e77dfe8b5aa8c6df822731"
  },
  {
    "url": "assets/js/8.d84ec37a.js",
    "revision": "68f54e1e0568a705e407cd0a524b1711"
  },
  {
    "url": "assets/js/80.39950fda.js",
    "revision": "734656be7d46eff344c31c2c559718e4"
  },
  {
    "url": "assets/js/81.2682a455.js",
    "revision": "76dc4262dc2b06a04bbd4b3430812789"
  },
  {
    "url": "assets/js/82.2751592a.js",
    "revision": "7107e73e0ee6c94fd62e52fb89997f67"
  },
  {
    "url": "assets/js/83.5149f135.js",
    "revision": "15eba28eb555809a31171604ed4381c6"
  },
  {
    "url": "assets/js/84.23ef4f23.js",
    "revision": "2f5e210aa5dfa7aa6b4f82c1e619e43b"
  },
  {
    "url": "assets/js/85.2270f2c6.js",
    "revision": "7d7d146bb1b113dc6e9a8a1602e2a831"
  },
  {
    "url": "assets/js/86.a20018e3.js",
    "revision": "325b5165baa6e74426fa864c77f56caf"
  },
  {
    "url": "assets/js/87.62df9412.js",
    "revision": "605044ccaa21abad86f58dc40b6dd321"
  },
  {
    "url": "assets/js/88.0a488943.js",
    "revision": "5b0879df070a00daabc049bd01e4be04"
  },
  {
    "url": "assets/js/89.cd073d8b.js",
    "revision": "c6bfb43185471c16a46f348c1269cd15"
  },
  {
    "url": "assets/js/9.18b9f60a.js",
    "revision": "b0267141e6d0e1aa4937b44cdd28891e"
  },
  {
    "url": "assets/js/90.bf5b70cc.js",
    "revision": "ecce0730a26e5b056dac0efbcb167e39"
  },
  {
    "url": "assets/js/91.313184e2.js",
    "revision": "a9cb7d664349bbe3ec9ad70041b7230d"
  },
  {
    "url": "assets/js/92.4f6a7ded.js",
    "revision": "4200503bb2c2ee06fc048b0638d3fd26"
  },
  {
    "url": "assets/js/93.25d3365a.js",
    "revision": "fd41c5b955d4263601cbe235b9991d28"
  },
  {
    "url": "assets/js/94.38ac9971.js",
    "revision": "9d4cc761a2b429353e92fe034765d9d1"
  },
  {
    "url": "assets/js/95.b552cea8.js",
    "revision": "edca481524ee53b05d553c3134a2deee"
  },
  {
    "url": "assets/js/96.55125488.js",
    "revision": "fb525921985d10df3ad6dc2085aff10c"
  },
  {
    "url": "assets/js/97.610e53f1.js",
    "revision": "d9f1b5963aa9cc77eaf85a6994d53362"
  },
  {
    "url": "assets/js/98.c7a19a42.js",
    "revision": "5b80090a83f7e2a30dc8b86eb2742c6e"
  },
  {
    "url": "assets/js/99.f133aa5e.js",
    "revision": "b1752bbe92c54e58fc7f3eba1cccf3f4"
  },
  {
    "url": "assets/js/app.458d20e6.js",
    "revision": "a59ff22cd109d10e097320ee7f2d83cf"
  },
  {
    "url": "assets/js/vendors~docsearch.4844e131.js",
    "revision": "360b23a0df3c6605374f8061d1e86891"
  },
  {
    "url": "changelog.html",
    "revision": "8e3f86ac2e46e11c4f8699876e284f0b"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "11179d471b036709261b30cea6465eab"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "e03f6747abdccf0d9f40298f3765e039"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "bc3759b3ad60b324adb1199978755557"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "f1a1fc412b14ff348f107a80b273ae52"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "b4f824e5f975f6789f74eef1d4e44a6c"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "8d5a9376641495464b34244836e76e41"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "15eb1fb5b6b89a5e98c49f6746d6a858"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "7431a03f6b0847718fcd84419bf72f0a"
  },
  {
    "url": "guide/feishu-guide.html",
    "revision": "2b4592d993644b3bab8330b32b189808"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "b91b56255bb32b7ff0dd297081d7ab9e"
  },
  {
    "url": "guide/index.html",
    "revision": "d40d02d6d8506ee7b5d699a1aa680701"
  },
  {
    "url": "guide/installation.html",
    "revision": "8d5aed62a12c8d405fea463bf810a3cb"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "231e7208cf4cd02dcb596f1a8890fee2"
  },
  {
    "url": "guide/mirai-guide.html",
    "revision": "7eb97cb39ae0368c0406ae3b0962a8f5"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "874fd30c654cc14eaec4eaa63b6a5bb1"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "489f0e44f36d8a225bbfd473324a1f62"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "1accc7bc56132c91ccff948edf15b653"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "60f2ad4cea28cb33721f61d7d71c3970"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "61bcceb590316984f82128df0a85a73f"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "1c7b58a3569271a958b3ebe765efca12"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "00c744096b4d5a8d490aa842734eaa69"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "a8ceaa9bc4ba0d8097e91873c9e78459"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "571a95ddf28fe4171b34ca11c66f0bfb"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "3ef03907f2359fd8bd5deb660f0972da"
  },
  {
    "url": "next/api/adapters/feishu.html",
    "revision": "bd51f14b5febb602aee04afa8a1815cc"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "9ed3f8291193c56868a2c8e73a430351"
  },
  {
    "url": "next/api/adapters/mirai.html",
    "revision": "a457c4cfadcef535e51ac53d6a7abcfa"
  },
  {
    "url": "next/api/config.html",
    "revision": "a01bd0b5bb0a1211a7c261e5c22b514b"
  },
  {
    "url": "next/api/drivers/aiohttp.html",
    "revision": "0f81ad97f274c4b6d3a1f2bbc9395330"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "3cc87953ef09ef3973e7e58e2ee261c7"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "91117b6621fb8e78068afe9a8eb73de7"
  },
  {
    "url": "next/api/drivers/quart.html",
    "revision": "3f8c0f92d95f315dc65311af8a9bc977"
  },
  {
    "url": "next/api/exception.html",
    "revision": "4a3b09c2291b558486f799f71cf6f09f"
  },
  {
    "url": "next/api/handler.html",
    "revision": "de3452f4fc56f25d573687d83e1e4ef4"
  },
  {
    "url": "next/api/index.html",
    "revision": "99e0d0a085cfdc513c2eb644caf865bb"
  },
  {
    "url": "next/api/log.html",
    "revision": "2d907ed93fd5a303c5192a52bc0c6ad6"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "328dffce18f1ea77a9c1b82c88885b53"
  },
  {
    "url": "next/api/message.html",
    "revision": "e9d1d557f635614344099135f5b395e8"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "dbb12255bd45f8a5b23f017019ad63f0"
  },
  {
    "url": "next/api/permission.html",
    "revision": "ce3feaccf8971048370fc9732b845aeb"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "13d91a616fbad87fc6f7da5cd99c9ec1"
  },
  {
    "url": "next/api/rule.html",
    "revision": "db6f4554e96a786543a8b3b22a5de583"
  },
  {
    "url": "next/api/typing.html",
    "revision": "cbdf37d99ef5f86ec18c0a713888cc0c"
  },
  {
    "url": "next/api/utils.html",
    "revision": "89a45a11a71c5be2508bb0d6eb63cccb"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "1b4700442e866501335c7beddbcf2c2d"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "ef6414f8b365b7f6178824faf1d54b86"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "791e0bf9e794c7e88aa8be7cb460a3fe"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "43d0249931bd24072ef455afeeea4695"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "f2077190ab0cc16dbb3e865fea82f29b"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "33336cba532dff35aab7d691fc3ec5af"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "a5ed7182ea0a4d359db428ddf498dd36"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "c21a6486fe944fc6b6823a5bb39308be"
  },
  {
    "url": "next/guide/feishu-guide.html",
    "revision": "5682d0e84008bc6ce3aa779d699c90e0"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "13595ed4ba52f683541372f897ebe0d0"
  },
  {
    "url": "next/guide/index.html",
    "revision": "1c59600c4b9a3e54f3838bb538f9c02a"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "892656021f6bb733b8fb6a6d2ec20b31"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "8ddaa103e1394d19703b89aad9f277ac"
  },
  {
    "url": "next/guide/mirai-guide.html",
    "revision": "5a4f7316c6ef273e302a602730b3c659"
  },
  {
    "url": "next/index.html",
    "revision": "ecb5826e556f00e9cc4a8abc0fee9515"
  },
  {
    "url": "store.html",
    "revision": "be11cf0dc67e673f90248d5c6e91b3ea"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
